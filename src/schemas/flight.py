from pydantic import BaseModel, Field
from datetime import date, datetime


class FlightSchema(BaseModel):
    date: date
    from_: str = Field(alias="from")
    to: str

class FlightCircuit(BaseModel):
    flight_number: str
    from_: str = Field(alias="from")
    to: str
    departure_time: datetime
    arrival_time: datetime

class FlightConnection(BaseModel):
    connections: int
    path: list[FlightCircuit]
    
    