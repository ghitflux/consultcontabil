"""
Obligation rules for MEI (Microempreendedor Individual).
"""

from typing import List

from app.db.models.client import Client
from app.patterns.strategies.base import ObligationRule


class MEIRule(ObligationRule):
    """
    Obligation rules for MEI.

    MEI has simplified obligations regardless of activity type.
    """

    def get_applicable_type_codes(self, client: Client) -> List[str]:
        """
        Get applicable obligation types for MEI clients.

        MEI has very few obligations, regardless of commerce/service/industry.

        Args:
            client: Client instance

        Returns:
            List of obligation type codes
        """
        codes = [
            "DAS_MEI_MENSAL",       # DAS mensal simplificado
            "DASN_SIMEI_ANUAL",     # Declaração anual
        ]

        # Se tiver funcionários (MEI pode ter 1 funcionário)
        # Aqui poderíamos verificar se o cliente tem funcionários
        # Por enquanto, vamos adicionar sempre
        codes.extend([
            "FGTS_MENSAL",          # Se tiver empregado
        ])

        return codes
