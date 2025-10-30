"""
Obligation rules for industry companies.
"""

from typing import List

from app.db.models.client import Client, RegimeTributario
from app.patterns.strategies.base import ObligationRule


class IndustryRule(ObligationRule):
    """
    Obligation rules for industry (indústria) companies.

    Includes IPI (Imposto sobre Produtos Industrializados).
    """

    def get_applicable_type_codes(self, client: Client) -> List[str]:
        """
        Get applicable obligation types for industry clients.

        Args:
            client: Client instance

        Returns:
            List of obligation type codes
        """
        codes = []

        # Simples Nacional
        if client.regime_tributario == RegimeTributario.SIMPLES_NACIONAL:
            codes.extend([
                "DAS_MENSAL",
                "DEFIS_ANUAL",
            ])

        # Lucro Presumido
        elif client.regime_tributario == RegimeTributario.LUCRO_PRESUMIDO:
            codes.extend([
                "DCTF_MENSAL",
                "PIS_COFINS_MENSAL",
                "EFD_CONTRIBUICOES",
                "IRPJ_TRIMESTRAL",
                "CSLL_TRIMESTRAL",
                "IPI_MENSAL",           # Imposto sobre Produtos Industrializados
            ])

        # Lucro Real
        elif client.regime_tributario == RegimeTributario.LUCRO_REAL:
            codes.extend([
                "DCTF_MENSAL",
                "PIS_COFINS_MENSAL",
                "EFD_CONTRIBUICOES",
                "IRPJ_MENSAL",
                "CSLL_MENSAL",
                "LALUR_ANUAL",
                "IPI_MENSAL",
            ])

        # MEI (indústria não pode ser MEI, mas por completude)
        elif client.regime_tributario == RegimeTributario.MEI:
            codes.extend([
                "DAS_MEI_MENSAL",
                "DASN_SIMEI_ANUAL",
            ])

        # Obrigações estaduais (ICMS e IPI)
        if client.regime_tributario != RegimeTributario.MEI:
            codes.append("SPED_FISCAL")  # SPED Fiscal (ICMS/IPI)

        # GIA (alguns estados)
        if client.uf in ["SP"]:
            codes.append("GIA_MENSAL")

        # Bloco K (específico para indústria)
        codes.append("BLOCO_K_MENSAL")  # Controle de Estoque e Produção

        # Obrigações trabalhistas e previdenciárias
        codes.extend([
            "ESOCIAL_MENSAL",
            "FGTS_MENSAL",
            "CAGED_MENSAL",
        ])

        # Obrigações anuais comuns
        codes.extend([
            "DIRPJ_ANUAL",
            "DIRF_ANUAL",
            "RAIS_ANUAL",
        ])

        return codes
