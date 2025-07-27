#!/usr/bin/env python
import sys
import json
from pathlib import Path
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import BaseConfig
from models.location import Country, State, City
from models.flight import FlightEvent

DATABASE_URL = BaseConfig.DATABASE_URL.replace(
    "postgresql+asyncpg://", "postgresql+asyncpg://"
)
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

DATA_DIR = PROJECT_ROOT / "data"
SEED_FILE = DATA_DIR / "seed.json"


async def seed():
    data = json.loads(SEED_FILE.read_text())

    async with AsyncSessionLocal() as session:
        for c in data.get("countries", []):
            session.add(
                Country(
                    name=c["name"],
                    code=c["code"],
                    coordinates=c["coordinates"],
                )
            )

        for s in data.get("states", []):
            country = (
                await session.execute(
                    select(Country).where(Country.code == s["country_code"])
                )
            ).scalar_one()
            session.add(
                State(
                    name=s["name"],
                    code=s["code"],
                    coordinates=s["coordinates"],
                    country_id=country.id,
                )
            )

        for c in data.get("cities", []):
            state = (
                await session.execute(
                    select(State).where(State.code == c["state_code"])
                )
            ).scalar_one()
            session.add(
                City(
                    name=c["name"],
                    code=c["code"],
                    coordinates=c["coordinates"],
                    timezone=c["timezone"],
                    state_id=state.id,
                )
            )

        for f in data.get("flights", []):
            origin = (
                await session.execute(
                    select(City).where(City.code == f["departure_city_code"])
                )
            ).scalar_one()
            dest = (
                await session.execute(
                    select(City).where(City.code == f["arrival_city_code"])
                )
            ).scalar_one()

            session.add(
                FlightEvent(
                    flight_number=f["flight_number"],
                    departure_date=datetime.fromisoformat(
                        f["departure_datetime"][:10]
                    ).date(),
                    departure_datetime=datetime.fromisoformat(f["departure_datetime"]),
                    arrival_date=datetime.fromisoformat(
                        f["arrival_datetime"][:10]
                    ).date(),
                    arrival_datetime=datetime.fromisoformat(f["arrival_datetime"]),
                    origin_id=origin.id,
                    destination_id=dest.id,
                    active=True,
                )
            )

        await session.commit()

    await engine.dispose()


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed())
