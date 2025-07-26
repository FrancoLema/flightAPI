from pydantic import BaseModel, Field
from typing import Optional


class CountrySchema(BaseModel):
    name: str
    code: str
    coordinates: str


class StateSchema(BaseModel):
    name: str
    code: str
    coordinates: str
    country_id: int


class CitySchema(BaseModel):
    name: str
    code: str
    coordinates: str
    timezone: str
    state_id: int


class CountryResponse(BaseModel):
    id: int
    name: str
    code: str
    coordinates: str


class StateResponse(BaseModel):
    id: int
    name: str
    code: str
    coordinates: str
    country_id: int


class CityResponse(BaseModel):
    id: int
    name: str
    code: str
    coordinates: str
    timezone: str
    state_id: int 