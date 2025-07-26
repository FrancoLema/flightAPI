from fastapi import APIRouter

from api.v1 import v1_api_router

api_router = APIRouter()

api_router.include_router(v1_api_router, prefix="/v1/api", tags=["Flight"])
