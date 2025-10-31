"use client";

import { Card, CardHeader, CardBody, Chip } from "@/heroui";
import { useAuth } from "@/hooks/auth/useAuth";

export default function PortalHomePage() {
  const { user } = useAuth();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Bem-vindo ao Portal do Cliente</h1>
        <p className="text-default-500 mt-1">
          Gerencie suas obrigações e finanças em um só lugar
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold">Obrigações Pendentes</h3>
          </CardHeader>
          <CardBody>
            <p className="text-4xl font-bold text-warning">-</p>
            <p className="text-sm text-default-500 mt-2">
              Carregando informações...
            </p>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold">Financeiro</h3>
          </CardHeader>
          <CardBody>
            <p className="text-4xl font-bold text-primary">-</p>
            <p className="text-sm text-default-500 mt-2">
              Saldo em aberto
            </p>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold">Próximo Vencimento</h3>
          </CardHeader>
          <CardBody>
            <p className="text-4xl font-bold text-danger">-</p>
            <p className="text-sm text-default-500 mt-2">
              Carregando informações...
            </p>
          </CardBody>
        </Card>
      </div>

      {/* Quick Links */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-semibold">Acesso Rápido</h3>
        </CardHeader>
        <CardBody>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <a
              href="/portal/obrigacoes"
              className="p-4 border border-divider rounded-lg hover:bg-default-100 transition-colors"
            >
              <h4 className="font-semibold mb-1">Minhas Obrigações</h4>
              <p className="text-sm text-default-500">
                Acompanhe suas obrigações fiscais e prazos
              </p>
            </a>

            <a
              href="/portal/financeiro"
              className="p-4 border border-divider rounded-lg hover:bg-default-100 transition-colors"
            >
              <h4 className="font-semibold mb-1">Financeiro</h4>
              <p className="text-sm text-default-500">
                Consulte pagamentos e faturas
              </p>
            </a>

            <a
              href="/portal/meus-dados"
              className="p-4 border border-divider rounded-lg hover:bg-default-100 transition-colors"
            >
              <h4 className="font-semibold mb-1">Meus Dados</h4>
              <p className="text-sm text-default-500">
                Visualize e atualize suas informações
              </p>
            </a>

            <a
              href="/portal/solicitacoes"
              className="p-4 border border-divider rounded-lg hover:bg-default-100 transition-colors"
            >
              <h4 className="font-semibold mb-1">Solicitações</h4>
              <p className="text-sm text-default-500">
                Envie dúvidas e solicitações
              </p>
            </a>
          </div>
        </CardBody>
      </Card>

      {/* User Info */}
      {user && (
        <Card>
          <CardHeader>
            <h3 className="text-lg font-semibold">Informações da Conta</h3>
          </CardHeader>
          <CardBody>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-default-500">Nome:</span>
                <span className="font-semibold">{user.name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-default-500">Email:</span>
                <span className="font-semibold">{user.email}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-default-500">Perfil:</span>
                <Chip color="primary" size="sm" variant="flat">
                  Cliente
                </Chip>
              </div>
            </div>
          </CardBody>
        </Card>
      )}
    </div>
  );
}
