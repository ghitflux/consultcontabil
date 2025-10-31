"use client";

import {
  Card,
  CardBody,
  CardHeader,
  Button,
  Input,
  Select,
  SelectItem,
  Spinner,
  Divider,
  Chip,
  Switch,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  Textarea,
  useDisclosure,
} from "@/heroui";
import { useEffect, useMemo, useState } from "react";
import { useReportPreview } from "@/hooks/useReportPreview";
import { useReportExport } from "@/hooks/useReportExport";
import type {
  ReportTemplate,
  ReportTemplateCreate,
  ReportType,
  ReportTypeInfo,
} from "@/types/report";
import { ReportFormat } from "@/types/report";
import { format } from "date-fns";
import { ReportPreviewRenderer } from "./ReportPreviewRenderer";
import { clientsApi } from "@/lib/api/endpoints/clients";
import type { ClientListItem } from "@/types/client";
import {
  ArrowRightIcon,
  ArrowLeftIcon,
  EyeIcon,
  DownloadIcon,
  SaveIcon,
  RefreshIcon,
  TrashIcon,
  DollarSignIcon,
  BarChartIcon,
} from "@/lib/icons";

interface InitialSelection {
  reportType?: ReportType | null;
  template?: ReportTemplate | null;
}

interface ReportBuilderProps {
  reportTypes: ReportTypeInfo[];
  templates: ReportTemplate[];
  templatesLoading: boolean;
  isTemplateMutating: boolean;
  onRefreshTemplates: (
    includeSystem?: boolean
  ) => Promise<ReportTemplate[] | void>;
  onCreateTemplate: (data: ReportTemplateCreate) => Promise<ReportTemplate>;
  onDeleteTemplate: (id: string) => Promise<void>;
  onReportExported?: () => void;
  initialSelection?: InitialSelection | null;
  consumeInitialSelection?: () => void;
}

const getDefaultFilename = (type: ReportType) =>
  `${type}_${format(new Date(), "yyyy-MM-dd")}`;

export function ReportBuilder({
  reportTypes,
  templates,
  templatesLoading,
  isTemplateMutating,
  onRefreshTemplates,
  onCreateTemplate,
  onDeleteTemplate,
  onReportExported,
  initialSelection,
  consumeInitialSelection,
}: ReportBuilderProps) {
  const {
    previewReport,
    preview,
    isLoading: previewLoading,
    clearPreview,
    error: previewError,
  } = useReportPreview();
  const {
    exportReport,
    isExporting,
    downloadReport,
    error: exportError,
  } = useReportExport();

  const [step, setStep] = useState(1);
  const [selectedType, setSelectedType] = useState<ReportType | null>(null);
  const [selectedTemplateId, setSelectedTemplateId] = useState<string | null>(
    null
  );

  const [periodStart, setPeriodStart] = useState<string>(
    format(new Date(new Date().getFullYear(), 0, 1), "yyyy-MM-dd")
  );
  const [periodEnd, setPeriodEnd] = useState<string>(
    format(new Date(), "yyyy-MM-dd")
  );
  const [clientIds, setClientIds] = useState<string[]>([]);
  const [includeSummary, setIncludeSummary] = useState(true);
  const [includeCharts, setIncludeCharts] = useState(true);
  const [formatOption, setFormatOption] = useState<ReportFormat>(
    ReportFormat.PDF
  );
  const [filename, setFilename] = useState<string>("");

  const [clients, setClients] = useState<ClientListItem[]>([]);
  const [clientsLoading, setClientsLoading] = useState(false);
  const [clientsError, setClientsError] = useState<string | null>(null);

  const {
    isOpen: isTemplateModalOpen,
    onOpen: onOpenTemplateModal,
    onClose: onCloseTemplateModal,
  } = useDisclosure();
  const [templateName, setTemplateName] = useState("");
  const [templateDescription, setTemplateDescription] = useState("");

  const selectedTypeInfo = reportTypes.find((t) => t.type === selectedType);

  useEffect(() => {
    let active = true;
    const loadClients = async () => {
      setClientsLoading(true);
      setClientsError(null);
      try {
        const response = await clientsApi.list({ page: 1, size: 50 });
        if (active) {
          setClients(response.items ?? []);
        }
      } catch (error) {
        console.error("Failed to fetch clients for report builder:", error);
        if (active) {
          setClientsError("Não foi possível carregar a lista de clientes.");
        }
      } finally {
        if (active) {
          setClientsLoading(false);
        }
      }
    };

    loadClients();
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (!initialSelection) return;

    if (initialSelection.template) {
      applyTemplate(initialSelection.template);
      setStep(2);
      consumeInitialSelection?.();
      return;
    }

    if (initialSelection.reportType) {
      setSelectedTemplateId(null);
      setSelectedType(initialSelection.reportType);
      setFilename(getDefaultFilename(initialSelection.reportType));
      setStep(2);
      consumeInitialSelection?.();
    }
  }, [initialSelection, consumeInitialSelection]);

  const sortedTemplates = useMemo(
    () =>
      [...templates].sort((a, b) => {
        if (a.is_system === b.is_system) {
          return a.name.localeCompare(b.name);
        }
        return a.is_system ? -1 : 1;
      }),
    [templates]
  );

  const clientOptions = useMemo(
    () =>
      clients.map((client) => ({
        key: client.id,
        label: client.razao_social,
      })),
    [clients]
  );

  const applyTemplate = (template: ReportTemplate) => {
    setSelectedTemplateId(template.id);
    setSelectedType(template.report_type);
    setFilename(getDefaultFilename(template.report_type));

    const filters = template.default_filters ?? {};
    if (typeof filters.period_start === "string") {
      setPeriodStart(filters.period_start);
    }
    if (typeof filters.period_end === "string") {
      setPeriodEnd(filters.period_end);
    }
    if (Array.isArray(filters.client_ids)) {
      setClientIds(filters.client_ids.filter(Boolean));
    } else {
      setClientIds([]);
    }

    const custom = template.default_customizations ?? {};
    if (typeof custom.include_summary === "boolean") {
      setIncludeSummary(custom.include_summary);
    } else {
      setIncludeSummary(true);
    }
    if (typeof custom.include_charts === "boolean") {
      setIncludeCharts(custom.include_charts);
    } else {
      setIncludeCharts(true);
    }
  };

  const handleTypeSelect = (type: ReportType) => {
    setSelectedTemplateId(null);
    setSelectedType(type);
    setFilename(getDefaultFilename(type));
    setIncludeSummary(true);
    setIncludeCharts(true);
    setClientIds([]);
  };

  const handlePreview = async () => {
    if (!selectedType) return;

    try {
      await previewReport({
        report_type: selectedType,
        filters: {
          period_start: periodStart,
          period_end: periodEnd,
          report_type: selectedType,
          client_ids: clientIds.length > 0 ? clientIds : null,
        },
        customizations: {
          include_summary: includeSummary,
          include_charts: includeCharts,
        },
      });
      setStep(3);
    } catch (error) {
      console.error("Error generating preview:", error);
    }
  };

  const handleExport = async () => {
    if (!selectedType) return;

    try {
      const result = await exportReport({
        report_type: selectedType,
        format: formatOption,
        filters: {
          period_start: periodStart,
          period_end: periodEnd,
          report_type: selectedType,
          client_ids: clientIds.length > 0 ? clientIds : null,
        },
        customizations: {
          include_summary: includeSummary,
          include_charts: includeCharts,
        },
        filename: filename || undefined,
      });

      if (result) {
        await downloadReport(result.report_id, result.file_name);
        onReportExported?.();
      }
    } catch (error) {
      console.error("Error exporting report:", error);
    }
  };

  const handleSaveTemplate = async () => {
    if (!selectedType || !templateName.trim()) return;

    try {
      await onCreateTemplate({
        name: templateName.trim(),
        description: templateDescription.trim() || null,
        report_type: selectedType,
        default_filters: {
          period_start: periodStart,
          period_end: periodEnd,
          report_type: selectedType,
          client_ids: clientIds.length > 0 ? clientIds : null,
        },
        default_customizations: {
          include_summary: includeSummary,
          include_charts: includeCharts,
        },
      });
      await onRefreshTemplates();
      setTemplateName("");
      setTemplateDescription("");
      onCloseTemplateModal();
    } catch (error) {
      console.error("Failed to create template:", error);
    }
  };

  const handleDeleteTemplate = async (template: ReportTemplate) => {
    try {
      await onDeleteTemplate(template.id);
      await onRefreshTemplates();
      if (selectedTemplateId === template.id) {
        setSelectedTemplateId(null);
      }
    } catch (error) {
      console.error("Failed to delete template:", error);
    }
  };

  return (
    <div className="space-y-6 mt-6">
      {/* Step Indicator */}
      <div className="flex items-center gap-2">
        <div
          className={`flex items-center justify-center w-8 h-8 rounded-full ${
            step >= 1 ? "bg-primary text-white" : "bg-default-200"
          }`}
        >
          1
        </div>
        <div className="flex-1 h-1 bg-default-200">
          <div
            className={`h-full transition-all ${
              step >= 2 ? "bg-primary" : ""
            }`}
            style={{ width: step >= 2 ? "100%" : "0%" }}
          />
        </div>
        <div
          className={`flex items-center justify-center w-8 h-8 rounded-full ${
            step >= 2 ? "bg-primary text-white" : "bg-default-200"
          }`}
        >
          2
        </div>
        <div className="flex-1 h-1 bg-default-200">
          <div
            className={`h-full transition-all ${
              step >= 3 ? "bg-primary" : ""
            }`}
            style={{ width: step >= 3 ? "100%" : "0%" }}
          />
        </div>
        <div
          className={`flex items-center justify-center w-8 h-8 rounded-full ${
            step >= 3 ? "bg-primary text-white" : "bg-default-200"
          }`}
        >
          3
        </div>
      </div>

      {/* Step 1: Select Report Type & Template */}
      {step === 1 && (
        <div className="grid gap-4 lg:grid-cols-[2fr,1fr]">
          <Card>
            <CardHeader>
              <h3 className="text-lg font-semibold">
                Selecione o Tipo de Relatório
              </h3>
            </CardHeader>
            <CardBody>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {reportTypes.map((type) => (
                  <Button
                    key={type.type}
                    variant={selectedType === type.type ? "solid" : "bordered"}
                    color={selectedType === type.type ? "primary" : "default"}
                    className="h-auto p-4 flex-col items-start text-left gap-2"
                    onPress={() => handleTypeSelect(type.type)}
                  >
                    <div className="font-semibold">{type.name}</div>
                    <div className="text-xs text-default-500">
                      {type.description}
                    </div>
                    <div className="text-xs text-default-400">
                      {type.category === "financeiro"
                        ? "💰 Financeiro"
                        : "⚙️ Operacional"}
                    </div>
                  </Button>
                ))}
              </div>
              <div className="mt-6 flex justify-end">
                <Button
                  color="primary"
                  onPress={() => selectedType && setStep(2)}
                  isDisabled={!selectedType}
                  endContent={<ArrowRightIcon className="h-4 w-4" />}
                >
                  Próximo
                </Button>
              </div>
            </CardBody>
          </Card>

          <Card>
            <CardHeader className="flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">Templates Salvos</h3>
                <Button
                  size="sm"
                  variant="light"
                  onPress={() => {
                    void onRefreshTemplates();
                  }}
                  isLoading={templatesLoading}
                  startContent={<RefreshIcon className="h-4 w-4" />}
                >
                  Atualizar
                </Button>
              </div>
              <p className="text-xs text-default-500">
                Aplique configurações pré-definidas ou salve novos templates no
                passo 3.
              </p>
            </CardHeader>
            <CardBody className="space-y-3">
              {templatesLoading ? (
                <div className="flex justify-center py-6">
                  <Spinner />
                </div>
              ) : sortedTemplates.length === 0 ? (
                <p className="text-sm text-default-500">
                  Nenhum template disponível ainda.
                </p>
              ) : (
                sortedTemplates.map((template) => (
                  <div
                    key={template.id}
                    className={`border border-divider rounded-lg p-3 space-y-2 ${
                      selectedTemplateId === template.id
                        ? "border-primary"
                        : ""
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <div className="flex items-center gap-2">
                          <h4 className="font-medium">{template.name}</h4>
                          <Chip
                            size="sm"
                            color={template.is_system ? "default" : "primary"}
                            variant="flat"
                          >
                            {template.is_system ? "Sistema" : "Personalizado"}
                          </Chip>
                        </div>
                        {template.description && (
                          <p className="text-xs text-default-500 mt-1">
                            {template.description}
                          </p>
                        )}
                      </div>
                      <div className="flex gap-2">
                        {!template.is_system && (
                          <Button
                            size="sm"
                            variant="light"
                            color="danger"
                            onPress={() => handleDeleteTemplate(template)}
                            isDisabled={isTemplateMutating}
                            startContent={<TrashIcon className="h-4 w-4" />}
                            isIconOnly
                          />
                        )}
                        <Button
                          size="sm"
                          variant="flat"
                          onPress={() => {
                            applyTemplate(template);
                            setStep(2);
                          }}
                        >
                          Aplicar
                        </Button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </CardBody>
          </Card>
        </div>
      )}

      {/* Step 2: Configure Filters */}
      {step === 2 && (
        <Card>
          <CardHeader className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
            <div>
              <h3 className="text-lg font-semibold">Configurar Filtros</h3>
              {selectedTypeInfo && (
                <p className="text-sm text-default-500">
                  {selectedTypeInfo.name}
                </p>
              )}
            </div>
            {selectedTemplateId && (
              <Chip size="sm" color="primary" variant="flat">
                Template aplicado
              </Chip>
            )}
          </CardHeader>
          <CardBody className="space-y-5">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                type="date"
                label="Data Inicial"
                value={periodStart}
                onValueChange={setPeriodStart}
              />
              <Input
                type="date"
                label="Data Final"
                value={periodEnd}
                onValueChange={setPeriodEnd}
              />
            </div>

            <Select
              label="Filtrar por Clientes (opcional)"
              placeholder={
                clientsLoading
                  ? "Carregando clientes..."
                  : "Selecione clientes"
              }
              selectionMode="multiple"
              selectedKeys={new Set(clientIds)}
              onSelectionChange={(keys) =>
                setClientIds(Array.from(keys) as string[])
              }
              isDisabled={clientsLoading || !!clientsError}
            >
              {clientOptions.map((client) => (
                <SelectItem key={client.key}>{client.label}</SelectItem>
              ))}
            </Select>
            {clientsError && (
              <p className="text-xs text-danger">{clientsError}</p>
            )}

            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div className="flex items-center gap-4">
                <Switch
                  isSelected={includeSummary}
                  onValueChange={setIncludeSummary}
                >
                  Incluir resumo executivo
                </Switch>
                <Switch
                  isSelected={includeCharts}
                  onValueChange={setIncludeCharts}
                >
                  Incluir gráficos
                </Switch>
              </div>
              {selectedTypeInfo?.required_permissions?.includes("admin") && (
                <Chip color="warning" variant="flat" size="sm">
                  Requer permissões de administrador
                </Chip>
              )}
            </div>

            {(previewError || exportError) && (
              <p className="text-xs text-danger">
                {previewError || exportError}
              </p>
            )}

            <Divider />

            <div className="flex gap-4 justify-end">
              <Button variant="bordered" onPress={() => setStep(1)} startContent={<ArrowLeftIcon className="h-4 w-4" />}>
                Voltar
              </Button>
              <Button
                color="primary"
                onPress={handlePreview}
                isLoading={previewLoading}
                isDisabled={!selectedType}
                endContent={<EyeIcon className="h-4 w-4" />}
              >
                Visualizar Preview
              </Button>
            </div>
          </CardBody>
        </Card>
      )}

      {/* Step 3: Preview & Export */}
      {step === 3 && (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold">Preview do Relatório</h3>
                <Button variant="bordered" size="sm" onPress={clearPreview}>
                  Limpar
                </Button>
              </div>
            </CardHeader>
            <CardBody>
              <ReportPreviewRenderer
                preview={preview}
                isLoading={previewLoading}
              />
            </CardBody>
          </Card>

          <Card>
            <CardHeader className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
              <h3 className="text-lg font-semibold">Exportar Relatório</h3>
              <Button
                variant="light"
                size="sm"
                onPress={onOpenTemplateModal}
                isDisabled={!selectedType}
                startContent={<SaveIcon className="h-4 w-4" />}
              >
                Salvar como Template
              </Button>
            </CardHeader>
            <CardBody className="space-y-4">
              <Select
                label="Formato"
                selectedKeys={[formatOption]}
                onSelectionChange={(keys) => {
                  const selected = Array.from(keys)[0] as ReportFormat;
                  setFormatOption(selected);
                }}
              >
                <SelectItem key={ReportFormat.PDF}>PDF</SelectItem>
                <SelectItem key={ReportFormat.CSV}>CSV</SelectItem>
              </Select>

              <Input
                label="Nome do Arquivo (opcional)"
                value={filename}
                onValueChange={setFilename}
                placeholder={
                  selectedType
                    ? getDefaultFilename(selectedType)
                    : "relatorio-personalizado"
                }
              />

              <div className="flex gap-4 justify-end">
                <Button variant="bordered" onPress={() => setStep(2)} startContent={<ArrowLeftIcon className="h-4 w-4" />}>
                  Voltar
                </Button>
                <Button
                  color="primary"
                  onPress={handleExport}
                  isLoading={isExporting}
                  isDisabled={!selectedType}
                  endContent={<DownloadIcon className="h-4 w-4" />}
                >
                  Exportar
                </Button>
              </div>
            </CardBody>
          </Card>
        </div>
      )}

      <Modal isOpen={isTemplateModalOpen} onClose={onCloseTemplateModal}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader>Salvar como Template</ModalHeader>
              <ModalBody className="space-y-4">
                <Input
                  label="Nome do Template"
                  value={templateName}
                  onValueChange={setTemplateName}
                  isRequired
                />
                <Textarea
                  label="Descrição (opcional)"
                  value={templateDescription}
                  onValueChange={setTemplateDescription}
                  minRows={3}
                />
                <p className="text-xs text-default-500">
                  O template salvará os filtros atuais, incluindo período,
                  clientes selecionados e preferências de resumo/gráficos.
                </p>
              </ModalBody>
              <ModalFooter>
                <Button variant="light" onPress={onClose}>
                  Cancelar
                </Button>
                <Button
                  color="primary"
                  onPress={handleSaveTemplate}
                  isDisabled={!selectedType || !templateName.trim()}
                  isLoading={isTemplateMutating}
                >
                  Salvar Template
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </div>
  );
}
