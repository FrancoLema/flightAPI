from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db import get_session
from repository.flight import FlightRepository
from repository.location import LocationRepository


async def flight_repository(
    session: AsyncSession = Depends(get_session),
) -> FlightRepository:
    return FlightRepository(session=session)


async def location_repository(
    session: AsyncSession = Depends(get_session),
) -> LocationRepository:
    return LocationRepository(session=session)
