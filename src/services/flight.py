import logging
from models.location import City
from models.flight import FlightEvent
from repository.flight import FlightRepository
from schemas.flight import FlightConnection, FlightCircuit
from services.location import LocationService
from exceptions.location import CityNotFoundError
from datetime import date, datetime, timedelta
from typing import Union, Optional
from config.settings import BaseConfig
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)


class FlightService:
    def __init__(self, repository: FlightRepository, location_service: LocationService):
        self.repository = repository
        self.location_service = location_service

    async def _validate_flight_date(
        self, input_date: Union[date, datetime, str]
    ) -> tuple[bool, str]:
        """
        Validate that a date is greater than today and less than 6 months from today.
        Args:
            input_date: Date to validate
        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        today = date.today()

        if isinstance(input_date, str):
            try:
                flight_date = datetime.strptime(input_date, "%Y-%m-%d").date()
            except ValueError:
                return False, "Invalid date format. Use YYYY-MM-DD format."
        elif isinstance(input_date, datetime):
            flight_date = input_date.date()
        elif isinstance(input_date, date):
            flight_date = input_date
        else:
            return False, "Invalid date type. Must be date, datetime, or string."

        if flight_date < today:
            return (
                False,
                f"Date must be equals or greater than today. Today is {today}.",
            )

        max_flight_date_months = BaseConfig.MAX_FLIGHT_DATE_MONTHS

        six_months_from_today = today + relativedelta(months=max_flight_date_months)
        if flight_date > six_months_from_today:
            return (
                False,
                f"Flight date cannot be more than {max_flight_date_months} months in the future. Maximum allowed date is {six_months_from_today}.",
            )

        return True, "Date is valid."

    async def _validate_and_get_city(
        self, origin: str, destiny: str
    ) -> tuple[City, City]:
        origin_city = await self.location_service.get_city(origin)
        if not origin_city:
            raise CityNotFoundError(f"City with code {origin} not found")
        destiny_city = await self.location_service.get_city(destiny)
        if not destiny_city:
            raise CityNotFoundError(f"City with code {destiny} not found")
        return origin_city, destiny_city

    async def _filter_date_for_connected_flights(
        self, flight_events: list[tuple[FlightEvent, FlightEvent]]
    ) -> list[tuple[FlightEvent, FlightEvent]]:
        """
        Exclude the flight events with a total duration greater than 24 hours and the difference between the arrival of the first event and the departure of the second event is greater than 4 hours.
        This both conditions are created in the repository, so we can filter directly by attributes.
        """

        max_duration = timedelta(hours=BaseConfig.MAX_FLIGHT_DURATION_HOURS)
        max_waiting_time = timedelta(hours=BaseConfig.MAX_WAITING_TIME_HOURS)

        filtered_flights = []
        for (
            flight_event_1,
            flight_event_2,
            waiting_time,
            total_duration,
        ) in flight_events:
            if total_duration <= max_duration and waiting_time <= max_waiting_time:
                flight_dict = {
                    "origin": flight_event_1,
                    "destination": flight_event_2,
                }
                filtered_flights.append(flight_dict)
        return filtered_flights

    async def _get_flight_by_origin_and_destination(
        self, origin: City, destiny: City, date: date
    ) -> tuple[Optional[FlightCircuit | None], bool]:
        """
        If its not a direct flight:
            1. Search for all the flight_events with the same destiny
            2. For each flight_event, filter for all the flight_events with the same origin
        """
        flight_events = await self.repository.get_flight_by_origin_and_destination(
            origin_code=origin.code, destination_code=destiny.code, date=date
        )

        if flight_events:
            flight_circuits = self._create_flight_circuit_dict(
                flight_events=flight_events
            )
            return flight_circuits, True

        else:
            flight_events = await self.repository.get_two_segment_connections(
                origin_code=origin.code, destination_code=destiny.code
            )
            if flight_events is None:
                return None, False
            else:
                filtered_flights = await self._filter_date_for_connected_flights(
                    flight_events=flight_events
                )
                flight_circuits = self._create_flight_circuit_connections_dict(
                    flight_events=filtered_flights
                )
                return flight_circuits, True

    async def _search_flight_connections(
        self, origin: City, destiny: City, date: datetime
    ) -> Optional[FlightConnection]:
        """
        Search for the flight in the database.
        If its not a direct flight_event, we need to search for the origin and destiny between connections.
            In this version we limit the MAX amount of flight-events in a travel to 2.
        """
        flight_event, exists = await self._get_flight_by_origin_and_destination(
            origin, destiny, date
        )
        if exists:
            connections = 0
            if len(flight_event) > 1:
                connections = 1
            return FlightConnection(connections=connections, path=flight_event)
        else:
            return None

    async def search_flight(
        self, origin: str, destiny: str, date: date
    ) -> Optional[FlightConnection]:
        try:
            if origin == destiny:
                raise ValueError("Origin and destiny cannot be the same")
            origin, destiny = await self._validate_and_get_city(origin, destiny)
            is_valid, error_message = await self._validate_flight_date(date)
            if not is_valid:
                raise ValueError(error_message)
            flight_connections = await self._search_flight_connections(
                origin, destiny, date
            )
            if flight_connections is None:
                raise ValueError("No flight connections found")
            return flight_connections

        except Exception as e:
            logger.error(f"Error searching flight: {e}")
            raise ValueError(e)

    def _create_flight_circuit_dict(
        self, flight_events: list[FlightEvent]
    ) -> list[FlightCircuit]:
        """
        Parse the flight events to a list of FlightCircuit.
        """
        flight_circuits = []

        for flight_event in flight_events:
            flight_circuit = FlightCircuit(
                flight_number=flight_event.flight_number,
                from_=flight_event.origin.code,
                to=flight_event.destination.code,
                departure_time=flight_event.departure_datetime,
                arrival_time=flight_event.arrival_datetime,
            )
            flight_circuits.append(flight_circuit)

        return flight_circuits

    def _create_flight_circuit_connections_dict(
        self, flight_events: list[dict[str, FlightEvent]]
    ) -> list[FlightCircuit]:
        """
        Parse the flight events to a list of FlightCircuit.
        The flight_events is a list of dictionaries with the first element being the first flight event and the second element being the second flight event.
        """
        flight_circuits = []

        for flight_connection in flight_events:
            origin_event = flight_connection.get("origin")
            dest_event = flight_connection.get("destination")

            if not origin_event or not dest_event:
                logger.warning(f"Incomplete flight connection: {flight_connection}")
                continue

            flight_circuit = FlightCircuit(
                flight_number=origin_event.flight_number,
                from_=origin_event.origin.code,
                to=dest_event.destination.code,
                departure_time=origin_event.departure_datetime,
                arrival_time=dest_event.arrival_datetime,
            )
            flight_circuits.append(flight_circuit)

        return flight_circuits
