"""
Seed script to create initial clients for testing.
Run with: python -m scripts.seed_clients
"""

import asyncio
import sys
from datetime import date
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select

from app.core.database import Base, db_manager
from app.db.models.client import Client, ClientStatus, RegimeTributario, TipoEmpresa


async def seed_clients() -> None:
    """Create seed clients for testing."""
    print("[*] Starting client seed...")

    # Create tables if they don't exist
    async with db_manager.write_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[OK] Tables created/verified")

    # Clients to create
    seed_clients_data = [
        {
            "razao_social": "Comercial Silva e Filhos LTDA",
            "nome_fantasia": "Silva Comércio",
            "cnpj": "12.345.678/0001-90",
            "inscricao_estadual": "123.456.789.123",
            "email": "contato@silvacomercio.com",
            "telefone": "(11) 3333-4444",
            "celular": "(11) 98888-7777",
            "cep": "01310-100",
            "logradouro": "Avenida Paulista",
            "numero": "1000",
            "bairro": "Bela Vista",
            "cidade": "São Paulo",
            "uf": "SP",
            "honorarios_mensais": 1500.00,
            "dia_vencimento": 10,
            "regime_tributario": RegimeTributario.SIMPLES_NACIONAL,
            "tipo_empresa": TipoEmpresa.COMERCIO,
            "data_abertura": date(2020, 1, 15),
            "responsavel_nome": "João Silva",
            "responsavel_email": "joao@silvacomercio.com",
            "status": ClientStatus.ATIVO,
        },
        {
            "razao_social": "Tecnologia Avançada Sistemas LTDA",
            "nome_fantasia": "TechSys",
            "cnpj": "98.765.432/0001-10",
            "email": "contato@techsys.com.br",
            "telefone": "(11) 4444-5555",
            "honorarios_mensais": 2500.00,
            "dia_vencimento": 5,
            "regime_tributario": RegimeTributario.LUCRO_PRESUMIDO,
            "tipo_empresa": TipoEmpresa.SERVICO,
            "status": ClientStatus.ATIVO,
        },
        {
            "razao_social": "Indústria Metalúrgica Forte SA",
            "nome_fantasia": "Metal Forte",
            "cnpj": "11.222.333/0001-44",
            "email": "financeiro@metalforte.ind.br",
            "honorarios_mensais": 5000.00,
            "dia_vencimento": 15,
            "regime_tributario": RegimeTributario.LUCRO_REAL,
            "tipo_empresa": TipoEmpresa.INDUSTRIA,
            "status": ClientStatus.ATIVO,
        },
        {
            "razao_social": "Consultoria Empresarial Santos MEI",
            "nome_fantasia": "Santos Consultoria",
            "cnpj": "33.444.555/0001-66",
            "email": "maria@santosconsultoria.com",
            "honorarios_mensais": 500.00,
            "dia_vencimento": 20,
            "regime_tributario": RegimeTributario.MEI,
            "tipo_empresa": TipoEmpresa.SERVICO,
            "status": ClientStatus.ATIVO,
        },
        {
            "razao_social": "Empresa Teste Pendente LTDA",
            "nome_fantasia": "Teste Pendente",
            "cnpj": "55.666.777/0001-88",
            "email": "teste@pendente.com",
            "honorarios_mensais": 1000.00,
            "dia_vencimento": 25,
            "regime_tributario": RegimeTributario.SIMPLES_NACIONAL,
            "tipo_empresa": TipoEmpresa.COMERCIO,
            "status": ClientStatus.PENDENTE,
        },
        {
            "razao_social": "Antiga Empresa Inativa LTDA",
            "nome_fantasia": "Empresa Inativa",
            "cnpj": "77.888.999/0001-00",
            "email": "inativa@empresa.com",
            "honorarios_mensais": 800.00,
            "dia_vencimento": 30,
            "regime_tributario": RegimeTributario.SIMPLES_NACIONAL,
            "tipo_empresa": TipoEmpresa.MISTO,
            "status": ClientStatus.INATIVO,
        },
    ]

    # Insert clients
    async with db_manager.session_factory() as session:
        for client_data in seed_clients_data:
            # Check if client already exists
            result = await session.execute(
                select(Client).where(Client.cnpj == client_data["cnpj"])
            )
            existing_client = result.scalar_one_or_none()

            if existing_client:
                print(f"[SKIP] Client {client_data['cnpj']} already exists, skipping...")
                continue

            # Create new client
            client = Client(**client_data)
            session.add(client)
            print(f"[OK] Created client: {client_data['razao_social']} (CNPJ: {client_data['cnpj']})")

        await session.commit()

    print("\n[SUCCESS] Seed completed successfully!")
    print(f"\n[INFO] {len(seed_clients_data)} clients created")


async def main() -> None:
    """Main function."""
    try:
        await seed_clients()
    except Exception as e:
        print(f"\n[ERROR] Error during seed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        # Close database connections
        await db_manager.close()


if __name__ == "__main__":
    asyncio.run(main())
