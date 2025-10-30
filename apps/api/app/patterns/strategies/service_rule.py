"""
Obligation rules for service companies.
"""

from typing import List

from app.db.models.client import Client, RegimeTributario
from app.patterns.strategies.base import ObligationRule


class ServiceRule(ObligationRule):
    """
    Obligation rules for service (serviço) companies.

    Main difference from commerce: ISS instead of ICMS.
    """

    def get_applicable_type_codes(self, client: Client) -> List[str]:
        """
        Get applicable obligation types for service clients.

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
            ])

        # MEI
        elif client.regime_tributario == RegimeTributario.MEI:
            codes.extend([
                "DAS_MEI_MENSAL",
                "DASN_SIMEI_ANUAL",
            ])

        # Obrigações municipais (ISS)
        # Service sempre tem ISS
        if client.regime_tributario != RegimeTributario.MEI:
            codes.append("NFS_E_MENSAL")  # Nota Fiscal de Serviços Eletrônica

        # Algumas cidades exigem declaração de ISS
        if client.cidade in ["São Paulo", "Rio de Janeiro", "Belo Horizonte"]:
            codes.append("DMS_MENSAL")  # Declaração Mensal de Serviços

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
