from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from src.infrastructure.db import BaseModel

class FlightEvent(BaseModel):
    __tablename__ = "flight_event"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    flight_number: Mapped[int] = Column(Integer)
    departure_date: Mapped[datetime] = Column(DateTime(timezone=True))
    departure_datetime: Mapped[datetime] = Column(DateTime(timezone=True))
    arrival_date: Mapped[datetime] = Column(DateTime(timezone=True))
    arrival_datetime: Mapped[datetime] = Column(DateTime(timezone=True))
    origin_id: Mapped[int] = Column(Integer, ForeignKey("city.id"))
    destination_id: Mapped[int] = Column(Integer, ForeignKey("city.id"))
    active: Mapped[bool] = Column(Boolean, default=True)
    origin = relationship("City", foreign_keys=[origin_id], back_populates="departures")
    destination = relationship("City", foreign_keys=[destination_id], back_populates="arrivals")

