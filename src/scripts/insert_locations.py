import os
import sys
from sqlalchemy import create_engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Country, State, City
from schemas.location import CountrySchema, StateSchema, CitySchema
from config.settings import BaseConfig
from infrastructure.db import BaseModel, get_session

DATABASE_URL = BaseConfig.DATABASE_URL
engine = create_engine(DATABASE_URL)

countries_data = [
    {
        "name": "Argentina",
        "code": "AR",
        "coordinates": "-34.6118,-58.3960"
    },
    {
        "name": "United States",
        "code": "US",
        "coordinates": "38.9072,-77.0369"
    }
]

states_data = [
    {
        "name": "Buenos Aires",
        "code": "BA",
        "coordinates": "-34.6118,-58.3960",
        "country_id": 1  # Argentina
    },
    {
        "name": "New York",
        "code": "NY",
        "coordinates": "40.7128,-74.0060",
        "country_id": 2  # United States
    },
    {
        "name": "California",
        "code": "CA",
        "coordinates": "36.7783,-119.4179",
        "country_id": 2  # United States
    }
]

cities_data = [
    {
        "name": "Buenos Aires",
        "code": "BUE",
        "coordinates": "-34.6118,-58.3960",
        "timezone": "America/Argentina/Buenos_Aires",
        "state_id": 1  # Buenos Aires state
    },
    {
        "name": "New York City",
        "code": "NYC",
        "coordinates": "40.7128,-74.0060",
        "timezone": "America/New_York",
        "state_id": 2  # New York state
    },
    {
        "name": "Los Angeles",
        "code": "LAX",
        "coordinates": "34.0522,-118.2437",
        "timezone": "America/Los_Angeles",
        "state_id": 3  # California state
    }
]


def insert_countries(session):
    """Insertar países"""
    print("Insertando países...")
    for country_data in countries_data:
        try:
            country_schema = CountrySchema(**country_data)
            country = Country(
                name=country_schema.name,
                code=country_schema.code,
                coordinates=country_schema.coordinates
            )
            session.add(country)
        except Exception as e:
            print(f"Error al insertar país {country_data}: {e}")
            continue
    session.commit()
    print("Países insertados correctamente.")


def insert_states(session):
    """Insertar estados"""
    print("Insertando estados...")
    for state_data in states_data:
        try:
            state_schema = StateSchema(**state_data)
            state = State(
                name=state_schema.name,
                code=state_schema.code,
                coordinates=state_schema.coordinates,
                country_id=state_schema.country_id
            )
            session.add(state)
        except Exception as e:
            print(f"Error al insertar estado {state_data}: {e}")
            continue
    session.commit()
    print("Estados insertados correctamente.")


def insert_cities(session):
    """Insertar ciudades"""
    print("Insertando ciudades...")
    for city_data in cities_data:
        try:
            city_schema = CitySchema(**city_data)
            city = City(
                name=city_schema.name,
                code=city_schema.code,
                coordinates=city_schema.coordinates,
                timezone=city_schema.timezone,
                state_id=city_schema.state_id
            )
            session.add(city)
        except Exception as e:
            print(f"Error al insertar ciudad {city_data}: {e}")
            continue
    session.commit()
    print("Ciudades insertadas correctamente.")


def main():
    BaseModel.metadata.create_all(bind=engine)
    
    session = get_session()
    try:
        insert_countries(session)
        insert_states(session)
        insert_cities(session)
        print("Todos los datos de ubicación han sido insertados correctamente.")
    except Exception as e:
        session.rollback()
        print(f"Error general: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    main() 