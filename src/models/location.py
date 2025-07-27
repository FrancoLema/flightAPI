from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from infrastructure.db import BaseModel


class Country(BaseModel):
    __tablename__ = "country"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False)
    code: Mapped[str] = Column(String, index=True, nullable=False, unique=True)
    coordinates: Mapped[str] = Column(String, nullable=False)

    states = relationship("State", back_populates="country")


class State(BaseModel):
    __tablename__ = "state"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False)
    code: Mapped[str] = Column(String, index=True, nullable=False, unique=True)
    coordinates: Mapped[str] = Column(String, nullable=False)
    country_id: Mapped[int] = Column(Integer, ForeignKey("country.id"), nullable=False)

    country = relationship("Country", back_populates="states")
    cities = relationship("City", back_populates="state")


class City(BaseModel):
    __tablename__ = "city"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False)
    code: Mapped[str] = Column(String, index=True, nullable=False, unique=True)
    coordinates: Mapped[str] = Column(String, nullable=False)
    timezone: Mapped[str] = Column(String, nullable=False)
    state_id: Mapped[int] = Column(Integer, ForeignKey("state.id"), nullable=False)

    state = relationship("State", back_populates="cities")
    # Flight Events
    departures = relationship(
        "FlightEvent", foreign_keys="FlightEvent.origin_id", back_populates="origin"
    )
    arrivals = relationship(
        "FlightEvent",
        foreign_keys="FlightEvent.destination_id",
        back_populates="destination",
    )
