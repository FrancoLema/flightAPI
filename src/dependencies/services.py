from fastapi import Depends
from services.flight import FlightService
from dependencies.repository import flight_repository, location_repository
from services.location import LocationService


async def location_service(repository=Depends(location_repository)) -> LocationService:
    return LocationService(repository=repository)


async def flight_service(
    repository=Depends(flight_repository), location_service=Depends(location_service)
) -> FlightService:
    return FlightService(repository=repository, location_service=location_service)
