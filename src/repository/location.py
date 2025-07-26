from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.location import City, State, Country


class LocationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_city(self, city_code: str) -> City:
        stmt = select(City).where(City.code == city_code)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_state(self, state_code: str) -> State:
        stmt = select(State).where(State.code == state_code)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_country(self, country_code: str) -> Country:
        stmt = select(Country).where(Country.code == country_code)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
