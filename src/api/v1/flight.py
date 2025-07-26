from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.services import flight_service
from schemas.flight import FlightConnection, FlightSchema
from exceptions.flight import FlightNotFoundException

router_flight = APIRouter()

@router_flight.get("/", status_code=status.HTTP_200_OK)
async def get_flight(request: FlightSchema, service=Depends(flight_service)):
    try:
        flight = await service.get_flight(request=request)
    except FlightNotFoundException as e:
        return HTTPException(
            detail=f"Flight not found {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return FlightConnection(**flight)


