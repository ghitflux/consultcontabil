"use client";

import React, { useEffect, useState, useMemo } from "react";
import {
  Card,
  CardBody,
  CardHeader,
  Select,
  SelectItem,
  Spinner,
  Button,
  Chip,
  Progress,
  Input,
} from "@heroui/react";
import { SearchIcon, CalendarIcon, CheckCircleIcon, AlertCircleIcon } from "@/lib/icons";
import { useObligationsMatrix } from "@/hooks/useObligationsMatrix";
import { useObligations } from "@/hooks/useObligations";

export function ObligationsClientView() {
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [selectedClientId, setSelectedClientId] = useState<string>("");

  const { matrix, isLoading: matrixLoading, fetchMatrix } = useObligationsMatrix();

  const {
    obligations,
    loading: obligationsLoading,
    fetchObligations,
  } = useObligations({
    clientId: selectedClientId || undefined,
    year: selectedYear,
    month: selectedMonth,
    autoFetch: false,
  });

  // Buscar matriz para obter lista de clientes
  useEffect(() => {
    fetchMatrix(selectedMonth, selectedYear);
  }, [selectedMonth, selectedYear, fetchMatrix]);

  // Buscar obrigações do cliente selecionado
  useEffect(() => {
    if (selectedClientId) {
      fetchObligations();
    }
  }, [selectedClientId, selectedMonth, selectedYear, fetchObligations]);

  const handleMonthChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value) {
      const date = new Date(value);
      setSelectedMonth(date.getMonth() + 1);
      setSelectedYear(date.getFullYear());
    }
  };

  const currentMonthYear = `${selectedYear}-${selectedMonth.toString().padStart(2, "0")}`;

  const selectedClient = useMemo(() => {
    return matrix.find((c) => c.client_id === selectedClientId);
  }, [matrix, selectedClientId]);

  const stats = useMemo(() => {
    const total = obligations.length;
    const completed = obligations.filter((o) => o.status === "completed").length;
    const pending = total - completed;
    const percentage = total > 0 ? (completed / total) * 100 : 0;
    return { total, completed, pending, percentage };
  }, [obligations]);

  const formatDate = (dateStr: string) => {
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric" });
    } catch {
      return dateStr;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "success";
      case "pending":
        return "warning";
      case "cancelled":
        return "danger";
      default:
        return "default";
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case "completed":
        return "Concluída";
      case "pending":
        return "Pendente";
      case "cancelled":
        return "Cancelada";
      default:
        return status;
    }
  };

  return (
    <div className="space-y-6">
      {/* Filters */}
      <Card>
        <CardHeader className="flex flex-col gap-4 px-6 pt-6">
          <div className="flex flex-col sm:flex-row gap-4 w-full">
            <div className="flex flex-col gap-1 flex-1">
              <label className="text-sm text-default-600">Cliente</label>
              <Select
                placeholder="Selecione um cliente..."
                selectedKeys={selectedClientId ? [selectedClientId] : []}
                onSelectionChange={(keys) => {
                  const selected = Array.from(keys)[0];
                  setSelectedClientId(selected as string);
                }}
                size="sm"
                classNames={{
                  trigger: "h-10",
                }}
                isLoading={matrixLoading}
              >
                {matrix.map((client) => (
                  <SelectItem key={client.client_id}>
                    {client.client_name} - {client.client_cnpj}
                  </SelectItem>
                ))}
              </Select>
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-sm text-default-600">Competência</label>
              <Input
                type="month"
                value={currentMonthYear}
                onChange={handleMonthChange}
                size="sm"
                className="w-full sm:w-40"
              />
            </div>
          </div>

          {selectedClient && (
            <div className="flex items-center gap-4 p-4 bg-default-100 rounded-lg">
              <div className="flex-1">
                <h3 className="font-semibold text-lg">{selectedClient.client_name}</h3>
                <p className="text-sm text-default-600">{selectedClient.client_cnpj}</p>
              </div>
              <div className="flex flex-col items-end gap-1">
                <span className="text-2xl font-bold">{selectedClient.progress.completed}/{selectedClient.progress.total}</span>
                <span className="text-xs text-default-500">obrigações concluídas</span>
              </div>
            </div>
          )}
        </CardHeader>

        {selectedClient && (
          <CardBody className="px-6 pb-6">
            <Progress
              value={stats.percentage}
              color={stats.pending > 0 ? "warning" : "success"}
              size="sm"
              className="mb-2"
            />
            <div className="flex gap-4 text-sm">
              <span className="text-success-600 flex items-center gap-1">
                <CheckCircleIcon className="h-4 w-4" />
                {stats.completed} concluídas
              </span>
              <span className="text-warning-600 flex items-center gap-1">
                <AlertCircleIcon className="h-4 w-4" />
                {stats.pending} pendentes
              </span>
            </div>
          </CardBody>
        )}
      </Card>

      {/* Obligations List */}
      {!selectedClientId ? (
        <Card>
          <CardBody className="p-12 text-center text-default-500">
            <SearchIcon className="h-12 w-12 mx-auto mb-4 text-default-300" />
            <p>Selecione um cliente para ver suas obrigações</p>
          </CardBody>
        </Card>
      ) : obligationsLoading ? (
        <Card>
          <CardBody className="flex items-center justify-center p-12">
            <Spinner size="lg" />
          </CardBody>
        </Card>
      ) : obligations.length === 0 ? (
        <Card>
          <CardBody className="p-12 text-center text-default-500">
            <p>Nenhuma obrigação encontrada para este cliente</p>
          </CardBody>
        </Card>
      ) : (
        <div className="grid gap-4">
          {obligations.map((obligation) => (
            <Card key={obligation.id} className="hover:shadow-md transition-shadow">
              <CardBody className="p-6">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-start gap-3 mb-3">
                      <div className="flex-1">
                        <h4 className="font-semibold text-lg mb-1">
                          {obligation.obligation_type_name}
                        </h4>
                        <p className="text-sm text-default-600 mb-2">
                          Código: {obligation.obligation_type_code}
                        </p>
                        {obligation.description && (
                          <p className="text-sm text-default-500 italic">
                            {obligation.description}
                          </p>
                        )}
                      </div>
                      <Chip
                        color={getStatusColor(obligation.status)}
                        variant="flat"
                        size="sm"
                      >
                        {getStatusLabel(obligation.status)}
                      </Chip>
                    </div>

                    <div className="flex flex-wrap gap-4 text-sm text-default-600">
                      <div className="flex items-center gap-1">
                        <CalendarIcon className="h-4 w-4" />
                        <span>Vencimento: {formatDate(obligation.due_date)}</span>
                      </div>
                      {obligation.completed_at && (
                        <div className="flex items-center gap-1">
                          <CheckCircleIcon className="h-4 w-4 text-success" />
                          <span>Concluída em: {formatDate(obligation.completed_at)}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="flex flex-col gap-2">
                    {obligation.status === "pending" && (
                      <Button
                        size="sm"
                        color="primary"
                        onPress={() => {
                          // TODO: Abrir modal de upload
                          console.log("Upload receipt for", obligation.id);
                        }}
                      >
                        Anexar Comprovante
                      </Button>
                    )}
                    {obligation.receipt_url && (
                      <Button
                        size="sm"
                        variant="flat"
                        onPress={() => window.open(obligation.receipt_url, "_blank")}
                      >
                        Ver Comprovante
                      </Button>
                    )}
                  </div>
                </div>
              </CardBody>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
