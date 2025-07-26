import sys
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.flight import FlightEvent
from schemas.flight import FlightSchema
from config.settings import BaseConfig  

DATABASE_URL = BaseConfig.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

flights_json_data = [
    {
        "date": "2024-07-01",
        "from": "EZE",
        "to": "JFK"
    },
    {
        "date": "2024-07-02",
        "from": "JFK",
        "to": "EZE"
    },
    {
        "date": "2024-07-03",
        "from": "EZE",
        "to": "MIA"
    }
]


def main():
    data = flights_json_data

    session = SessionLocal()
    try:
        for entry in data:
            try:
                flight_data = FlightSchema(**entry)
            except Exception as e:
                print(f"Error de validación en {entry}: {e}")
                continue
            flight = FlightEvent(
                date=flight_data.date,
                from_=flight_data.from_,
                to=flight_data.to
            )
            session.add(flight)
        session.commit()
        print("Datos insertados correctamente.")
    except Exception as e:
        session.rollback()
        print(f"Error al insertar datos: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main() 