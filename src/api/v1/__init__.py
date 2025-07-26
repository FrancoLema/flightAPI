from fastapi import APIRouter

from api.v1.flight import router_flight

v1_api_router = APIRouter()

v1_api_router.include_router(router_flight, prefix="/flight", tags=["Flight"])
