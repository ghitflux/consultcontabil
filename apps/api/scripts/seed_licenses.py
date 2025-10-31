"""
Seed script for licenses, CNAEs, and municipal registrations.
"""

import asyncio
from datetime import date, timedelta
from uuid import UUID

from app.core.database import db_manager
from app.db.models.cnae import Cnae
from app.db.models.license import License
from app.db.models.municipal_registration import MunicipalRegistration
from app.db.models.client import Client
from app.db.repositories.client import ClientRepository
from app.schemas.cnae import CnaeType
from app.schemas.license import LicenseStatus, LicenseType
from app.schemas.municipal_registration import MunicipalRegistrationStatus, StateCode


async def seed_licenses() -> None:
    """Seed licenses, CNAEs, and municipal registrations."""
    print("🌱 Starting license data seed...")

    async for session in db_manager.get_session():
        try:
            # Get clients
            client_repo = ClientRepository(session)
            clients = await client_repo.list_all(limit=10)

            if not clients:
                print("❌ No clients found. Please seed clients first.")
                return

            print(f"📋 Found {len(clients)} clients")

            # Seed CNAEs
            print("\n📝 Seeding CNAEs...")
            cnae_count = 0
            for client in clients[:5]:  # Only first 5 clients
                # Primary CNAE
                primary_cnae = Cnae(
                    client_id=client.id,
                    cnae_code="6201-5/00",  # Desenvolvimento de programas de computador
                    description="Desenvolvimento de programas de computador sob medida",
                    cnae_type=CnaeType.PRINCIPAL,
                    is_active=True,
                )
                session.add(primary_cnae)
                cnae_count += 1

                # Secondary CNAEs
                secondary_cnaes = [
                    ("6202-3/00", "Desenvolvimento e licenciamento de programas de computador customizáveis"),
                    ("6319-4/00", "Processamento de dados, hospedagem na internet e atividades relacionadas"),
                ]
                for code, desc in secondary_cnaes:
                    cnae = Cnae(
                        client_id=client.id,
                        cnae_code=code,
                        description=desc,
                        cnae_type=CnaeType.SECUNDARIO,
                        is_active=True,
                    )
                    session.add(cnae)
                    cnae_count += 1

            await session.commit()
            print(f"✅ Created {cnae_count} CNAEs")

            # Seed Licenses
            print("\n📜 Seeding Licenses...")
            today = date.today()
            license_types = [
                LicenseType.ALVARA_FUNCIONAMENTO,
                LicenseType.CERTIFICADO_DIGITAL,
                LicenseType.LICENCA_SANITARIA,
                LicenseType.LICENCA_BOMBEIROS,
            ]

            license_count = 0
            for i, client in enumerate(clients[:5]):
                # Create 3 licenses per client
                for j, license_type in enumerate(license_types[:3]):
                    expiration_days = [30, 60, 90, -10, -30][(i * 3 + j) % 5]  # Mix of expiring and expired
                    expiration_date = today + timedelta(days=expiration_days)

                    # Determine status
                    if expiration_days < 0:
                        status = LicenseStatus.VENCIDA
                    elif expiration_days <= 30:
                        status = LicenseStatus.PENDENTE_RENOVACAO
                    else:
                        status = LicenseStatus.ATIVA

                    license_obj = License(
                        client_id=client.id,
                        license_type=license_type,
                        registration_number=f"LIC-{i+1:03d}-{j+1:02d}",
                        issuing_authority=f"Órgão Emissor {i+1}",
                        issue_date=today - timedelta(days=365),
                        expiration_date=expiration_date if j < 2 else None,  # Some without expiration
                        status=status,
                        notes=f"Licença de exemplo para {client.razao_social}",
                    )
                    session.add(license_obj)
                    license_count += 1

            await session.commit()
            print(f"✅ Created {license_count} licenses")

            # Seed Municipal Registrations
            print("\n🏛️ Seeding Municipal Registrations...")
            states = [StateCode.SP, StateCode.RJ, StateCode.MG]
            cities = ["São Paulo", "Rio de Janeiro", "Belo Horizonte"]

            registration_count = 0
            for i, client in enumerate(clients[:5]):
                state = states[i % len(states)]
                city = cities[i % len(cities)]

                registration = MunicipalRegistration(
                    client_id=client.id,
                    city=city,
                    state=state,
                    registration_number=f"IM-{i+1:05d}",
                    issue_date=today - timedelta(days=180),
                    status=MunicipalRegistrationStatus.ATIVA,
                    notes=f"Inscrição municipal em {city}, {state.value}",
                )
                session.add(registration)
                registration_count += 1

            await session.commit()
            print(f"✅ Created {registration_count} municipal registrations")

            print("\n✅ License data seed completed!")
            break

        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding license data: {e}")
            raise
        finally:
            break


if __name__ == "__main__":
    asyncio.run(seed_licenses())

