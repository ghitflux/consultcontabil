"""
Script to seed obligation types.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.db.models.obligation_type import ObligationType
from app.schemas.obligation import ObligationRecurrence

settings = get_settings()


async def seed_obligation_types():
    """Seed obligation types."""
    DATABASE_URL = str(settings.DATABASE_URL)

    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Check if types already exist using raw SQL to avoid enum conversion issues
        from sqlalchemy import text
        result = await session.execute(text("SELECT COUNT(*) FROM obligation_types"))
        count = result.scalar()

        # Check if there are obligations using these types
        result = await session.execute(text("SELECT COUNT(*) FROM obligations"))
        obligations_count = result.scalar()

        if count and count > 0:
            if obligations_count and obligations_count > 0:
                print(f"Found {count} existing obligation types with {obligations_count} obligations. Skipping seed to preserve data.")
                await engine.dispose()
                return
            else:
                print(f"Found {count} existing obligation types. Deleting to recreate with correct codes...")
                await session.execute(text("DELETE FROM obligation_types"))
                await session.commit()

        # Define obligation types - matching codes expected by strategies
        obligation_types = [
            {
                "name": "DAS",
                "code": "DAS_MENSAL",
                "description": "Documento de Arrecadação do Simples Nacional",
                "applies_to_commerce": True,
                "applies_to_service": True,
                "applies_to_industry": True,
                "applies_to_mei": True,
                "applies_to_simples": True,
                "applies_to_presumido": False,
                "applies_to_real": False,
                "recurrence": "mensal",
                "day_of_month": 20,
            },
            {
                "name": "DCTFWeb",
                "code": "DCTF_MENSAL",
                "description": "Declaração de Débitos e Créditos Tributários Federais",
                "applies_to_commerce": True,
                "applies_to_service": True,
                "applies_to_industry": True,
                "applies_to_mei": False,
                "applies_to_simples": False,
                "applies_to_presumido": True,
                "applies_to_real": True,
                "recurrence": "mensal",
                "day_of_month": 20,
            },
            {
                "name": "EFD-Contribuições",
                "code": "EFD_CONTRIBUICOES",
                "description": "Escrituração Fiscal Digital - Contribuições",
                "applies_to_commerce": True,
                "applies_to_service": True,
                "applies_to_industry": True,
                "applies_to_mei": False,
                "applies_to_simples": False,
                "applies_to_presumido": True,
                "applies_to_real": True,
                "recurrence": "mensal",
                "day_of_month": 15,
            },
            {
                "name": "ISS",
                "code": "NFS_E_MENSAL",
                "description": "Nota Fiscal de Serviços Eletrônica / ISS",
                "applies_to_commerce": False,
                "applies_to_service": True,
                "applies_to_industry": False,
                "applies_to_mei": True,
                "applies_to_simples": True,
                "applies_to_presumido": True,
                "applies_to_real": True,
                "recurrence": "mensal",
                "day_of_month": 20,
            },
            {
                "name": "FGTS",
                "code": "FGTS_MENSAL",
                "description": "Fundo de Garantia do Tempo de Serviço",
                "applies_to_commerce": True,
                "applies_to_service": True,
                "applies_to_industry": True,
                "applies_to_mei": False,
                "applies_to_simples": True,
                "applies_to_presumido": True,
                "applies_to_real": True,
                "recurrence": "mensal",
                "day_of_month": 7,
            },
            {
                "name": "INSS/eSocial",
                "code": "ESOCIAL_MENSAL",
                "description": "eSocial / Instituto Nacional do Seguro Social",
                "applies_to_commerce": True,
                "applies_to_service": True,
                "applies_to_industry": True,
                "applies_to_mei": True,
                "applies_to_simples": True,
                "applies_to_presumido": True,
                "applies_to_real": True,
                "recurrence": "mensal",
                "day_of_month": 7,
            },
            {
                "name": "ECD",
                "code": "ECD",
                "description": "Escrituração Contábil Digital",
                "applies_to_commerce": True,
                "applies_to_service": True,
                "applies_to_industry": True,
                "applies_to_mei": False,
                "applies_to_simples": False,
                "applies_to_presumido": True,
                "applies_to_real": True,
                "recurrence": "anual",
                "day_of_month": 31,
                "month_of_year": 5,
            },
            {
                "name": "ECF",
                "code": "ECF",
                "description": "Escrituração Contábil Fiscal",
                "applies_to_commerce": True,
                "applies_to_service": True,
                "applies_to_industry": True,
                "applies_to_mei": False,
                "applies_to_simples": False,
                "applies_to_presumido": True,
                "applies_to_real": True,
                "recurrence": "anual",
                "day_of_month": 31,
                "month_of_year": 7,
            },
            {
                "name": "DEFIS",
                "code": "DEFIS",
                "description": "Declaração de Informações Socioeconômicas e Fiscais",
                "applies_to_commerce": True,
                "applies_to_service": True,
                "applies_to_industry": True,
                "applies_to_mei": True,
                "applies_to_simples": True,
                "applies_to_presumido": False,
                "applies_to_real": False,
                "recurrence": "anual",
                "day_of_month": 31,
                "month_of_year": 3,
            },
        ]

        # Insert directly using SQL to avoid enum conversion issues
        from sqlalchemy import text, bindparam
        from uuid import uuid4

        for ot_data in obligation_types:
            # Use raw SQL to insert with correct enum values
            stmt = text("""
                INSERT INTO obligation_types
                (id, name, code, description, applies_to_commerce, applies_to_service,
                 applies_to_industry, applies_to_mei, applies_to_simples, applies_to_presumido,
                 applies_to_real, recurrence, day_of_month, month_of_year, is_active)
                VALUES
                (:id, :name, :code, :description, :applies_to_commerce, :applies_to_service,
                 :applies_to_industry, :applies_to_mei, :applies_to_simples, :applies_to_presumido,
                 :applies_to_real, CAST(:recurrence AS obligationrecurrence), :day_of_month, :month_of_year, :is_active)
            """)
            await session.execute(stmt, {
                "id": uuid4(),
                "name": ot_data["name"],
                "code": ot_data["code"],
                "description": ot_data["description"],
                "applies_to_commerce": ot_data["applies_to_commerce"],
                "applies_to_service": ot_data["applies_to_service"],
                "applies_to_industry": ot_data["applies_to_industry"],
                "applies_to_mei": ot_data["applies_to_mei"],
                "applies_to_simples": ot_data["applies_to_simples"],
                "applies_to_presumido": ot_data["applies_to_presumido"],
                "applies_to_real": ot_data["applies_to_real"],
                "recurrence": ot_data["recurrence"],
                "day_of_month": ot_data.get("day_of_month"),
                "month_of_year": ot_data.get("month_of_year"),
                "is_active": ot_data.get("is_active", True),
            })

        await session.commit()
        print(f"Created {len(obligation_types)} obligation types")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_obligation_types())

