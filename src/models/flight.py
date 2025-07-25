from datetime import date, datetime

from sqlalchemy import (
    Column,
    Integer,
    Date,
    Boolean,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, relationship
from infrastructure.db import BaseModel

class FlightEvent(BaseModel):
    __tablename__ = "flight_event"

    id: Mapped[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    flight_number: Mapped[int] = Column(
        Integer,
        nullable=False,
    )
    departure_date: Mapped[date] = Column(
        Date,
        nullable=False,
    )
    departure_datetime: Mapped[datetime] = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )
    arrival_date: Mapped[date] = Column(
        Date,
        nullable=False,
    )
    arrival_datetime: Mapped[datetime] = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )
    origin_id: Mapped[int] = Column(
        Integer,
        ForeignKey("city.id"),
        nullable=False,
    )
    destination_id: Mapped[int] = Column(
        Integer,
        ForeignKey("city.id"),
        nullable=False,
    )
    active: Mapped[bool] = Column(
        Boolean,
        default=True,
        nullable=False,
    )
    origin = relationship("City", foreign_keys=[origin_id], back_populates="departures")
    destination = relationship("City", foreign_keys=[destination_id], back_populates="arrivals")

