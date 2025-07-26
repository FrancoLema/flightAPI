from sqlalchemy.ext.asyncio import AsyncSession

from models.flight import FlightEvent


class FlightRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_flight(self, flight_id: int) -> FlightEvent:
        return await self.session.get(FlightEvent, flight_id)

    async def get_flights(self) -> list[FlightEvent]:
        return await self.session.query(FlightEvent).all()
