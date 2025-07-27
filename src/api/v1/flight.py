from fastapi import APIRouter, Depends, HTTPException, status, Query
from dependencies.services import flight_service
from exceptions.flight import FlightNotFoundException
from datetime import date

router_flight = APIRouter()


@router_flight.get("/", status_code=status.HTTP_200_OK)
async def get_flight(
    date: date = Query(..., description="Fecha del vuelo (YYYY-MM-DD)"),
    origin: str = Query(..., alias="from", description="Código de la ciudad de origen"),
    destiny: str = Query(..., alias="to", description="Código de la ciudad de destino"),
    service=Depends(flight_service),
):
    try:
        flight = await service.search_flight(date=date, origin=origin, destiny=destiny)
    except ValueError as e:
        raise HTTPException(
            detail=f"{str(e)}",
            status_code=status.HTTP_400_BAD_REQUEST,
        ) from e
    except FlightNotFoundException as e:
        raise HTTPException(
            detail=f"{str(e)}",
            status_code=status.HTTP_404_NOT_FOUND,
        ) from e
    except Exception as e:
        raise HTTPException(
            detail=f"{str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e
    return flight
