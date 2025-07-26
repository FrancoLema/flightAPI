from repository.location import LocationRepository
from models.location import City, State, Country

class LocationService:
    def __init__(self, repository: LocationRepository):
        self.repository = repository

    async def get_city(self, city_code: str) -> City:
        return await self.repository.get_city(city_code)

    async def get_state(self, state_code: str) -> State:
        return await self.repository.get_state(state_code)

    async def get_country(self, country_code: str) -> Country:
        return await self.repository.get_country(country_code)
