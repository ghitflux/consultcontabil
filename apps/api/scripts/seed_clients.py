"""
Script to seed clients.
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
from app.db.models.client import Client, ClientStatus, RegimeTributario, TipoEmpresa

settings = get_settings()


async def seed_clients():
    """Seed clients."""
    DATABASE_URL = str(settings.DATABASE_URL)

    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Check if clients already exist
        from sqlalchemy import select, func
        result = await session.execute(select(func.count()).select_from(Client))
        count = result.scalar()

        if count and count >= 15:  # We'll create 15 clients
            print(f"Found {count} existing clients. Skipping seed.")
            await engine.dispose()
            return

        # Sample clients based on the image
        clients_data = [
            {
                "razao_social": "Tech Solutions Ltda",
                "nome_fantasia": "Tech Solutions",
                "cnpj": "12.345.678/0001-90",
                "email": "contato@techsolutions.com.br",
                "telefone": "(11) 3456-7890",
                "celular": "(11) 98765-4321",
                "cep": "01310-100",
                "logradouro": "Av. Paulista",
                "numero": "1000",
                "bairro": "Bela Vista",
                "cidade": "São Paulo",
                "uf": "SP",
                "honorarios_mensais": 1500.00,
                "dia_vencimento": 10,
                "servicos": ["fiscal", "contabil", "pessoal"],
                "valor_fiscal": 800.00,
                "valor_contabil": 500.00,
                "valor_pessoal": 200.00,
                "regime_tributario": RegimeTributario.LUCRO_PRESUMIDO,
                "tipo_empresa": TipoEmpresa.SERVICO,
                "status": ClientStatus.ATIVO,
                "data_abertura": date(2020, 1, 15),
            },
            {
                "razao_social": "Comércio ABC S.A.",
                "nome_fantasia": "ABC Comércio",
                "cnpj": "98.765.432/0001-10",
                "email": "contato@abccomercio.com.br",
                "telefone": "(21) 2345-6789",
                "celular": "(21) 99876-5432",
                "cep": "20040-020",
                "logradouro": "Rua do Ouvidor",
                "numero": "50",
                "bairro": "Centro",
                "cidade": "Rio de Janeiro",
                "uf": "RJ",
                "honorarios_mensais": 2000.00,
                "dia_vencimento": 15,
                "servicos": ["fiscal", "contabil"],
                "valor_fiscal": 1200.00,
                "valor_contabil": 800.00,
                "valor_pessoal": 0.00,
                "regime_tributario": RegimeTributario.SIMPLES_NACIONAL,
                "tipo_empresa": TipoEmpresa.COMERCIO,
                "status": ClientStatus.ATIVO,
                "data_abertura": date(2019, 5, 20),
            },
            {
                "razao_social": "Indústria XYZ Ltda",
                "nome_fantasia": "XYZ Indústria",
                "cnpj": "11.222.333/0001-44",
                "email": "contato@xyzindustria.com.br",
                "telefone": "(47) 3456-7890",
                "celular": "(47) 98765-4321",
                "cep": "89010-001",
                "logradouro": "Rua XV de Novembro",
                "numero": "1234",
                "bairro": "Centro",
                "cidade": "Blumenau",
                "uf": "SC",
                "honorarios_mensais": 3000.00,
                "dia_vencimento": 5,
                "servicos": ["fiscal", "contabil", "pessoal"],
                "valor_fiscal": 1500.00,
                "valor_contabil": 1000.00,
                "valor_pessoal": 500.00,
                "regime_tributario": RegimeTributario.LUCRO_REAL,
                "tipo_empresa": TipoEmpresa.INDUSTRIA,
                "status": ClientStatus.ATIVO,
                "data_abertura": date(2018, 3, 10),
            },
        ]

        # Add more sample clients
        for i in range(4, 15):
            clients_data.append({
                "razao_social": f"Empresa {chr(64 + i)} Ltda",
                "nome_fantasia": f"Empresa {chr(64 + i)}",
                "cnpj": f"{i:02d}.{i+10:03d}.{i+20:03d}/0001-{i+30:02d}",
                "email": f"contato@empresa{chr(96+i)}.com.br",
                "telefone": f"(11) {3000+i}-{7000+i}",
                "honorarios_mensais": 1000.00 + (i * 100),
                "dia_vencimento": (i % 28) + 1,
                "servicos": ["fiscal", "contabil"],
                "valor_fiscal": 500.00 + (i * 50),
                "valor_contabil": 300.00 + (i * 30),
                "valor_pessoal": 200.00 + (i * 20),
                "regime_tributario": RegimeTributario.SIMPLES_NACIONAL if i % 2 == 0 else RegimeTributario.LUCRO_PRESUMIDO,
                "tipo_empresa": TipoEmpresa.COMERCIO if i % 3 == 0 else TipoEmpresa.SERVICO,
                "status": ClientStatus.ATIVO,
                "data_abertura": date(2020 + (i % 3), (i % 12) + 1, (i % 28) + 1),
            })

        for client_data in clients_data:
            client = Client(**client_data)
            session.add(client)

        await session.commit()
        print(f"Created {len(clients_data)} clients")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_clients())

