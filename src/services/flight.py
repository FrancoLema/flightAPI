from models.location import City
from repository.flight import FlightRepository
from schemas.flight import FlightSchema, FlightConnection
from services.location import LocationService
from repository.location import LocationRepository
from exceptions.location import CityNotFoundError
from datetime import date, datetime
from typing import Union
from config.settings import BaseConfig
from dateutil.relativedelta import relativedelta

class FlightService:
    def __init__(self, repository: FlightRepository):
        self.repository = repository
        self.location_service = LocationService(repository=LocationRepository())

    
    async def _validate_flight_date(self, input_date: Union[date, datetime, str]) -> tuple[bool, str]:
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
            return False, f"Flight date cannot be in the past. Today is {today}."
        
        max_flight_date_months = BaseConfig.MAX_FLIGHT_DATE_MONTHS

        six_months_from_today = today + relativedelta(months=max_flight_date_months)
        if flight_date > six_months_from_today:
            return False, f"Flight date cannot be more than {max_flight_date_months} months in the future. Maximum allowed date is {six_months_from_today}."
        
        return True, "Date is valid."


    async def _validate_and_get_city(self, origin: str, destiny: str) -> tuple[City, City]:        
        origin_city = await self.location_service.get_city(origin)
        if not origin_city:
            raise CityNotFoundError(f"City with code {origin} not found")
        destiny_city = await self.location_service.get_city(destiny)
        if not destiny_city:
            raise CityNotFoundError(f"City with code {destiny} not found")
        return origin_city, destiny_city

    async def _get_flight_by_origin_and_destination(self, origin: City, destiny: City, date: datetime) -> None:
        """
        If its not a direct flight:
            1. Search for all the flight_events with the same destiny
            2. For each flight_event, filter for all the flight_events with the same origin
            3. Exclude the flight events with a total duration greater than 24 hours
            4. Exclude the flight events where the difference between the arrival of the first event and the departure of the second event is greater than 4 hours.
            5. Return the flight_event with the lowest price
        """
        flight_event = await self.repository.get_flight_by_origin_and_destination(origin, destiny, date)
        if flight_event:
            return flight_event
        else:
            return None

    async def _search_flight_connections(self, origin: City, destiny: City, date: datetime) -> FlightConnection:
        """
        Search for the flight in the database.
        If its not a direct flight_event, we need to search for the origin and destiny between connections.
            In this version we limit the MAX amount of flight-events in a travel to 2.  
        """
        flight_event = await self._get_flight_by_origin_and_destination(origin, destiny, date)
        if flight_event:
            return FlightConnection(connections=0, path=[flight_event])
        else:
            return FlightConnection(connections=1, path=[flight_event])

    async def search_flight(self, flight_info: FlightSchema) -> FlightConnection:
        try:
            if flight_info.from_ == flight_info.to:
                raise ValueError("Origin and destiny cannot be the same")
            origin, destiny = await self._validate_and_get_city(flight_info.from_, flight_info.to)
            is_valid, error_message = await self._validate_flight_date(flight_info.date)
            if not is_valid:
                raise ValueError(error_message)
            flight_connections = await self._search_flight_connections(origin, destiny, flight_info.date)
                
        except Exception as e:
            raise ValueError(e)
        
        return flight_connections