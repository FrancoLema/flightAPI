from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db import get_session
from repository.flight import FlightRepository


async def flight_repository(
    session: AsyncSession = Depends(get_session),
) -> FlightRepository:
    return FlightRepository(session=session)
