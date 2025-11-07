"use client";

import { useState, useEffect } from "react";
import { Card, CardBody, Tabs, Tab, Input, Spinner, Button } from "@heroui/react";
import { SearchIcon, PlusIcon } from "@/lib/icons";
import { ObligationButton } from "@/components/features/obrigacoes/ObligationButton";
import { UploadReceiptModal } from "@/components/features/obrigacoes/UploadReceiptModal";
import { apiClient } from "@/lib/api/client";

type TabKey = "clients" | "office";

interface ObligationData {
  id: string;
  status: string;
  receipt_url?: string;
  due_date?: string;
  obligation_type_name?: string;
}

interface ClientRow {
  client_id: string;
  client_name: string;
  client_cnpj: string;
  obligations: Record<string, ObligationData | null>;
  progress: { completed: number; total: number };
}

const OBLIGATION_TYPES = [
  "DAS",
  "DCTFWeb",
  "EFD-Contribuições",
  "ECD",
  "ECF",
  "ISS",
  "FGTS",
  "INSS/eSocial",
];

export default function ObrigacoesPage() {
  const [activeTab, setActiveTab] = useState<TabKey>("clients");
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [searchQuery, setSearchQuery] = useState("");
  const [data, setData] = useState<ClientRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Upload modal state
  const [uploadModalOpen, setUploadModalOpen] = useState(false);
  const [selectedObligation, setSelectedObligation] = useState<{
    id: string;
    name: string;
    clientName: string;
  } | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const params = new URLSearchParams({
        month: selectedMonth.toString(),
        year: selectedYear.toString(),
        category: activeTab,
      });
      if (searchQuery) params.append("search", searchQuery);

      const response = await apiClient.get<ClientRow[]>(`/obligations/list?${params}`);
      setData(response);
    } catch (err) {
      console.error("Error fetching obligations:", err);
      setError("Erro ao carregar obrigações");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [selectedMonth, selectedYear, searchQuery, activeTab]);

  const handleMonthChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value) {
      const date = new Date(value);
      setSelectedMonth(date.getMonth() + 1);
      setSelectedYear(date.getFullYear());
    }
  };

  const handleUploadClick = (obligationId: string, typeName: string, clientName: string) => {
    setSelectedObligation({ id: obligationId, name: typeName, clientName });
    setUploadModalOpen(true);
  };

  const handleUpload = async (file: File, notes?: string) => {
    if (!selectedObligation) return;

    const formData = new FormData();
    formData.append("file", file);
    if (notes) formData.append("notes", notes);

    await apiClient.upload(`/obligations/${selectedObligation.id}/receipt`, formData);
    await fetchData();
  };

  const handleDownload = (receiptUrl: string) => {
    window.open(receiptUrl, "_blank");
  };

  const handleUndo = async (obligationId: string) => {
    await apiClient.post(`/obligations/${obligationId}/undo`, {});
    await fetchData();
  };

  const currentMonthYear = `${selectedYear}-${selectedMonth.toString().padStart(2, "0")}`;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Obrigações</h1>
        <p className="text-sm text-default-500 mt-1">
          Gerenciar e acompanhar obrigações fiscais
        </p>
      </div>

      {/* Tabs */}
      <Card>
        <CardBody>
          <Tabs
            selectedKey={activeTab}
            onSelectionChange={(key) => setActiveTab(key as TabKey)}
            color="primary"
            variant="underlined"
          >
            <Tab key="clients" title="Clientes">
              <div className="mt-6 space-y-4">
                {/* Filtros */}
                <div className="flex flex-col sm:flex-row gap-4">
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

                  <div className="flex flex-col gap-1 flex-1">
                    <label className="text-sm text-default-600">Buscar empresa</label>
                    <Input
                      placeholder="Buscar empresa..."
                      value={searchQuery}
                      onValueChange={setSearchQuery}
                      startContent={<SearchIcon className="h-4 w-4 text-default-400" />}
                      size="sm"
                    />
                  </div>

                  <div className="flex flex-col gap-1 justify-end">
                    <Button
                      color="primary"
                      startContent={<PlusIcon className="h-4 w-4" />}
                      size="sm"
                    >
                      Nova Obrigação
                    </Button>
                  </div>
                </div>

                {/* Dica */}
                <div className="text-sm text-default-500 p-3 bg-default-100 rounded-lg">
                  💡 <strong>Dica:</strong> Clique em <strong>Baixar</strong> para anexar o comprovante e marcar a obrigação como entregue. Você pode desfazer clicando no ícone de atualizar.
                </div>

                {/* Tabela */}
                {loading ? (
                  <div className="flex items-center justify-center p-12">
                    <Spinner size="lg" />
                  </div>
                ) : error ? (
                  <div className="text-center p-12 text-danger">{error}</div>
                ) : data.length === 0 ? (
                  <div className="text-center p-12 text-default-500">
                    Nenhuma empresa encontrada
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="w-full border-collapse">
                      <thead className="bg-default-100 border-b border-divider">
                        <tr>
                          <th className="px-4 py-3 text-left text-sm font-semibold sticky left-0 bg-default-100 z-10 min-w-[250px]">
                            Empresa / CNPJ
                          </th>
                          {OBLIGATION_TYPES.map((type) => (
                            <th key={type} className="px-2 py-3 text-center text-sm font-semibold min-w-[100px]">
                              {type}
                            </th>
                          ))}
                          <th className="px-4 py-3 text-center text-sm font-semibold min-w-[100px]">
                            Progresso
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {data.map((row) => (
                          <tr key={row.client_id} className="border-b border-divider hover:bg-default-50">
                            <td className="px-4 py-3 sticky left-0 bg-background z-10">
                              <div>
                                <p className="font-medium text-sm">{row.client_name}</p>
                                <p className="text-xs text-default-500">{row.client_cnpj}</p>
                              </div>
                            </td>
                            {OBLIGATION_TYPES.map((type) => (
                              <ObligationButton
                                key={`${row.client_id}-${type}`}
                                obligation={row.obligations[type] || null}
                                obligationTypeName={type}
                                clientName={row.client_name}
                                onUpload={(id) => handleUploadClick(id, type, row.client_name)}
                                onDownload={handleDownload}
                                onUndo={handleUndo}
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
              </div>
            </Tab>

            <Tab key="office" title="Escritório">
              <div className="mt-6 p-12 text-center text-default-500">
                <p>Obrigações do escritório (em desenvolvimento)</p>
              </div>
            </Tab>
          </Tabs>
        </CardBody>
      </Card>

      {/* Upload Modal */}
      {selectedObligation && (
        <UploadReceiptModal
          isOpen={uploadModalOpen}
          onClose={() => setUploadModalOpen(false)}
          onUpload={handleUpload}
          obligationName={selectedObligation.name}
          clientName={selectedObligation.clientName}
        />
      )}
    </div>
  );
}
