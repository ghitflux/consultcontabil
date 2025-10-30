"""
Obligation rules for commerce companies.
"""

from typing import List

from app.db.models.client import Client, RegimeTributario
from app.patterns.strategies.base import ObligationRule


class CommerceRule(ObligationRule):
    """
    Obligation rules for commerce (comércio) companies.

    Defines which obligations apply based on tax regime.
    """

    def get_applicable_type_codes(self, client: Client) -> List[str]:
        """
        Get applicable obligation types for commerce clients.

        Args:
            client: Client instance

        Returns:
            List of obligation type codes
        """
        codes = []

        # Simples Nacional
        if client.regime_tributario == RegimeTributario.SIMPLES_NACIONAL:
            codes.extend([
                "DAS_MENSAL",           # Documento de Arrecadação do Simples
                "DEFIS_ANUAL",          # Declaração de Informações Socioeconômicas e Fiscais
            ])

        # Lucro Presumido
        elif client.regime_tributario == RegimeTributario.LUCRO_PRESUMIDO:
            codes.extend([
                "DCTF_MENSAL",          # Declaração de Débitos e Créditos Tributários Federais
                "PIS_COFINS_MENSAL",    # PIS/COFINS Cumulativo
                "EFD_CONTRIBUICOES",    # Escrituração Fiscal Digital de Contribuições
                "IRPJ_TRIMESTRAL",      # Imposto de Renda Pessoa Jurídica
                "CSLL_TRIMESTRAL",      # Contribuição Social sobre o Lucro Líquido
            ])

        # Lucro Real
        elif client.regime_tributario == RegimeTributario.LUCRO_REAL:
            codes.extend([
                "DCTF_MENSAL",
                "PIS_COFINS_MENSAL",    # PIS/COFINS Não-Cumulativo
                "EFD_CONTRIBUICOES",
                "IRPJ_MENSAL",          # IR estimativa mensal
                "CSLL_MENSAL",          # CSLL estimativa mensal
                "LALUR_ANUAL",          # Livro de Apuração do Lucro Real
            ])

        # MEI
        elif client.regime_tributario == RegimeTributario.MEI:
            codes.extend([
                "DAS_MEI_MENSAL",       # DAS específico para MEI
                "DASN_SIMEI_ANUAL",     # Declaração Anual do Simples Nacional - MEI
            ])

        # Obrigações estaduais (ICMS)
        # Commerce sempre tem ICMS
        if client.regime_tributario != RegimeTributario.MEI:
            codes.append("SPED_FISCAL")  # SPED Fiscal (ICMS/IPI)

        # GIA (alguns estados)
        if client.uf in ["SP"]:
            codes.append("GIA_MENSAL")  # Guia de Informação e Apuração do ICMS

        # Obrigações municipais (ISS - se houver prestação de serviço)
        # Commerce puro normalmente não tem ISS, mas fica como exemplo

        # Obrigações trabalhistas e previdenciárias
        codes.extend([
            "ESOCIAL_MENSAL",       # eSocial
            "FGTS_MENSAL",          # FGTS
            "CAGED_MENSAL",         # Cadastro Geral de Empregados e Desempregados
        ])

        # Obrigações anuais comuns
        codes.extend([
            "DIRPJ_ANUAL",          # Declaração de Informações Econômico-Fiscais da PJ
            "DIRF_ANUAL",           # Declaração do Imposto de Renda Retido na Fonte
            "RAIS_ANUAL",           # Relação Anual de Informações Sociais
        ])

        return codes
