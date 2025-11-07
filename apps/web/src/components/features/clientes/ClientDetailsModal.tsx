"use client";

import React from "react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  Snippet,
  Chip,
  Divider,
} from "@heroui/react";
import { EditIcon } from "@/lib/icons";
import type { Client } from "@/types/client";
import {
  formatCNPJ,
  formatPhone,
  getStatusLabel,
  getRegimeLabel,
  getTipoEmpresaLabel,
  getServicoContratadoLabel,
  getLicencaNecessariaLabel,
} from "@/types/client";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";

interface ClientDetailsModalProps {
  client: Client | null;
  isOpen: boolean;
  onClose: () => void;
  onEdit?: (client: Client) => void;
}

export function ClientDetailsModal({ client, isOpen, onClose, onEdit }: ClientDetailsModalProps) {
  if (!client) return null;

  const formatDate = (dateString: string | null) => {
    if (!dateString) return "-";
    try {
      return format(new Date(dateString), "dd/MM/yyyy", { locale: ptBR });
    } catch {
      return dateString;
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      size="5xl"
      scrollBehavior="inside"
    >
      <ModalContent>
        {(onCloseModal) => (
          <>
            <ModalHeader className="flex flex-col gap-1">
              <h2 className="text-2xl font-bold">{client.razao_social}</h2>
              <div className="flex items-center gap-2">
                <Chip
                  color={
                    client.status === "ativo"
                      ? "success"
                      : client.status === "pendente"
                        ? "warning"
                        : "danger"
                  }
                  variant="flat"
                  size="sm"
                >
                  {getStatusLabel(client.status)}
                </Chip>
                <Chip color="primary" variant="flat" size="sm">
                  {getRegimeLabel(client.regime_tributario)}
                </Chip>
              </div>
            </ModalHeader>
            <ModalBody>
              <div className="space-y-6">
                {/* Dados da Empresa */}
                <section>
                  <h3 className="text-lg font-semibold mb-3">Dados da Empresa</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                      <p className="text-xs text-gray-600 mb-1">Razão Social</p>
                      <Snippet symbol="" size="sm">{client.razao_social}</Snippet>
                    </div>
                    {client.nome_fantasia && (
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Nome Fantasia</p>
                        <Snippet symbol="" size="sm">{client.nome_fantasia}</Snippet>
                      </div>
                    )}
                    <div>
                      <p className="text-xs text-gray-600 mb-1">CNPJ</p>
                      <Snippet symbol="" size="sm">{formatCNPJ(client.cnpj)}</Snippet>
                    </div>
                    {client.inscricao_estadual && (
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Inscrição Estadual</p>
                        <Snippet symbol="" size="sm">{client.inscricao_estadual}</Snippet>
                      </div>
                    )}
                    {client.inscricao_municipal && (
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Inscrição Municipal</p>
                        <Snippet symbol="" size="sm">{client.inscricao_municipal}</Snippet>
                      </div>
                    )}
                    {client.codigo_simples && (
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Código Simples</p>
                        <Snippet symbol="" size="sm">{client.codigo_simples}</Snippet>
                      </div>
                    )}
                  </div>
                </section>

                <Divider />

                {/* Contato */}
                <section>
                  <h3 className="text-lg font-semibold mb-3">Contato</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                      <p className="text-xs text-gray-600 mb-1">Email</p>
                      <Snippet symbol="" size="sm">{client.email}</Snippet>
                    </div>
                    {client.telefone && (
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Telefone</p>
                        <Snippet symbol="" size="sm">{formatPhone(client.telefone) || client.telefone}</Snippet>
                      </div>
                    )}
                    {client.celular && (
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Celular</p>
                        <Snippet symbol="" size="sm">{formatPhone(client.celular) || client.celular}</Snippet>
                      </div>
                    )}
                  </div>
                </section>

                <Divider />

                {/* Endereço */}
                {(client.logradouro || client.cidade) && (
                  <>
                    <section>
                      <h3 className="text-lg font-semibold mb-3">Endereço</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {client.cep && (
                          <div>
                            <p className="text-xs text-gray-600 mb-1">CEP</p>
                            <Snippet symbol="" size="sm">{client.cep}</Snippet>
                          </div>
                        )}
                        {client.logradouro && (
                          <div>
                            <p className="text-xs text-gray-600 mb-1">Logradouro</p>
                            <Snippet symbol="" size="sm">{client.logradouro}</Snippet>
                          </div>
                        )}
                        {client.numero && (
                          <div>
                            <p className="text-xs text-gray-600 mb-1">Número</p>
                            <Snippet symbol="" size="sm">{client.numero}</Snippet>
                          </div>
                        )}
                        {client.complemento && (
                          <div>
                            <p className="text-xs text-gray-600 mb-1">Complemento</p>
                            <Snippet symbol="" size="sm">{client.complemento}</Snippet>
                          </div>
                        )}
                        {client.bairro && (
                          <div>
                            <p className="text-xs text-gray-600 mb-1">Bairro</p>
                            <Snippet symbol="" size="sm">{client.bairro}</Snippet>
                          </div>
                        )}
                        {client.cidade && (
                          <div>
                            <p className="text-xs text-gray-600 mb-1">Cidade</p>
                            <Snippet symbol="" size="sm">{`${client.cidade} - ${client.uf}`}</Snippet>
                          </div>
                        )}
                      </div>
                    </section>
                    <Divider />
                  </>
                )}

                {/* Financeiro */}
                <section>
                  <h3 className="text-lg font-semibold mb-3">Financeiro</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                      <p className="text-xs text-gray-600 mb-1">Honorários Mensais</p>
                      <Snippet symbol="" size="sm" color="success">{formatCurrency(client.honorarios_mensais)}</Snippet>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600 mb-1">Vencimento</p>
                      <Snippet symbol="" size="sm">Dia {client.dia_vencimento}</Snippet>
                    </div>
                  </div>
                </section>

                <Divider />

                {/* Informações Tributárias */}
                <section>
                  <h3 className="text-lg font-semibold mb-3">Informações Tributárias</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                      <p className="text-xs text-gray-600 mb-1">Regime Tributário</p>
                      <Snippet symbol="" size="sm">{getRegimeLabel(client.regime_tributario)}</Snippet>
                    </div>
                    {client.data_abertura && (
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Data de Abertura</p>
                        <Snippet symbol="" size="sm">{formatDate(client.data_abertura)}</Snippet>
                      </div>
                    )}
                    {client.inicio_escritorio && (
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Início no Escritório</p>
                        <Snippet symbol="" size="sm">{formatDate(client.inicio_escritorio)}</Snippet>
                      </div>
                    )}
                  </div>
                </section>

                {/* Tipos de Empresa */}
                {client.tipos_empresa && client.tipos_empresa.length > 0 && (
                  <>
                    <Divider />
                    <section>
                      <h3 className="text-lg font-semibold mb-3">Tipos de Empresa</h3>
                      <div className="flex flex-wrap gap-2">
                        {client.tipos_empresa.map((tipo) => (
                          <Chip key={tipo} color="default" variant="flat">
                            {getTipoEmpresaLabel(tipo)}
                          </Chip>
                        ))}
                      </div>
                    </section>
                  </>
                )}

                {/* Serviços Contratados */}
                {client.servicos_contratados && client.servicos_contratados.length > 0 && (
                  <>
                    <Divider />
                    <section>
                      <h3 className="text-lg font-semibold mb-3">Serviços Contratados</h3>
                      <div className="flex flex-wrap gap-2">
                        {client.servicos_contratados.map((servico) => (
                          <Chip key={servico} color="primary" variant="flat">
                            {getServicoContratadoLabel(servico)}
                          </Chip>
                        ))}
                      </div>
                    </section>
                  </>
                )}

                {/* Licenças Necessárias */}
                {client.licencas_necessarias && client.licencas_necessarias.length > 0 && (
                  <>
                    <Divider />
                    <section>
                      <h3 className="text-lg font-semibold mb-3">Licenças Necessárias</h3>
                      <div className="flex flex-wrap gap-2">
                        {client.licencas_necessarias.map((licenca) => (
                          <Chip key={licenca} color="warning" variant="flat">
                            {getLicencaNecessariaLabel(licenca)}
                          </Chip>
                        ))}
                      </div>
                    </section>
                  </>
                )}

                {/* Responsável */}
                {client.responsavel_nome && (
                  <>
                    <Divider />
                    <section>
                      <h3 className="text-lg font-semibold mb-3">Responsável</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div>
                          <p className="text-xs text-gray-600 mb-1">Nome</p>
                          <Snippet symbol="" size="sm">{client.responsavel_nome}</Snippet>
                        </div>
                        {client.responsavel_cpf && (
                          <div>
                            <p className="text-xs text-gray-600 mb-1">CPF</p>
                            <Snippet symbol="" size="sm">{client.responsavel_cpf}</Snippet>
                          </div>
                        )}
                        {client.responsavel_email && (
                          <div>
                            <p className="text-xs text-gray-600 mb-1">Email</p>
                            <Snippet symbol="" size="sm">{client.responsavel_email}</Snippet>
                          </div>
                        )}
                        {client.responsavel_telefone && (
                          <div>
                            <p className="text-xs text-gray-600 mb-1">Telefone</p>
                            <Snippet symbol="" size="sm">{formatPhone(client.responsavel_telefone) || client.responsavel_telefone}</Snippet>
                          </div>
                        )}
                      </div>
                    </section>
                  </>
                )}

                {/* Observações */}
                {client.observacoes && (
                  <>
                    <Divider />
                    <section>
                      <h3 className="text-lg font-semibold mb-3">Observações</h3>
                      <Snippet symbol="" size="sm" className="whitespace-pre-wrap">
                        {client.observacoes}
                      </Snippet>
                    </section>
                  </>
                )}
              </div>
            </ModalBody>
            <ModalFooter>
              {onEdit && (
                <Button
                  color="primary"
                  startContent={<EditIcon className="h-4 w-4" />}
                  onClick={() => {
                    onEdit(client);
                    onCloseModal();
                  }}
                >
                  Editar
                </Button>
              )}
              <Button variant="light" onClick={onCloseModal}>
                Fechar
              </Button>
            </ModalFooter>
          </>
        )}
      </ModalContent>
    </Modal>
  );
}
