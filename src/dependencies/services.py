from fastapi import Depends
from services.flight import FlightService
from dependencies.repository import flight_repository


async def flight_service(repository=Depends(flight_repository)) -> FlightService:
    return FlightService(repository=repository)
