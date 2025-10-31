"use client";

import { useState, useEffect } from "react";
import {
  Card,
  CardHeader,
  CardBody,
  Divider,
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  Input,
  Textarea,
  Select,
  SelectItem,
  useDisclosure,
} from "@/heroui";
import { ObligationsTable } from "@/components/features/obrigacoes/ObligationsTable";
import { ObligationFilters } from "@/components/features/obrigacoes/ObligationFilters";
import { ObligationTimeline } from "@/components/features/obrigacoes/ObligationTimeline";
import { useObligations, Obligation } from "@/hooks/useObligations";
import { useClients } from "@/hooks/useClients";

export default function ObrigacoesPage() {
  const [selectedClientId, setSelectedClientId] = useState<string>("");
  const [selectedObligation, setSelectedObligation] =
    useState<Obligation | null>(null);

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
  const [generateYear, setGenerateYear] = useState(new Date().getFullYear());
  const [generateMonth, setGenerateMonth] = useState(new Date().getMonth() + 1);

  const { clients, isLoading: clientsLoading, fetchClients: fetchClientsData } = useClients();

  const {
    obligations,
    loading: obligationsLoading,
    uploadReceipt,
    cancelObligation,
    generateObligations,
  } = useObligations({
    clientId: selectedClientId,
    ...filters,
    autoFetch: !!selectedClientId,
  });

  // Fetch clients on mount
  useEffect(() => {
    fetchClientsData({ size: 100 });
  }, [fetchClientsData]);

  const handleViewDetails = (obligation: Obligation) => {
    setSelectedObligation(obligation);
    onDetailsOpen();
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
    } catch (error) {
      console.error("Error uploading receipt:", error);
    }
  };

  const handleCancelSubmit = async () => {
    if (!selectedObligation || !cancelReason) return;

    try {
      await cancelObligation(selectedObligation.id, cancelReason);
      onCancelClose();
    } catch (error) {
      console.error("Error cancelling obligation:", error);
    }
  };

  const handleGenerateSubmit = async () => {
    try {
      await generateObligations(
        generateYear,
        generateMonth,
        selectedClientId || undefined
      );
      onGenerateClose();
    } catch (error) {
      console.error("Error generating obligations:", error);
    }
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

      {/* Client Selector */}
      <Card>
        <CardBody>
          <Select
            label="Selecione um Cliente"
            placeholder="Escolha um cliente"
            value={selectedClientId}
            onChange={(e) => setSelectedClientId(e.target.value)}
            isLoading={clientsLoading}
          >
            {(clients?.items || []).map((client) => (
              <SelectItem key={client.id}>
                {client.razao_social} - {client.cnpj}
              </SelectItem>
            ))}
          </Select>
        </CardBody>
      </Card>

      {selectedClientId && (
        <>
          {/* Filters */}
          <Card>
            <CardBody>
              <ObligationFilters
                onFilterChange={setFilters}
                onGenerateClick={onGenerateOpen}
              />
            </CardBody>
          </Card>

          {/* Obligations Table */}
          <Card>
            <CardHeader>
              <h2 className="text-xl font-semibold">Lista de Obrigações</h2>
            </CardHeader>
            <Divider />
            <CardBody>
              <ObligationsTable
                obligations={obligations}
                loading={obligationsLoading}
                onViewDetails={handleViewDetails}
                onUploadReceipt={handleUploadReceipt}
                onCancel={handleCancelObligation}
              />
            </CardBody>
          </Card>
        </>
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

                <Divider />

                <ObligationTimeline obligationId={selectedObligation.id} />
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
                value={generateMonth.toString()}
                onChange={(e) => setGenerateMonth(parseInt(e.target.value))}
              >
                {Array.from({ length: 12 }, (_, i) => i + 1).map((month) => (
                  <SelectItem key={month.toString()}>
                    {new Date(2000, month - 1).toLocaleDateString("pt-BR", {
                      month: "long",
                    })}
                  </SelectItem>
                ))}
              </Select>
              <p className="text-sm text-default-500">
                {selectedClientId
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
