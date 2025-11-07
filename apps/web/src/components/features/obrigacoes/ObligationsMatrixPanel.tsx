"use client";

import React, { useEffect, useState } from "react";
import { Card, CardBody, CardHeader, Input, Spinner } from "@heroui/react";
import { SearchIcon } from "@/lib/icons";
import { useObligationsMatrix } from "@/hooks/useObligationsMatrix";
import { ObligationCell } from "./ObligationCell";

const OBLIGATION_TYPES = [
  "DCTFWeb",
  "EFD-Contribuições",
  "ECD",
  "ECF",
  "ISS",
  "FGTS",
  "INSS/eSocial",
];

export function ObligationsMatrixPanel() {
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [searchQuery, setSearchQuery] = useState("");

  const { matrix, isLoading, error, fetchMatrix, completeObligation, undoObligation, downloadReceipt } =
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

  const currentMonthYear = `${selectedYear}-${selectedMonth.toString().padStart(2, "0")}`;

  return (
    <div className="space-y-6">
      {/* Filters */}
      <Card>
        <CardHeader className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between px-6 pt-6">
          <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
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
          </div>
        </CardHeader>

        <CardBody className="px-6 pb-6">
          <div className="text-sm text-default-500 p-3 bg-default-100 rounded-lg">
            💡 <strong>Dica:</strong> Clique em <strong>Baixar</strong> para marcar a obrigação como entregue. Você pode desfazer clicando no ícone de atualizar.
          </div>
        </CardBody>
      </Card>

      {/* Matrix Table */}
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
                <thead className="bg-default-100 border-b border-divider">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-semibold sticky left-0 bg-default-100 z-10 min-w-[250px]">
                      Empresa / CNPJ
                    </th>
                    {OBLIGATION_TYPES.map((type) => (
                      <th key={type} className="px-2 py-3 text-center text-sm font-semibold min-w-[120px]">
                        {type}
                      </th>
                    ))}
                    <th className="px-4 py-3 text-center text-sm font-semibold min-w-[100px]">
                      Progresso
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {matrix.map((row) => (
                    <tr key={row.client_id} className="border-b border-divider hover:bg-default-50">
                      <td className="px-4 py-3 sticky left-0 bg-background z-10">
                        <div>
                          <p className="font-medium text-sm">{row.client_name}</p>
                          <p className="text-xs text-default-500">{row.client_cnpj}</p>
                        </div>
                      </td>
                      {row.obligations.map((obligation, index) => (
                        <ObligationCell
                          key={`${row.client_id}-${index}`}
                          obligation={obligation}
                          onComplete={() => obligation && completeObligation(obligation.id)}
                          onUndo={() => obligation && undoObligation(obligation.id)}
                          onDownload={() =>
                            obligation?.receipt_url && downloadReceipt(obligation.receipt_url)
                          }
                        />
                      ))}
                      <td className="px-4 py-3 text-center">
                        <div className="flex flex-col items-center gap-1">
                          <span className="text-sm font-medium">
                            {row.progress.completed}/{row.progress.total}
                          </span>
                          <div className="w-16 h-1.5 bg-default-200 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-success rounded-full transition-all"
                              style={{
                                width: `${row.progress.total > 0 ? (row.progress.completed / row.progress.total) * 100 : 0}%`,
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
