"use client";

import {
  Card,
  CardBody,
  CardHeader,
  Chip,
  Divider,
  Spinner,
  Button,
} from "@/heroui";
import { useEffect, useState } from "react";
import { useAuth } from "@/hooks/auth/useAuth";
import { financeApi } from "@/lib/api/endpoints/finance";
import {
  formatCurrency,
  getPaymentStatusLabel,
  getPaymentStatusColor,
} from "@/types/finance";

interface ClientSummary {
  client_id: string;
  client_name: string;
  client_cnpj: string;
  total_pendente: number;
  total_atrasado: number;
  total_pago: number;
  ultimo_pagamento: string | null;
  proxima_vencimento: string | null;
  transactions: Array<{
    id: string;
    amount: number;
    payment_status: string;
    due_date: string;
    paid_date: string | null;
    reference_month: string;
    description: string;
  }>;
}

export default function PortalFinanceiroPage() {
  const { user } = useAuth();
  const [summary, setSummary] = useState<ClientSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (user) {
      loadSummary();
    }
  }, [user]);

  const loadSummary = async () => {
    try {
      setLoading(true);
      setError(null);

      // In a real scenario, we'd get client_id from user profile
      // For now, we'll fetch the first client associated with the user
      const response = await (financeApi as any).list({ size: 1 });

      if (response.items.length > 0 && response.items[0]?.client_id) {
        const data = await (financeApi as any).getClientSummary(response.items[0].client_id);
        setSummary(data);
      } else {
        setError("Nenhuma informação financeira disponível");
      }
    } catch (err) {
      console.error("Error loading summary:", err);
      setError("Erro ao carregar informações financeiras");
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "long",
      year: "numeric",
    });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error || !summary) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Card>
          <CardBody className="text-center p-8">
            <p className="text-4xl mb-2">⚠️</p>
            <p className="text-default-400">{error || "Dados não encontrados"}</p>
          </CardBody>
        </Card>
      </div>
    );
  }

  const totalOutstanding = summary.total_pendente + summary.total_atrasado;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Financeiro</h1>
        <p className="text-default-500 mt-1">
          Acompanhe seus pagamentos e saldo
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="border-2 border-danger">
          <CardBody className="text-center">
            <p className="text-sm text-default-500 mb-1">Saldo em Aberto</p>
            <p className="text-4xl font-bold text-danger">
              {formatCurrency(totalOutstanding)}
            </p>
            {summary.total_atrasado > 0 && (
              <div className="mt-2">
                <Chip color="danger" size="sm" variant="flat">
                  {formatCurrency(summary.total_atrasado)} em atraso
                </Chip>
              </div>
            )}
          </CardBody>
        </Card>

        <Card>
          <CardBody className="text-center">
            <p className="text-sm text-default-500 mb-1">Total Pago</p>
            <p className="text-4xl font-bold text-success">
              {formatCurrency(summary.total_pago)}
            </p>
            {summary.ultimo_pagamento && (
              <p className="text-xs text-default-400 mt-2">
                Último pagamento: {formatDate(summary.ultimo_pagamento)}
              </p>
            )}
          </CardBody>
        </Card>

        <Card>
          <CardBody className="text-center">
            <p className="text-sm text-default-500 mb-1">Próximo Vencimento</p>
            {summary.proxima_vencimento ? (
              <>
                <p className="text-4xl font-bold text-warning">
                  {new Date(summary.proxima_vencimento).toLocaleDateString(
                    "pt-BR",
                    {
                      day: "2-digit",
                      month: "short",
                    }
                  )}
                </p>
                <p className="text-xs text-default-400 mt-2">
                  {formatDate(summary.proxima_vencimento)}
                </p>
              </>
            ) : (
              <p className="text-2xl font-bold text-default-400">
                Nenhum pendente
              </p>
            )}
          </CardBody>
        </Card>
      </div>

      {/* Company Info */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-semibold">Informações da Empresa</h3>
        </CardHeader>
        <CardBody>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-default-500">Razão Social</p>
              <p className="font-semibold">{summary.client_name}</p>
            </div>
            <div>
              <p className="text-sm text-default-500">CNPJ</p>
              <p className="font-semibold">{summary.client_cnpj}</p>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Transactions History */}
      <Card>
        <CardHeader className="flex justify-between items-center">
          <h3 className="text-lg font-semibold">Histórico de Pagamentos</h3>
          <Button size="sm" color="primary" variant="flat">
            Ver Todos
          </Button>
        </CardHeader>
        <CardBody>
          {summary.transactions && summary.transactions.length > 0 ? (
            <div className="space-y-4">
              {summary.transactions.map((transaction) => (
                <div
                  key={transaction.id}
                  className="p-4 border border-divider rounded-lg"
                >
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h4 className="font-semibold">{transaction.description}</h4>
                      <p className="text-sm text-default-500">
                        Ref: {formatDate(transaction.reference_month)}
                      </p>
                    </div>
                    <Chip
                      color={getPaymentStatusColor(transaction.payment_status as any)}
                      size="sm"
                      variant="flat"
                    >
                      {getPaymentStatusLabel(transaction.payment_status as any)}
                    </Chip>
                  </div>

                  <Divider className="my-2" />

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <p className="text-default-500">Valor</p>
                      <p className="font-semibold">
                        {formatCurrency(transaction.amount)}
                      </p>
                    </div>
                    <div>
                      <p className="text-default-500">Vencimento</p>
                      <p className="font-semibold">
                        {new Date(transaction.due_date).toLocaleDateString(
                          "pt-BR"
                        )}
                      </p>
                    </div>
                    {transaction.paid_date && (
                      <div>
                        <p className="text-default-500">Data do Pagamento</p>
                        <p className="font-semibold">
                          {new Date(transaction.paid_date).toLocaleDateString(
                            "pt-BR"
                          )}
                        </p>
                      </div>
                    )}
                    <div>
                      <Button size="sm" variant="flat" color="primary">
                        Detalhes
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center p-8">
              <p className="text-4xl mb-2">📋</p>
              <p className="text-default-400">Nenhuma transação encontrada</p>
            </div>
          )}
        </CardBody>
      </Card>

      {/* Payment Info */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-semibold">Como Pagar</h3>
        </CardHeader>
        <CardBody>
          <div className="space-y-4">
            <div>
              <h4 className="font-semibold mb-2">PIX</h4>
              <p className="text-sm text-default-500">
                Faça o pagamento via PIX para o CNPJ da contabilidade. Após o
                pagamento, envie o comprovante para nosso WhatsApp ou email.
              </p>
            </div>
            <Divider />
            <div>
              <h4 className="font-semibold mb-2">Transferência Bancária</h4>
              <p className="text-sm text-default-500 mb-2">
                Você também pode realizar transferência bancária:
              </p>
              <div className="bg-default-100 p-3 rounded-lg space-y-1 text-sm">
                <p>
                  <strong>Banco:</strong> Banco do Brasil
                </p>
                <p>
                  <strong>Agência:</strong> 1234-5
                </p>
                <p>
                  <strong>Conta Corrente:</strong> 12345-6
                </p>
                <p>
                  <strong>CNPJ:</strong> 12.345.678/0001-90
                </p>
                <p>
                  <strong>Favorecido:</strong> Contabilidade Exemplo LTDA
                </p>
              </div>
            </div>
            <Divider />
            <div>
              <h4 className="font-semibold mb-2">Dúvidas?</h4>
              <p className="text-sm text-default-500">
                Entre em contato conosco através do WhatsApp (11) 98765-4321 ou
                email financeiro@contabilidade.com.br
              </p>
            </div>
          </div>
        </CardBody>
      </Card>
    </div>
  );
}
