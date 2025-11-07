"use client";

import React, { useEffect, useState } from "react";
import { Card, CardBody, CardHeader, Input, Spinner, Chip } from "@heroui/react";
import { SearchIcon } from "@/lib/icons";
import { useObligationsMatrix } from "@/hooks/useObligationsMatrix";
import { ObligationCell } from "./ObligationCell";
import type { ObligationData } from "@/hooks/useObligationsMatrix";

const OBLIGATION_TYPES = [
  "DCTFWeb",
  "EFD-Contribuições",
  "ECD",
  "ECF",
  "ISS",
  "FGTS",
  "INSS/eSocial",
];

interface ObligationTypeRow {
  type: string;
  typeIndex: number;
  obligations: Array<{
    obligation: ObligationData | null;
    clientId: string;
    clientName: string;
    clientCnpj: string;
  }>;
  stats: {
    total: number;
    completed: number;
    pending: number;
  };
}

export function ObligationsOfficeView() {
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [searchQuery, setSearchQuery] = useState("");
  const [showOnlyPending, setShowOnlyPending] = useState(false);

  const { matrix, isLoading, error, fetchMatrix, uploadReceipt, undoObligation, downloadReceipt } =
    useObligationsMatrix();

  useEffect(() => {
    fetchMatrix(selectedMonth, selectedYear, searchQuery);
  }, [selectedMonth, selectedYear, searchQuery, fetchMatrix]);

  const handleMonthChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value) {
      const date = new Date(value);
      setSelectedMonth(date.getMonth() + 1);
      setSelectedYear(date.getFullYear());
    }
  };

  // Transpor matriz: tipos em linhas, clientes em colunas
  const transposeMatrix = (): ObligationTypeRow[] => {
    return OBLIGATION_TYPES.map((type, typeIndex) => {
      const obligations = matrix.map((clientRow) => ({
        obligation: clientRow.obligations[typeIndex] || null,
        clientId: clientRow.client_id,
        clientName: clientRow.client_name,
        clientCnpj: clientRow.client_cnpj,
      }));

      const stats = {
        total: obligations.filter((o) => o.obligation !== null).length,
        completed: obligations.filter((o) => o.obligation?.status === "concluida").length,
        pending: obligations.filter(
          (o) => o.obligation !== null && o.obligation?.status !== "concluida"
        ).length,
      };

      return { type, typeIndex, obligations, stats };
    });
  };

  const transposedMatrix = transposeMatrix();
  const filteredMatrix = showOnlyPending
    ? transposedMatrix.filter((row) => row.stats.pending > 0)
    : transposedMatrix;

  const currentMonthYear = `${selectedYear}-${selectedMonth.toString().padStart(2, "0")}`;

  return (
    <div className="space-y-6">
      {/* Filters */}
      <Card>
        <CardHeader className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between px-6 pt-6">
          <div className="flex flex-col sm:flex-row gap-4 w-full">
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

            <div className="flex flex-col gap-1 flex-1 sm:flex-initial">
              <label className="text-sm text-default-600">Buscar empresa</label>
              <Input
                placeholder="Buscar empresa..."
                value={searchQuery}
                onValueChange={setSearchQuery}
                startContent={<SearchIcon className="h-4 w-4 text-default-400" />}
                size="sm"
                className="w-full sm:w-64"
              />
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-sm text-default-600">Filtros</label>
              <div className="flex gap-2">
                <Chip
                  variant={showOnlyPending ? "solid" : "flat"}
                  color={showOnlyPending ? "primary" : "default"}
                  onClick={() => setShowOnlyPending(!showOnlyPending)}
                  className="cursor-pointer"
                >
                  Apenas pendentes
                </Chip>
              </div>
            </div>
          </div>
        </CardHeader>

        <CardBody className="px-6 pb-6">
          <div className="text-sm text-default-500 p-3 bg-default-100 rounded-lg">
            💡 <strong>Dica:</strong> Esta visão mostra todas as obrigações do escritório agrupadas por tipo.
            Use para identificar rapidamente quais tipos de obrigações têm mais pendências.
          </div>
        </CardBody>
      </Card>

      {/* Office View Table */}
      <Card>
        <CardBody className="p-0">
          {isLoading ? (
            <div className="flex items-center justify-center p-12">
              <Spinner size="lg" />
            </div>
          ) : error ? (
            <div className="text-center p-12 text-danger">{error}</div>
          ) : matrix.length === 0 ? (
            <div className="text-center p-12 text-default-500">
              Nenhuma empresa encontrada
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-default-100 border-b border-divider sticky top-0 z-20">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-semibold sticky left-0 bg-default-100 z-30 min-w-[200px]">
                      Tipo de Obrigação
                    </th>
                    {matrix.map((client) => (
                      <th key={client.client_id} className="px-2 py-3 text-center text-sm font-semibold min-w-[120px]">
                        <div className="flex flex-col items-center">
                          <span className="line-clamp-2" title={client.client_name}>
                            {client.client_name}
                          </span>
                          <span className="text-xs text-default-400 font-normal">
                            {client.client_cnpj}
                          </span>
                        </div>
                      </th>
                    ))}
                    <th className="px-4 py-3 text-center text-sm font-semibold min-w-[120px]">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {filteredMatrix.map((row) => (
                    <tr key={row.type} className="border-b border-divider hover:bg-default-50">
                      <td className="px-4 py-3 sticky left-0 bg-background z-10">
                        <div className="flex flex-col gap-1">
                          <span className="font-medium text-sm">{row.type}</span>
                          <div className="flex gap-2 text-xs">
                            <span className="text-success-600">{row.stats.completed} concluídas</span>
                            <span className="text-warning-600">{row.stats.pending} pendentes</span>
                          </div>
                        </div>
                      </td>
                      {row.obligations.map((item, index) => (
                        <ObligationCell
                          key={`${row.type}-${item.clientId}-${index}`}
                          obligation={item.obligation}
                          clientName={item.clientName}
                          onComplete={async (file, notes) => {
                            if (item.obligation) {
                              await uploadReceipt(item.obligation.id, file, notes);
                            }
                          }}
                          onUndo={async () => {
                            if (item.obligation) {
                              await undoObligation(item.obligation.id);
                            }
                          }}
                          onDownload={() =>
                            item.obligation?.receipt_url && downloadReceipt(item.obligation.receipt_url)
                          }
                        />
                      ))}
                      <td className="px-4 py-3 text-center">
                        <div className="flex flex-col items-center gap-1">
                          <span className="text-sm font-medium">
                            {row.stats.completed}/{row.stats.total}
                          </span>
                          <div className="w-16 h-1.5 bg-default-200 rounded-full overflow-hidden">
                            <div
                              className={`h-full rounded-full transition-all ${
                                row.stats.pending > 0 ? "bg-warning" : "bg-success"
                              }`}
                              style={{
                                width: `${row.stats.total > 0 ? (row.stats.completed / row.stats.total) * 100 : 0}%`,
                              }}
                            />
                          </div>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardBody>
      </Card>
    </div>
  );
}
