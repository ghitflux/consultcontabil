"""
Script to seed obligations for clients.
"""

import asyncio
import sys
from pathlib import Path
from datetime import date

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.db.models.client import Client
from app.services.obligation.generator import ObligationGenerator

settings = get_settings()


async def seed_obligations():
    """Generate obligations for all active clients for current month and previous month."""
    DATABASE_URL = str(settings.DATABASE_URL)

    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Get all active clients
        from sqlalchemy import select
        result = await session.execute(select(Client).where(Client.status == "ativo"))
        clients = result.scalars().all()

        if not clients:
            print("No active clients found. Please run seed_clients.py first.")
            await engine.dispose()
            return

        generator = ObligationGenerator(session)
        current_date = date.today()
        current_year = current_date.year
        current_month = current_date.month

        # Generate for current month
        print(f"Generating obligations for {current_year}/{current_month:02d}...")
        stats = await generator.generate_for_all_clients(
            year=current_year,
            month=current_month,
        )
        print(f"Generated {stats['total_obligations']} obligations for {stats['total_clients']} clients")

        # Generate for previous month
        prev_month = current_month - 1
        prev_year = current_year
        if prev_month == 0:
            prev_month = 12
            prev_year -= 1

        print(f"Generating obligations for {prev_year}/{prev_month:02d}...")
        stats = await generator.generate_for_all_clients(
            year=prev_year,
            month=prev_month,
        )
        print(f"Generated {stats['total_obligations']} obligations for {stats['total_clients']} clients")

        await session.commit()

    await engine.dispose()
    print("Obligations seeding completed")


if __name__ == "__main__":
    asyncio.run(seed_obligations())

