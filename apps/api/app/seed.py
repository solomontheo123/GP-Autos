import asyncio
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select

from app.db.session import SessionLocal, engine
from app.models.vehicle import VehicleListing

SEED_VEHICLES = [
    {
        "id": "10000000-0000-4000-8000-000000000001",
        "slug": "2021-toyota-camry-xse",
        "title": "2021 Toyota Camry XSE",
        "make": "Toyota",
        "model": "Camry XSE",
        "year": 2021,
        "mileage": 28400,
        "condition": "Foreign used",
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "body_type": "Sedan",
        "location": "Lekki, Lagos",
        "description": (
            "A refined Camry XSE with a composed ride, spacious cabin and confident "
            "performance. Well maintained with a clear service history and premium interior "
            "finishes."
        ),
        "price": "48500000",
        "image_url": "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?auto=format&fit=crop&w=1200&q=85",
    },
    {
        "id": "10000000-0000-4000-8000-000000000002",
        "slug": "2020-mercedes-benz-c300",
        "title": "2020 Mercedes-Benz C300",
        "make": "Mercedes-Benz",
        "model": "C300",
        "year": 2020,
        "mileage": 31200,
        "condition": "Foreign used",
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "body_type": "Sedan",
        "location": "Victoria Island, Lagos",
        "description": (
            "A polished C-Class with the comfort and technology expected from Mercedes-Benz. "
            "Carefully kept, beautifully presented and ready for its next owner."
        ),
        "price": "64500000",
        "image_url": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1200&q=85",
    },
    {
        "id": "10000000-0000-4000-8000-000000000003",
        "slug": "2019-lexus-rx-350",
        "title": "2019 Lexus RX 350",
        "make": "Lexus",
        "model": "RX 350",
        "year": 2019,
        "mileage": 39800,
        "condition": "Foreign used",
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "body_type": "SUV",
        "location": "Maitama, Abuja",
        "description": (
            "A luxury SUV known for quiet comfort and dependable character. This RX 350 "
            "pairs a premium cabin with the versatility of a confident everyday drive."
        ),
        "price": "57200000",
        "image_url": "https://images.unsplash.com/photo-1606016159991-dfe4f2746ad5?auto=format&fit=crop&w=1200&q=85",
    },
    {
        "id": "10000000-0000-4000-8000-000000000004",
        "slug": "2022-honda-accord-sport",
        "title": "2022 Honda Accord Sport",
        "make": "Honda",
        "model": "Accord Sport",
        "year": 2022,
        "mileage": 19600,
        "condition": "Foreign used",
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "body_type": "Sedan",
        "location": "Ikeja, Lagos",
        "description": (
            "A modern Accord Sport with responsive handling, generous space and a well-appointed "
            "interior. Low mileage and excellent presentation make this a compelling daily driver."
        ),
        "price": "53900000",
        "image_url": "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?auto=format&fit=crop&w=1200&q=85",
    },
    {
        "id": "10000000-0000-4000-8000-000000000005",
        "slug": "2021-hyundai-tucson-limited",
        "title": "2021 Hyundai Tucson Limited",
        "make": "Hyundai",
        "model": "Tucson Limited",
        "year": 2021,
        "mileage": 25800,
        "condition": "Foreign used",
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "body_type": "SUV",
        "location": "GRA, Port Harcourt",
        "description": (
            "A practical, contemporary SUV with a comfortable cabin and flexible cargo space. The "
            "Tucson Limited is an easy fit for busy weekdays and open-road weekends alike."
        ),
        "price": "44800000",
        "image_url": "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=1200&q=85",
    },
    {
        "id": "10000000-0000-4000-8000-000000000006",
        "slug": "2020-kia-sportage-ex",
        "title": "2020 Kia Sportage EX",
        "make": "Kia",
        "model": "Sportage EX",
        "year": 2020,
        "mileage": 34500,
        "condition": "Foreign used",
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "body_type": "SUV",
        "location": "Yaba, Lagos",
        "description": (
            "A versatile compact SUV with a confident driving position, useful equipment and a "
            "well-kept interior. Ready to make family travel simpler."
        ),
        "price": "38600000",
        "image_url": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=1200&q=85",
    },
]


async def seed() -> None:
    async with SessionLocal() as session:
        for record in SEED_VEHICLES:
            vehicle_id = UUID(str(record["id"]))
            existing = await session.scalar(
                select(VehicleListing).where(VehicleListing.id == vehicle_id)
            )
            values = {
                **record,
                "id": vehicle_id,
                "price": Decimal(str(record["price"])),
                "stock": 1,
            }
            if existing is None:
                session.add(VehicleListing(**values))
            else:
                for field, value in values.items():
                    setattr(existing, field, value)
        await session.commit()
    await engine.dispose()


def main() -> None:
    asyncio.run(seed())


if __name__ == "__main__":
    main()
