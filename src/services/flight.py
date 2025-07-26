from models.flight import FlightEvent
from repository.flight import FlightRepository


class FlightService:
    def __init__(self, repository: FlightRepository):
        self.repository = repository

    async def get_flight(self, flight_id: int) -> FlightEvent:
        return await self.repository.get_flight(flight_id)

    async def get_flights(self) -> list[FlightEvent]:
        return await self.repository.get_flights()
