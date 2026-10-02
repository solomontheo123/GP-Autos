from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.vehicle import VehicleListingRead
from app.services.vehicle_service import (
    get_vehicle_by_id,
    get_vehicle_by_slug,
    list_active_vehicles,
)

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])


@router.get("", response_model=list[VehicleListingRead])
async def list_vehicles(session: AsyncSession = Depends(get_session)) -> list[VehicleListingRead]:
    return [
        VehicleListingRead.model_validate(vehicle)
        for vehicle in await list_active_vehicles(session)
    ]


@router.get("/slug/{slug}", response_model=VehicleListingRead)
async def read_vehicle_by_slug(
    slug: str, session: AsyncSession = Depends(get_session)
) -> VehicleListingRead:
    vehicle = await get_vehicle_by_slug(session, slug)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle listing not found"
        )
    return VehicleListingRead.model_validate(vehicle)


@router.get("/{vehicle_id}", response_model=VehicleListingRead)
async def read_vehicle(
    vehicle_id: str, session: AsyncSession = Depends(get_session)
) -> VehicleListingRead:
    vehicle = await get_vehicle_by_id(session, vehicle_id)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle listing not found"
        )
    return VehicleListingRead.model_validate(vehicle)
