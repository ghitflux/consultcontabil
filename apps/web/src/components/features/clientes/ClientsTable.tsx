'use client';

import { useMemo } from 'react';
import { Chip } from '@/heroui';
import type { Client } from '@/lib/mocks/clients';
import { DataTable, type Column } from '@/components/ui/DataTable';
import { SnippetCopy } from '@/components/ui/SnippetCopy';

interface ClientsTableProps {
  clients: Client[];
  isLoading?: boolean;
}

const statusColorMap: Record<Client['status'], 'success' | 'warning' | 'default'> = {
  ativo: 'success',
  pendente: 'warning',
  inativo: 'default',
};

const statusLabelMap: Record<Client['status'], string> = {
  ativo: 'Ativo',
  pendente: 'Pendente',
  inativo: 'Inativo',
};

export function ClientsTable({ clients, isLoading = false }: ClientsTableProps) {
  const columns = useMemo<Column<Client>[]>(
    () => [
      {
        key: 'razaoSocial',
        label: 'Razão Social',
        sortable: true,
      },
      {
        key: 'cnpj',
        label: 'CNPJ',
        render: (client) => <SnippetCopy text={client.cnpj} />,
      },
      {
        key: 'email',
        label: 'Email',
        render: (client) => <SnippetCopy text={client.email} />,
      },
      {
        key: 'status',
        label: 'Status',
        sortable: true,
        render: (client) => (
          <Chip color={statusColorMap[client.status]} size="sm" variant="flat">
            {statusLabelMap[client.status]}
          </Chip>
        ),
      },
      {
        key: 'honorarios',
        label: 'Honorários',
        sortable: true,
        render: (client) => (
          <span className="font-medium">
            {new Intl.NumberFormat('pt-BR', {
              style: 'currency',
              currency: 'BRL',
            }).format(client.honorarios)}
          </span>
        ),
      },
    ],
    []
  );

  return (
    <DataTable
      columns={columns}
      data={clients}
      isLoading={isLoading}
      getRowKey={(client) => client.id}
      emptyContent="Nenhum cliente encontrado"
    />
  );
}
