"""
Seed obligation types into database.

Run with: python -m scripts.seed_obligation_types
"""

import asyncio
import sys
from pathlib import Path
from uuid import uuid4

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select

from app.core.config import settings
# Import models in correct order to resolve relationships
from app.db.models.user import User  # noqa
from app.db.models.client import Client  # noqa
from app.db.models.obligation_type import ObligationType
from app.db.models.obligation import Obligation  # noqa
from app.db.models.obligation_event import ObligationEvent  # noqa
from app.db.models.notification import Notification  # noqa
from app.db.session import get_session_context
from app.schemas.obligation import ObligationRecurrence

# Define obligation types
OBLIGATION_TYPES = [
    # Simples Nacional
    {
        "code": "DAS_MENSAL",
        "name": "DAS - Documento de Arrecadação do Simples Nacional",
        "description": "Pagamento unificado de tributos para empresas do Simples Nacional",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_simples": True,
        "recurrence": "mensal",
        "day_of_month": 20,
    },
    {
        "code": "DEFIS_ANUAL",
        "name": "DEFIS - Declaração de Informações Socioeconômicas e Fiscais",
        "description": "Declaração anual obrigatória para empresas do Simples Nacional",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_simples": True,
        "recurrence": "anual",
        "day_of_month": 31,
        "month_of_year": 3,  # Março
    },
    # MEI
    {
        "code": "DAS_MEI_MENSAL",
        "name": "DAS MEI - Documento de Arrecadação do MEI",
        "description": "Pagamento mensal simplificado para Microempreendedor Individual",
        "applies_to_mei": True,
        "recurrence": "mensal",
        "day_of_month": 20,
    },
    {
        "code": "DASN_SIMEI_ANUAL",
        "name": "DASN-SIMEI - Declaração Anual do Simples Nacional para MEI",
        "description": "Declaração anual obrigatória para MEI",
        "applies_to_mei": True,
        "recurrence": "anual",
        "day_of_month": 31,
        "month_of_year": 5,  # Maio
    },
    # Federal - Lucro Presumido/Real
    {
        "code": "DCTF_MENSAL",
        "name": "DCTF - Declaração de Débitos e Créditos Tributários Federais",
        "description": "Declaração mensal de tributos federais",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_presumido": True,
        "applies_to_real": True,
        "recurrence": "mensal",
        "day_of_month": 15,
    },
    {
        "code": "PIS_COFINS_MENSAL",
        "name": "PIS/COFINS - Contribuições Sociais",
        "description": "Pagamento mensal de PIS e COFINS",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_presumido": True,
        "applies_to_real": True,
        "recurrence": "mensal",
        "day_of_month": 25,
    },
    {
        "code": "EFD_CONTRIBUICOES",
        "name": "EFD-Contribuições - Escrituração Fiscal Digital",
        "description": "Escrituração digital de PIS e COFINS",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_presumido": True,
        "applies_to_real": True,
        "recurrence": "mensal",
        "day_of_month": 10,
    },
    {
        "code": "IRPJ_TRIMESTRAL",
        "name": "IRPJ - Imposto de Renda Pessoa Jurídica (Trimestral)",
        "description": "Pagamento trimestral de IRPJ para Lucro Presumido",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_presumido": True,
        "recurrence": "trimestral",
        "day_of_month": 31,
    },
    {
        "code": "CSLL_TRIMESTRAL",
        "name": "CSLL - Contribuição Social sobre o Lucro Líquido (Trimestral)",
        "description": "Pagamento trimestral de CSLL para Lucro Presumido",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_presumido": True,
        "recurrence": "trimestral",
        "day_of_month": 31,
    },
    {
        "code": "IRPJ_MENSAL",
        "name": "IRPJ - Imposto de Renda Pessoa Jurídica (Mensal)",
        "description": "Pagamento mensal de IRPJ estimativa para Lucro Real",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_real": True,
        "recurrence": "mensal",
        "day_of_month": 31,
    },
    {
        "code": "CSLL_MENSAL",
        "name": "CSLL - Contribuição Social sobre o Lucro Líquido (Mensal)",
        "description": "Pagamento mensal de CSLL estimativa para Lucro Real",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_real": True,
        "recurrence": "mensal",
        "day_of_month": 31,
    },
    # Estadual
    {
        "code": "SPED_FISCAL",
        "name": "SPED Fiscal - Escrituração Fiscal Digital",
        "description": "Escrituração digital de ICMS e IPI",
        "applies_to_commerce": True,
        "applies_to_industry": True,
        "applies_to_presumido": True,
        "applies_to_real": True,
        "recurrence": "mensal",
        "day_of_month": 20,
    },
    {
        "code": "GIA_MENSAL",
        "name": "GIA - Guia de Informação e Apuração do ICMS",
        "description": "Declaração mensal de ICMS (SP)",
        "applies_to_commerce": True,
        "applies_to_industry": True,
        "applies_to_presumido": True,
        "applies_to_real": True,
        "recurrence": "mensal",
        "day_of_month": 10,
    },
    # Municipal
    {
        "code": "NFS_E_MENSAL",
        "name": "NFS-e - Nota Fiscal de Serviços Eletrônica",
        "description": "Emissão e declaração de notas fiscais de serviço",
        "applies_to_service": True,
        "applies_to_presumido": True,
        "applies_to_real": True,
        "recurrence": "mensal",
        "day_of_month": 5,
    },
    {
        "code": "DMS_MENSAL",
        "name": "DMS - Declaração Mensal de Serviços",
        "description": "Declaração mensal de ISS",
        "applies_to_service": True,
        "applies_to_presumido": True,
        "applies_to_real": True,
        "recurrence": "mensal",
        "day_of_month": 10,
    },
    # Trabalhistas
    {
        "code": "ESOCIAL_MENSAL",
        "name": "eSocial - Sistema de Escrituração Digital",
        "description": "Envio de informações trabalhistas, previdenciárias e fiscais",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_simples": True,
        "applies_to_presumido": True,
        "applies_to_real": True,
        "recurrence": "mensal",
        "day_of_month": 15,
    },
    {
        "code": "FGTS_MENSAL",
        "name": "FGTS - Fundo de Garantia do Tempo de Serviço",
        "description": "Recolhimento mensal de FGTS",
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
        "code": "CAGED_MENSAL",
        "name": "CAGED - Cadastro Geral de Empregados e Desempregados",
        "description": "Declaração de admissões e demissões",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_simples": True,
        "applies_to_presumido": True,
        "applies_to_real": True,
        "recurrence": "mensal",
        "day_of_month": 7,
    },
    # Anuais
    {
        "code": "DIRPJ_ANUAL",
        "name": "DIRPJ - Declaração de Informações Econômico-Fiscais da PJ",
        "description": "Declaração anual de informações fiscais",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_presumido": True,
        "applies_to_real": True,
        "recurrence": "anual",
        "day_of_month": 31,
        "month_of_year": 7,  # Julho
    },
    {
        "code": "DIRF_ANUAL",
        "name": "DIRF - Declaração do Imposto de Renda Retido na Fonte",
        "description": "Declaração anual de IR retido na fonte",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_simples": True,
        "applies_to_presumido": True,
        "applies_to_real": True,
        "recurrence": "anual",
        "day_of_month": 28,
        "month_of_year": 2,  # Fevereiro
    },
    {
        "code": "RAIS_ANUAL",
        "name": "RAIS - Relação Anual de Informações Sociais",
        "description": "Declaração anual de informações trabalhistas",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_simples": True,
        "applies_to_presumido": True,
        "applies_to_real": True,
        "recurrence": "anual",
        "day_of_month": 31,
        "month_of_year": 3,  # Março
    },
    # Específicos
    {
        "code": "IPI_MENSAL",
        "name": "IPI - Imposto sobre Produtos Industrializados",
        "description": "Pagamento mensal de IPI",
        "applies_to_industry": True,
        "applies_to_presumido": True,
        "applies_to_real": True,
        "recurrence": "mensal",
        "day_of_month": 25,
    },
    {
        "code": "BLOCO_K_MENSAL",
        "name": "Bloco K - Controle de Estoque e Produção",
        "description": "Escrituração de estoque e produção industrial",
        "applies_to_industry": True,
        "applies_to_presumido": True,
        "applies_to_real": True,
        "recurrence": "mensal",
        "day_of_month": 20,
    },
    {
        "code": "LALUR_ANUAL",
        "name": "LALUR - Livro de Apuração do Lucro Real",
        "description": "Livro fiscal anual para Lucro Real",
        "applies_to_commerce": True,
        "applies_to_service": True,
        "applies_to_industry": True,
        "applies_to_real": True,
        "recurrence": "anual",
        "day_of_month": 31,
        "month_of_year": 12,  # Dezembro
    },
]


async def seed_obligation_types():
    """Seed obligation types into database."""
    try:
        async with get_session_context() as db:
            print("Seeding obligation types...")

            # Check existing
            result = await db.execute(select(ObligationType))
            existing = result.scalars().all()
            existing_codes = {ob.code for ob in existing}

            # Insert new types
            created_count = 0
            updated_count = 0

            for type_data in OBLIGATION_TYPES:
                code = type_data["code"]

                if code in existing_codes:
                    print(f"  Skipping {code} (already exists)")
                    continue

                # Create new
                ob_type = ObligationType(
                    id=uuid4(),
                    **type_data
                )
                db.add(ob_type)
                created_count += 1
                print(f"  Created {code}")

            # Flush to ensure data is sent to database
            await db.flush()

            print(f"\nSeed complete!")
            print(f"  Created: {created_count}")
            print(f"  Existing: {len(existing_codes)}")
            print(f"  Total: {created_count + len(existing_codes)}")
    except Exception as e:
        print(f"\nERROR during seed: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(seed_obligation_types())
