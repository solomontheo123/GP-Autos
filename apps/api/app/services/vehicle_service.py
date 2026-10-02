from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ListingStatus
from app.models.vehicle import VehicleListing


async def list_active_vehicles(session: AsyncSession) -> list[VehicleListing]:
    result = await session.scalars(
        select(VehicleListing)
        .where(VehicleListing.status == ListingStatus.ACTIVE, VehicleListing.stock > 0)
        .order_by(VehicleListing.created_at.desc())
    )
    return list(result)


async def get_vehicle_by_id(session: AsyncSession, vehicle_id: str) -> VehicleListing | None:
    return await session.scalar(select(VehicleListing).where(VehicleListing.id == vehicle_id))


async def get_vehicle_by_slug(session: AsyncSession, slug: str) -> VehicleListing | None:
    return await session.scalar(select(VehicleListing).where(VehicleListing.slug == slug))
