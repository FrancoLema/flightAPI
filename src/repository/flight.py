from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from models.flight import FlightEvent


class FlightRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_flight(self, code: str) -> FlightEvent:
        return await self.session.get(FlightEvent, code)

    async def get_flights(self) -> list[FlightEvent]:
        return await self.session.query(FlightEvent).all()

    async def get_flight_by_origin_and_destination(self, origin: str, destination: str, date: datetime) -> FlightEvent:
        return await self.session.query(FlightEvent).filter(FlightEvent.origin == origin, FlightEvent.destination == destination, FlightEvent.date == date).all()