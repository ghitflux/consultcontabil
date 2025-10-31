"""
Seed script for report templates.

Creates system templates for all report types with default configurations.

Usage:
    python -m scripts.seed_report_templates
"""

import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

from app.core.database import AsyncSessionLocal
from app.db.models.report_template import ReportTemplate
from app.db.models.report_history import ReportHistory
from app.contracts.report.enums import ReportType, ReportFormat, ReportCategory
from sqlalchemy import select


async def seed_templates():
    """Create system templates for all report types."""
    async with AsyncSessionLocal() as session:
        # Check if system templates already exist
        result = await session.execute(
            select(ReportTemplate).where(ReportTemplate.is_system == True)
        )
        existing = result.scalars().all()

        if existing:
            print(f"✅ Found {len(existing)} existing system templates. Skipping seed.")
            return

        # Define system templates
        templates_data = [
            # Financial Reports
            {
                "name": "Relatório de KPIs - Mensal",
                "report_type": ReportType.KPIS,
                "description": "KPIs consolidados do último mês",
                "default_filters": {
                    "report_type": ReportType.KPIS.value,
                    "period_start": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                    "period_end": datetime.now().strftime("%Y-%m-%d"),
                },
                "default_customizations": {
                    "include_summary": True,
                    "include_charts": True,
                },
                "is_system": True,
            },
            {
                "name": "DRE - Trimestral",
                "report_type": ReportType.DRE,
                "description": "Demonstração de Resultado do Exercício dos últimos 3 meses",
                "default_filters": {
                    "report_type": ReportType.DRE.value,
                    "period_start": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
                    "period_end": datetime.now().strftime("%Y-%m-%d"),
                },
                "default_customizations": {
                    "include_summary": True,
                    "include_charts": False,
                },
                "is_system": True,
            },
            {
                "name": "Fluxo de Caixa - Mensal",
                "report_type": ReportType.FLUXO_CAIXA,
                "description": "Fluxo de caixa do mês atual",
                "default_filters": {
                    "report_type": ReportType.FLUXO_CAIXA.value,
                    "period_start": datetime.now().replace(day=1).strftime("%Y-%m-%d"),
                    "period_end": datetime.now().strftime("%Y-%m-%d"),
                },
                "default_customizations": {
                    "include_summary": True,
                    "include_charts": True,
                },
                "is_system": True,
            },
            {
                "name": "Receita por Cliente - Anual",
                "report_type": ReportType.RECEITA_POR_CLIENTE,
                "description": "Análise de receita por cliente no ano",
                "default_filters": {
                    "report_type": ReportType.RECEITA_POR_CLIENTE.value,
                    "period_start": datetime.now().replace(month=1, day=1).strftime("%Y-%m-%d"),
                    "period_end": datetime.now().strftime("%Y-%m-%d"),
                },
                "default_customizations": {
                    "include_summary": True,
                    "include_charts": True,
                },
                "is_system": True,
            },
            {
                "name": "Despesas por Categoria - Trimestral",
                "report_type": ReportType.DESPESAS_POR_CATEGORIA,
                "description": "Análise de despesas dos últimos 3 meses",
                "default_filters": {
                    "report_type": ReportType.DESPESAS_POR_CATEGORIA.value,
                    "period_start": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
                    "period_end": datetime.now().strftime("%Y-%m-%d"),
                },
                "default_customizations": {
                    "include_summary": True,
                    "include_charts": True,
                },
                "is_system": True,
            },
            {
                "name": "Livro Caixa - Mensal",
                "report_type": ReportType.LIVRO_CAIXA,
                "description": "Livro caixa detalhado do mês",
                "default_filters": {
                    "report_type": ReportType.LIVRO_CAIXA.value,
                    "period_start": datetime.now().replace(day=1).strftime("%Y-%m-%d"),
                    "period_end": datetime.now().strftime("%Y-%m-%d"),
                },
                "default_customizations": {
                    "include_summary": False,
                    "include_charts": False,
                },
                "is_system": True,
            },
            {
                "name": "Projeção de Fluxo de Caixa - 90 Dias",
                "report_type": ReportType.PROJECAO_FLUXO_CAIXA,
                "description": "Projeção de fluxo de caixa para os próximos 90 dias",
                "default_filters": {
                    "report_type": ReportType.PROJECAO_FLUXO_CAIXA.value,
                    "period_start": datetime.now().strftime("%Y-%m-%d"),
                    "period_end": (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"),
                },
                "default_customizations": {
                    "include_summary": True,
                    "include_charts": True,
                },
                "is_system": True,
            },
            # Operational Reports
            {
                "name": "Relatório de Obrigações - Mensal",
                "report_type": ReportType.OBRIGACOES,
                "description": "Status de obrigações fiscais do mês",
                "default_filters": {
                    "report_type": ReportType.OBRIGACOES.value,
                    "period_start": datetime.now().replace(day=1).strftime("%Y-%m-%d"),
                    "period_end": datetime.now().strftime("%Y-%m-%d"),
                },
                "default_customizations": {
                    "include_summary": True,
                    "include_charts": True,
                },
                "is_system": True,
            },
            {
                "name": "Cadastro de Clientes - Completo",
                "report_type": ReportType.CLIENTES,
                "description": "Lista completa de clientes ativos",
                "default_filters": {
                    "report_type": ReportType.CLIENTES.value,
                },
                "default_customizations": {
                    "include_summary": True,
                    "include_charts": False,
                },
                "is_system": True,
            },
            {
                "name": "Licenças e Alvarás - Vencimentos",
                "report_type": ReportType.LICENCAS,
                "description": "Licenças com vencimento nos próximos 60 dias",
                "default_filters": {
                    "report_type": ReportType.LICENCAS.value,
                    "period_start": datetime.now().strftime("%Y-%m-%d"),
                    "period_end": (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
                },
                "default_customizations": {
                    "include_summary": True,
                    "include_charts": False,
                },
                "is_system": True,
            },
            {
                "name": "Auditoria - Últimos 30 Dias",
                "report_type": ReportType.AUDITORIA,
                "description": "Log de auditoria do último mês",
                "default_filters": {
                    "report_type": ReportType.AUDITORIA.value,
                    "period_start": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                    "period_end": datetime.now().strftime("%Y-%m-%d"),
                },
                "default_customizations": {
                    "include_summary": False,
                    "include_charts": False,
                },
                "is_system": True,
            },
        ]

        # Create templates
        templates = []
        for data in templates_data:
            template = ReportTemplate(
                id=uuid4(),
                **data,
                created_by_id=None,  # System template
            )
            templates.append(template)
            session.add(template)

        await session.commit()

        print(f"\n✅ Created {len(templates)} system report templates:")
        for template in templates:
            print(f"  - {template.name} ({template.report_type.value})")

        print("\n📊 Templates by category:")
        financial = [t for t in templates if t.report_type.value in [
            "kpis", "dre", "fluxo_caixa", "receita_por_cliente",
            "despesas_por_categoria", "livro_caixa", "projecao_fluxo_caixa"
        ]]
        operational = [t for t in templates if t.report_type.value in [
            "obrigacoes", "clientes", "licencas", "auditoria"
        ]]
        print(f"  💰 Financeiros: {len(financial)}")
        print(f"  ⚙️  Operacionais: {len(operational)}")


async def main():
    """Main execution."""
    print("🌱 Seeding report templates...\n")
    try:
        await seed_templates()
        print("\n✅ Seed completed successfully!")
    except Exception as e:
        print(f"\n❌ Error during seed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
