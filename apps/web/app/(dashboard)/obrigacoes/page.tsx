"use client";

import { useState, useEffect, useMemo } from "react";
import {
  Card,
  CardBody,
  Button,
  Tabs,
  Tab,
  Select,
  SelectItem,
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Input,
  Textarea,
  useDisclosure,
} from "@/heroui";
import { ObligationsMatrixTable } from "@/components/features/obrigacoes/ObligationsMatrixTable";
import { ObligationTimeline } from "@/components/features/obrigacoes/ObligationTimeline";
import { useObligations, Obligation } from "@/hooks/useObligations";
import { useClients } from "@/hooks/useClients";
import { SearchInput } from "@/components/ui/SearchInput";
import { CalendarIcon } from "@/lib/icons";

const MONTHS = [
  { value: 1, label: "Janeiro" },
  { value: 2, label: "Fevereiro" },
  { value: 3, label: "Março" },
  { value: 4, label: "Abril" },
  { value: 5, label: "Maio" },
  { value: 6, label: "Junho" },
  { value: 7, label: "Julho" },
  { value: 8, label: "Agosto" },
  { value: 9, label: "Setembro" },
  { value: 10, label: "Outubro" },
  { value: 11, label: "Novembro" },
  { value: 12, label: "Dezembro" },
];

const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

export default function ObrigacoesPage() {
  const [activeTab, setActiveTab] = useState<"office" | "client">("office");
  const [selectedClientId, setSelectedClientId] = useState<string>("");
  const [selectedObligation, setSelectedObligation] = useState<Obligation | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [letterFilter, setLetterFilter] = useState("");

  // Competência (mês/ano)
  const currentDate = new Date();
  const [selectedYear, setSelectedYear] = useState(currentDate.getFullYear());
  const [selectedMonth, setSelectedMonth] = useState(currentDate.getMonth() + 1);

  const [filters, setFilters] = useState<{
    status?: string;
    year?: number;
    month?: number;
  }>({});

  // Modals
  const {
    isOpen: isDetailsOpen,
    onOpen: onDetailsOpen,
    onClose: onDetailsClose,
  } = useDisclosure();
  const {
    isOpen: isUploadOpen,
    onOpen: onUploadOpen,
    onClose: onUploadClose,
  } = useDisclosure();
  const {
    isOpen: isCancelOpen,
    onOpen: onCancelOpen,
    onClose: onCancelClose,
  } = useDisclosure();
  const {
    isOpen: isGenerateOpen,
    onOpen: onGenerateOpen,
    onClose: onGenerateClose,
  } = useDisclosure();

  // Form states
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadNotes, setUploadNotes] = useState("");
  const [cancelReason, setCancelReason] = useState("");
  const [generateYear, setGenerateYear] = useState(currentDate.getFullYear());
  const [generateMonth, setGenerateMonth] = useState(currentDate.getMonth() + 1);

  const { clients, isLoading: clientsLoading, fetchClients: fetchClientsData } = useClients();

  // Determinar qual clientId usar baseado na tab
  const effectiveClientId = activeTab === "client" ? selectedClientId : "";

  const {
    obligations,
    loading: obligationsLoading,
    uploadReceipt,
    cancelObligation,
    generateObligations,
    fetchObligations,
  } = useObligations({
    clientId: effectiveClientId || undefined,
    year: selectedYear,
    month: selectedMonth,
    ...filters,
    autoFetch: true,
  });

  // Fetch clients on mount
  useEffect(() => {
    fetchClientsData({ size: 1000 });
  }, [fetchClientsData]);

  // Atualizar filtros quando competência muda
  useEffect(() => {
    setFilters({
      year: selectedYear,
      month: selectedMonth,
    });
  }, [selectedYear, selectedMonth]);

  // Filtrar obrigações por busca e letra
  const filteredObligations = useMemo(() => {
    let filtered = obligations;

    // Filtrar por busca
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (ob) =>
          ob.client_name.toLowerCase().includes(query) ||
          ob.client_cnpj.replace(/\D/g, "").includes(query)
      );
    }

    // Filtrar por letra
    if (letterFilter) {
      filtered = filtered.filter((ob) =>
        ob.client_name.toUpperCase().startsWith(letterFilter)
      );
    }

    return filtered;
  }, [obligations, searchQuery, letterFilter]);

  const handleViewDetails = (obligation: Obligation) => {
    setSelectedObligation(obligation);
    onDetailsOpen();
  };

  const handleDownload = async (obligation: Obligation) => {
    // Simular baixa - você pode chamar uploadReceipt ou uma função específica
    setSelectedObligation(obligation);
    onUploadOpen();
  };

  const handleRefresh = (obligation: Obligation) => {
    // Recarregar obrigações
    fetchObligations();
  };

  const handleUploadReceipt = (obligation: Obligation) => {
    setSelectedObligation(obligation);
    setUploadFile(null);
    setUploadNotes("");
    onUploadOpen();
  };

  const handleCancelObligation = (obligation: Obligation) => {
    setSelectedObligation(obligation);
    setCancelReason("");
    onCancelOpen();
  };

  const handleUploadSubmit = async () => {
    if (!selectedObligation || !uploadFile) return;

    try {
      await uploadReceipt(selectedObligation.id, uploadFile, uploadNotes);
      onUploadClose();
      fetchObligations();
    } catch (error) {
      console.error("Error uploading receipt:", error);
    }
  };

  const handleCancelSubmit = async () => {
    if (!selectedObligation || !cancelReason) return;

    try {
      await cancelObligation(selectedObligation.id, cancelReason);
      onCancelClose();
      fetchObligations();
    } catch (error) {
      console.error("Error cancelling obligation:", error);
    }
  };

  const handleGenerateSubmit = async () => {
    try {
      await generateObligations(
        generateYear,
        generateMonth,
        activeTab === "client" ? selectedClientId || undefined : undefined
      );
      onGenerateClose();
      fetchObligations();
    } catch (error) {
      console.error("Error generating obligations:", error);
    }
  };

  const formatCompetencia = () => {
    const month = MONTHS.find((m) => m.value === selectedMonth);
    return `${month?.label.toLowerCase() || ""} de ${selectedYear}`;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Obrigações Fiscais</h1>
        <p className="text-default-500 mt-1">
          Gerencie e acompanhe as obrigações fiscais dos clientes
        </p>
      </div>

      {/* Tabs e Filtros */}
      <Card>
        <CardBody className="space-y-4">
          <Tabs
            selectedKey={activeTab}
            onSelectionChange={(key) => {
              setActiveTab(key as "office" | "client");
              setSelectedClientId("");
            }}
          >
            <Tab key="office" title="Obrigações do Escritório" />
            <Tab key="client" title="Cliente Específico" />
          </Tabs>

          {activeTab === "client" && (
            <Select
              label="Selecione um Cliente"
              placeholder="Escolha um cliente"
              selectedKeys={selectedClientId ? [selectedClientId] : []}
              onSelectionChange={(keys) => {
                const value = Array.from(keys)[0] as string;
                setSelectedClientId(value || "");
              }}
              isLoading={clientsLoading}
              variant="bordered"
            >
              {(clients?.items || []).map((client) => (
                <SelectItem key={client.id}>
                  {client.razao_social} - {client.cnpj}
                </SelectItem>
              ))}
            </Select>
          )}

          <div className="flex flex-col gap-4 md:flex-row md:items-end">
            {/* Competência */}
            <div className="flex gap-2 items-end">
              <Select
                label="Competência"
                placeholder="Mês"
                selectedKeys={selectedMonth.toString()}
                onSelectionChange={(keys) => {
                  const value = Array.from(keys)[0] as string;
                  setSelectedMonth(parseInt(value) || currentDate.getMonth() + 1);
                }}
                variant="bordered"
                className="w-48"
                startContent={<CalendarIcon className="h-5 w-5 text-default-400" />}
              >
                {MONTHS.map((month) => (
                  <SelectItem key={month.value.toString()}>
                    {month.label}
                  </SelectItem>
                ))}
              </Select>
              <Select
                placeholder="Ano"
                selectedKeys={selectedYear.toString()}
                onSelectionChange={(keys) => {
                  const value = Array.from(keys)[0] as string;
                  setSelectedYear(parseInt(value) || currentDate.getFullYear());
                }}
                variant="bordered"
                className="w-32"
              >
                {Array.from({ length: 5 }, (_, i) => {
                  const year = currentDate.getFullYear() - 2 + i;
                  return (
                    <SelectItem key={year.toString()}>
                      {year}
                    </SelectItem>
                  );
                })}
              </Select>
            </div>

            {/* Busca */}
            <div className="flex-1">
              <SearchInput
                value={searchQuery}
                onValueChange={setSearchQuery}
                placeholder="Buscar empresa..."
              />
            </div>

            {/* Gerar Obrigações */}
            <Button color="success" variant="flat" onPress={onGenerateOpen}>
              Gerar Obrigações
            </Button>
          </div>

          {/* Filtro rápido por letra */}
          <div className="flex flex-wrap gap-1">
            <Button
              size="sm"
              variant={letterFilter === "" ? "solid" : "flat"}
              className="min-w-8"
              onPress={() => setLetterFilter("")}
            >
              Todas
            </Button>
            {ALPHABET.map((letter) => (
              <Button
                key={letter}
                size="sm"
                variant={letterFilter === letter ? "solid" : "flat"}
                className="min-w-8"
                onPress={() => setLetterFilter(letter)}
              >
                {letter}
              </Button>
            ))}
          </div>
        </CardBody>
      </Card>

      {/* Tabela de Obrigações */}
      {(activeTab === "office" || (activeTab === "client" && selectedClientId)) && (
        <Card>
          <CardBody className="p-0">
            <ObligationsMatrixTable
              obligations={filteredObligations}
              loading={obligationsLoading}
              onDownload={handleDownload}
              onRefresh={handleRefresh}
            />
          </CardBody>
        </Card>
      )}

      {/* Details Modal */}
      <Modal isOpen={isDetailsOpen} onClose={onDetailsClose} size="3xl">
        <ModalContent>
          <ModalHeader>Detalhes da Obrigação</ModalHeader>
          <ModalBody>
            {selectedObligation && (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-default-500">Cliente</p>
                    <p className="font-semibold">
                      {selectedObligation.client_name}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-default-500">CNPJ</p>
                    <p className="font-semibold">
                      {selectedObligation.client_cnpj}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-default-500">Obrigação</p>
                    <p className="font-semibold">
                      {selectedObligation.obligation_type_name}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-default-500">Código</p>
                    <p className="font-semibold">
                      {selectedObligation.obligation_type_code}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-default-500">Vencimento</p>
                    <p className="font-semibold">
                      {new Date(
                        selectedObligation.due_date
                      ).toLocaleDateString("pt-BR")}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-default-500">Status</p>
                    <p className="font-semibold">{selectedObligation.status}</p>
                  </div>
                </div>

                <div className="border-t border-divider pt-4">
                  <ObligationTimeline obligationId={selectedObligation.id} />
                </div>
              </div>
            )}
          </ModalBody>
          <ModalFooter>
            <Button variant="light" onPress={onDetailsClose}>
              Fechar
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      {/* Upload Receipt Modal */}
      <Modal isOpen={isUploadOpen} onClose={onUploadClose}>
        <ModalContent>
          <ModalHeader>Enviar Comprovante</ModalHeader>
          <ModalBody>
            <div className="space-y-4">
              <Input
                type="file"
                label="Arquivo"
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={(e) =>
                  setUploadFile(e.target.files?.[0] || null)
                }
              />
              <Textarea
                label="Observações (opcional)"
                placeholder="Digite observações sobre o comprovante"
                value={uploadNotes}
                onChange={(e) => setUploadNotes(e.target.value)}
              />
            </div>
          </ModalBody>
          <ModalFooter>
            <Button variant="light" onPress={onUploadClose}>
              Cancelar
            </Button>
            <Button
              color="primary"
              onPress={handleUploadSubmit}
              isDisabled={!uploadFile}
            >
              Enviar
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      {/* Cancel Modal */}
      <Modal isOpen={isCancelOpen} onClose={onCancelClose}>
        <ModalContent>
          <ModalHeader>Cancelar Obrigação</ModalHeader>
          <ModalBody>
            <Textarea
              label="Motivo do Cancelamento"
              placeholder="Digite o motivo do cancelamento"
              value={cancelReason}
              onChange={(e) => setCancelReason(e.target.value)}
              isRequired
            />
          </ModalBody>
          <ModalFooter>
            <Button variant="light" onPress={onCancelClose}>
              Voltar
            </Button>
            <Button
              color="danger"
              onPress={handleCancelSubmit}
              isDisabled={!cancelReason}
            >
              Cancelar Obrigação
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      {/* Generate Modal */}
      <Modal isOpen={isGenerateOpen} onClose={onGenerateClose}>
        <ModalContent>
          <ModalHeader>Gerar Obrigações</ModalHeader>
          <ModalBody>
            <div className="space-y-4">
              <Input
                type="number"
                label="Ano"
                value={generateYear.toString()}
                onChange={(e) => setGenerateYear(parseInt(e.target.value))}
              />
              <Select
                label="Mês"
                selectedKeys={generateMonth.toString()}
                onSelectionChange={(keys) => {
                  const value = Array.from(keys)[0] as string;
                  setGenerateMonth(parseInt(value) || currentDate.getMonth() + 1);
                }}
              >
                {MONTHS.map((month) => (
                  <SelectItem key={month.value.toString()}>
                    {month.label}
                  </SelectItem>
                ))}
              </Select>
              <p className="text-sm text-default-500">
                {activeTab === "client" && selectedClientId
                  ? "Serão geradas obrigações apenas para o cliente selecionado."
                  : "Serão geradas obrigações para todos os clientes ativos."}
              </p>
            </div>
          </ModalBody>
          <ModalFooter>
            <Button variant="light" onPress={onGenerateClose}>
              Cancelar
            </Button>
            <Button color="success" onPress={handleGenerateSubmit}>
              Gerar
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </div>
  );
}
