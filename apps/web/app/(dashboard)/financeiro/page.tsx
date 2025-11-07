"use client";

import { Card, CardBody, CardHeader, Spinner, Button } from "@/heroui";
import { useEffect, useState } from "react";
// import { financeApi } from "@/lib/api/endpoints/finance";
import type { FinancialDashboardKPIs } from "@/types/finance";
import { formatCurrency } from "@/types/finance";
import Link from "next/link";

export default function FinanceiroDashboard() {
  const [kpis] = useState<FinancialDashboardKPIs | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadKPIs();
  }, []);

  const loadKPIs = async () => {
    try {
      setLoading(true);
      // TODO: Implement getDashboardKPIs endpoint
      // const data = await (financeApi as any).getDashboardKPIs();
      // setKpis(data);
    } catch (error) {
      console.error("Error loading KPIs:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Dashboard Financeiro</h1>
          <p className="text-default-500 mt-1">Visão geral das finanças</p>
        </div>
        <div className="flex gap-2">
          <Link href="/financeiro/transacoes">
            <Button color="primary">Ver Transações</Button>
          </Link>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardBody className="text-center">
            <p className="text-sm text-default-500">Receita do Mês</p>
            <p className="text-3xl font-bold text-success">
              {formatCurrency(kpis?.total_receita_mes_atual || 0)}
            </p>
            <p className={`text-sm mt-1 ${(kpis?.receita_crescimento_percentual || 0) >= 0 ? 'text-success' : 'text-danger'}`}>
              {(kpis?.receita_crescimento_percentual || 0) >= 0 ? '↑' : '↓'}
              {Math.abs(kpis?.receita_crescimento_percentual || 0).toFixed(1)}% vs mês anterior
            </p>
          </CardBody>
        </Card>

        <Card>
          <CardBody className="text-center">
            <p className="text-sm text-default-500">Total Pendente</p>
            <p className="text-3xl font-bold text-warning">
              {formatCurrency(kpis?.total_pendente || 0)}
            </p>
            <p className="text-sm text-default-500 mt-1">
              {kpis?.count_pendente || 0} transações
            </p>
          </CardBody>
        </Card>

        <Card>
          <CardBody className="text-center">
            <p className="text-sm text-default-500">Total Atrasado</p>
            <p className="text-3xl font-bold text-danger">
              {formatCurrency(kpis?.total_atrasado || 0)}
            </p>
            <p className="text-sm text-default-500 mt-1">
              {kpis?.count_atrasado || 0} transações
            </p>
          </CardBody>
        </Card>

        <Card>
          <CardBody className="text-center">
            <p className="text-sm text-default-500">Pago este Mês</p>
            <p className="text-3xl font-bold text-primary">
              {formatCurrency(kpis?.total_pago_mes_atual || 0)}
            </p>
            <p className="text-sm text-default-500 mt-1">
              {kpis?.count_pago_mes_atual || 0} transações
            </p>
          </CardBody>
        </Card>
      </div>

      {/* Top Debtors */}
      {kpis && kpis.top_devedores && kpis.top_devedores.length > 0 && (
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold">Maiores Devedores</h3>
          </CardHeader>
          <CardBody>
            <div className="space-y-3">
              {kpis.top_devedores.map((devedor) => (
                <div key={devedor.client_id} className="flex justify-between items-center p-3 border border-divider rounded-lg">
                  <span className="font-medium">{devedor.client_name}</span>
                  <span className="text-danger font-bold">
                    {formatCurrency(devedor.total_pendente)}
                  </span>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>
      )}

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link href="/financeiro/transacoes">
          <Card isPressable className="hover:scale-105 transition-transform">
            <CardBody className="text-center p-6">
              <div className="text-4xl mb-2">💰</div>
              <h3 className="font-semibold text-lg">Transações</h3>
              <p className="text-sm text-default-500">Gerenciar transações financeiras</p>
            </CardBody>
          </Card>
        </Link>

        <Link href="/financeiro/relatorios">
          <Card isPressable className="hover:scale-105 transition-transform">
            <CardBody className="text-center p-6">
              <div className="text-4xl mb-2">📊</div>
              <h3 className="font-semibold text-lg">Relatórios</h3>
              <p className="text-sm text-default-500">Ver relatórios financeiros</p>
            </CardBody>
          </Card>
        </Link>

        <Card isPressable className="hover:scale-105 transition-transform">
          <CardBody className="text-center p-6">
            <div className="text-4xl mb-2">📄</div>
            <h3 className="font-semibold text-lg">Gerar Honorários</h3>
            <p className="text-sm text-default-500">Gerar honorários mensais</p>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
