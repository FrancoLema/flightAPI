from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from infrastructure.db import BaseModel


class City(BaseModel):
    __tablename__ = "city"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False)
    code: Mapped[str] = Column(String, index=True, nullable=False)
    coordinates: Mapped[str] = Column(String, nullable=False)
    timezone: Mapped[str] = Column(String, nullable=False)
    state_id: Mapped[int] = Column(Integer, ForeignKey("state.id"), nullable=False)
    state = relationship("State", back_populates="cities")


class State(BaseModel):
    __tablename__ = "state"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False)
    code: Mapped[str] = Column(String, index=True, nullable=False)
    coordinates: Mapped[str] = Column(String, nullable=False)
    country_id: Mapped[int] = Column(Integer, ForeignKey("country.id"), nullable=False)
    country = relationship("Country", back_populates="states")


class Country(BaseModel):
    __tablename__ = "country"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False)
    code: Mapped[str] = Column(String, index=True, nullable=False)
    coordinates: Mapped[str] = Column(String, nullable=False)
