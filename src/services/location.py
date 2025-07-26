from repository.location import LocationRepository
from models.location import City, State, Country
from exceptions.location import LocationNotFoundError


class LocationService:
    def __init__(self, repository: LocationRepository):
        self.repository = repository

    async def get_city(self, city_code: str) -> City:
        city = await self.repository.get_city(city_code)
        if not city:
            raise LocationNotFoundError(f"City with code {city_code} not found")
        return city

    async def get_state(self, state_code: str) -> State:
        state = await self.repository.get_state(state_code)
        if not state:
            raise LocationNotFoundError(f"State with code {state_code} not found")
        return state

    async def get_country(self, country_code: str) -> Country:
        country = await self.repository.get_country(country_code)
        if not country:
            raise LocationNotFoundError(f"Country with code {country_code} not found")
        return country
