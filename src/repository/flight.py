import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from sqlalchemy.orm import aliased
from datetime import date
from models.flight import FlightEvent
from models.location import City
from typing import Optional, List

logger = logging.getLogger(__name__)


class FlightRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_flight(self, code: str) -> Optional[FlightEvent]:
        return await self.session.get(FlightEvent, code)

    async def get_flights(self) -> List[FlightEvent]:
        stmt = select(FlightEvent)
        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def get_flight_by_origin_and_destination(
        self,
        origin_code: str,
        destination_code: str,
        date: date
    ) -> List[FlightEvent]:
        logger.debug(f"----- GET FLIGHT BY ORIGIN AND DESTINATION: {origin_code}, {destination_code}, {date} -----")
        origin_city = aliased(City)
        destination_city = aliased(City)

        stmt = (
            select(FlightEvent)
            .join(origin_city, FlightEvent.origin_id == origin_city.id)
            .join(destination_city,   FlightEvent.destination_id == destination_city.id)
            .where(
                origin_city.code      == origin_code,
                destination_city.code        == destination_code,
                FlightEvent.departure_date >= date,
            )
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_two_segment_connections(
        self,
        origin_code: str,
        destination_code: str
    ) -> list[tuple[FlightEvent, FlightEvent]]:
        f1 = aliased(FlightEvent)
        f2 = aliased(FlightEvent)
        origin_city = aliased(City)
        dest_city   = aliased(City)

        stmt = (
            select(f1, f2)

            .join(origin_city, f1.origin_id == origin_city.id)
            .where(origin_city.code == origin_code)

            .join(f2, f1.destination_id == f2.origin_id)
            .join(dest_city, f2.destination_id == dest_city.id)

            .where(dest_city.code == destination_code)

            .where(f2.departure_datetime >= f1.arrival_datetime)
        )

        result = await self.session.execute(stmt)
        return [(row[0], row[1]) for row in result.all()]


    async def get_flights_by_origin(
        self, origin_code: str
    ) -> list[FlightEvent]:
        stmt = (
            select(FlightEvent).join(FlightEvent.origin).where(City.code == origin_code, FlightEvent.active)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_flights_by_destination(
        self, destination_code: str
    ) -> list[FlightEvent]:
        stmt = (
            select(FlightEvent).join(FlightEvent.destination).where(City.code == destination_code, FlightEvent.active)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()