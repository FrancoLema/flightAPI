from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from src.infrastructure.db import BaseModel

class City(BaseModel):
    __tablename__ = "city"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String)
    code: Mapped[str] = Column(String, index=True)
    coordinates: Mapped[str] = Column(String)
    timezone: Mapped[str] = Column(String)
    state_id: Mapped[int] = Column(Integer, ForeignKey("state.id"))
    state = relationship("State", back_populates="cities")

class State(BaseModel):
    __tablename__ = "state"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String)
    code: Mapped[str] = Column(String, index=True)
    coordinates: Mapped[str] = Column(String)
    country_id: Mapped[int] = Column(Integer, ForeignKey("country.id"))
    country = relationship("Country", back_populates="states")
    



class Country(BaseModel):
    __tablename__ = "country"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String)
    code: Mapped[str] = Column(String, index=True)
    coordinates: Mapped[str] = Column(String)
    


