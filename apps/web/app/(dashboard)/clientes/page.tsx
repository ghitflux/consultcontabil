'use client';

import { Button, Card, CardBody, CardHeader, Chip, Divider, Modal, ModalBody, ModalContent, ModalHeader, Pagination, Spinner, Table, TableBody, TableCell, TableColumn, TableHeader, TableRow, useDisclosure } from '@/heroui';
import { useClients } from '@/hooks/useClients';
import type { ClientListItem, ClientStatus } from '@/types/client';
import { formatCNPJ, getRegimeLabel, getStatusLabel, getTipoEmpresaLabel } from '@/types/client';
import { useEffect, useState } from 'react';
import { SearchInput } from '@/components/ui/SearchInput';

export default function ClientesPage() {
  const { clients, selectedClient, isLoading, fetchClients, fetchClientById, setSelectedClient } = useClients();
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [letterFilter, setLetterFilter] = useState('');
  const [page, setPage] = useState(1);
  const { isOpen, onOpen, onClose } = useDisclosure();

  const pageSize = 10;

  // Fetch clients on mount and when filters change
  useEffect(() => {
    fetchClients({
      query: searchQuery || undefined,
      status: (statusFilter as ClientStatus) || undefined,
      starts_with: letterFilter || undefined,
      page,
      size: pageSize,
    });
  }, [searchQuery, statusFilter, letterFilter, page, fetchClients]);

  const handleViewDetails = async (client: ClientListItem) => {
    await fetchClientById(client.id);
    onOpen();
  };

  const handleCloseModal = () => {
    setSelectedClient(null);
    onClose();
  };

  const statusColors: Record<ClientStatus, "success" | "warning" | "default"> = {
    ativo: "success",
    pendente: "warning",
    inativo: "default",
  };

  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Clientes</h1>
          <p className="text-sm text-default-500">Gerenciar clientes do escritório</p>
        </div>
        <Button color="primary">
          <PlusIcon className="h-5 w-5" />
          Novo Cliente
        </Button>
      </div>

      <Card>
        <CardHeader className="flex flex-col items-start gap-4 px-6 pt-6">
          <div className="flex w-full items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold">Lista de Clientes</h2>
              <p className="text-sm text-default-500">
                {clients?.total || 0} cliente{clients?.total !== 1 ? 's' : ''} cadastrado{clients?.total !== 1 ? 's' : ''}
              </p>
            </div>
          </div>

          {/* Search and Filters */}
          <div className="flex w-full flex-col gap-4">
            <div className="flex flex-col gap-4 md:flex-row">
              <div className="w-full md:w-80">
                <SearchInput
                  value={searchQuery}
                  onValueChange={setSearchQuery}
                  placeholder="Buscar por razão social ou CNPJ..."
                />
              </div>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant={statusFilter === '' ? 'solid' : 'bordered'}
                  onPress={() => setStatusFilter('')}
                >
                  Todos
                </Button>
                <Button
                  size="sm"
                  variant={statusFilter === 'ativo' ? 'solid' : 'bordered'}
                  color="success"
                  onPress={() => setStatusFilter('ativo')}
                >
                  Ativos
                </Button>
                <Button
                  size="sm"
                  variant={statusFilter === 'pendente' ? 'solid' : 'bordered'}
                  color="warning"
                  onPress={() => setStatusFilter('pendente')}
                >
                  Pendentes
                </Button>
              </div>
            </div>

            {/* Alphabetical Filter */}
            <div className="flex flex-wrap gap-1">
              <Button
                size="sm"
                variant={letterFilter === '' ? 'solid' : 'flat'}
                className="min-w-8"
                onPress={() => setLetterFilter('')}
              >
                Todas
              </Button>
              {alphabet.map((letter) => (
                <Button
                  key={letter}
                  size="sm"
                  variant={letterFilter === letter ? 'solid' : 'flat'}
                  className="min-w-8"
                  onPress={() => setLetterFilter(letter)}
                >
                  {letter}
                </Button>
              ))}
            </div>
          </div>
        </CardHeader>
        <Divider />
        <CardBody className="p-0">
          {isLoading ? (
            <div className="flex items-center justify-center p-8">
              <Spinner size="lg" />
            </div>
          ) : (
            <>
              <Table aria-label="Tabela de clientes" removeWrapper>
                <TableHeader>
                  <TableColumn>RAZÃO SOCIAL</TableColumn>
                  <TableColumn>CNPJ</TableColumn>
                  <TableColumn>REGIME</TableColumn>
                  <TableColumn>HONORÁRIOS</TableColumn>
                  <TableColumn>STATUS</TableColumn>
                  <TableColumn>AÇÕES</TableColumn>
                </TableHeader>
                <TableBody emptyContent="Nenhum cliente encontrado">
                  {(clients?.items || []).map((client) => (
                    <TableRow key={client.id}>
                      <TableCell>
                        <div>
                          <p className="font-medium">{client.razao_social}</p>
                          {client.nome_fantasia && (
                            <p className="text-xs text-default-500">{client.nome_fantasia}</p>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <code className="text-xs">{formatCNPJ(client.cnpj)}</code>
                      </TableCell>
                      <TableCell>
                        <span className="text-sm">{getRegimeLabel(client.regime_tributario)}</span>
                      </TableCell>
                      <TableCell>
                        <span className="font-medium">
                          {client.honorarios_mensais.toLocaleString('pt-BR', {
                            style: 'currency',
                            currency: 'BRL',
                          })}
                        </span>
                      </TableCell>
                      <TableCell>
                        <Chip size="sm" color={statusColors[client.status]} variant="flat">
                          {getStatusLabel(client.status)}
                        </Chip>
                      </TableCell>
                      <TableCell>
                        <Button
                          size="sm"
                          variant="light"
                          onPress={() => handleViewDetails(client)}
                        >
                          Ver detalhes
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>

              {/* Pagination */}
              {clients && clients.pages > 1 && (
                <div className="flex justify-center p-4">
                  <Pagination
                    total={clients.pages}
                    page={page}
                    onChange={setPage}
                    showControls
                  />
                </div>
              )}
            </>
          )}
        </CardBody>
      </Card>

      {/* Details Modal */}
      <Modal isOpen={isOpen} onClose={handleCloseModal} size="2xl" scrollBehavior="inside">
        <ModalContent>
          <ModalHeader>Detalhes do Cliente</ModalHeader>
          <ModalBody className="pb-6">
            {selectedClient ? (
              <div className="space-y-6">
                {/* Company Info */}
                <div>
                  <h3 className="mb-3 font-semibold">Informações da Empresa</h3>
                  <div className="grid gap-3 md:grid-cols-2">
                    <DetailItem label="Razão Social" value={selectedClient.razao_social} />
                    <DetailItem label="Nome Fantasia" value={selectedClient.nome_fantasia} />
                    <DetailItem label="CNPJ" value={formatCNPJ(selectedClient.cnpj)} />
                    <DetailItem label="Inscrição Estadual" value={selectedClient.inscricao_estadual} />
                  </div>
                </div>

                {/* Contact */}
                <div>
                  <h3 className="mb-3 font-semibold">Contato</h3>
                  <div className="grid gap-3 md:grid-cols-2">
                    <DetailItem label="Email" value={selectedClient.email} />
                    <DetailItem label="Telefone" value={selectedClient.telefone} />
                  </div>
                </div>

                {/* Address */}
                {selectedClient.logradouro && (
                  <div>
                    <h3 className="mb-3 font-semibold">Endereço</h3>
                    <DetailItem
                      label="Endereço Completo"
                      value={`${selectedClient.logradouro}, ${selectedClient.numero}${
                        selectedClient.complemento ? ` - ${selectedClient.complemento}` : ''
                      }, ${selectedClient.bairro}, ${selectedClient.cidade}/${selectedClient.uf}`}
                    />
                  </div>
                )}

                {/* Financial */}
                <div>
                  <h3 className="mb-3 font-semibold">Informações Financeiras</h3>
                  <div className="grid gap-3 md:grid-cols-2">
                    <DetailItem
                      label="Honorários Mensais"
                      value={selectedClient.honorarios_mensais.toLocaleString('pt-BR', {
                        style: 'currency',
                        currency: 'BRL',
                      })}
                    />
                    <DetailItem label="Dia de Vencimento" value={selectedClient.dia_vencimento.toString()} />
                  </div>
                </div>

                {/* Tax Info */}
                <div>
                  <h3 className="mb-3 font-semibold">Informações Tributárias</h3>
                  <div className="grid gap-3 md:grid-cols-2">
                    <DetailItem label="Regime Tributário" value={getRegimeLabel(selectedClient.regime_tributario)} />
                    <DetailItem label="Tipo de Empresa" value={getTipoEmpresaLabel(selectedClient.tipo_empresa)} />
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex justify-center p-8">
                <Spinner />
              </div>
            )}
          </ModalBody>
        </ModalContent>
      </Modal>
    </div>
  );
}

function DetailItem({ label, value }: { label: string; value: string | null | undefined }) {
  return (
    <div>
      <p className="text-xs text-default-500">{label}</p>
      <p className="text-sm">{value || '-'}</p>
    </div>
  );
}

function PlusIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
    </svg>
  );
}
