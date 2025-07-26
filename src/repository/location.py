from sqlalchemy.ext.asyncio import AsyncSession

from models.location import City, State, Country


class LocationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_city(self, city_code: str) -> City:
        return await self.session.query(City).filter(City.code == city_code).first()

    async def get_state(self, state_code: str) -> State:
        return await self.session.query(State).filter(State.code == state_code).first()

    async def get_country(self, country_code: str) -> Country:
        return await self.session.query(Country).filter(Country.code == country_code).first()
