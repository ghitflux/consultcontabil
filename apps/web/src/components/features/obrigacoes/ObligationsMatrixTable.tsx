"use client";

import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Button,
  Progress,
  Tooltip,
  Spinner,
  Chip,
} from "@/heroui";
import { Obligation } from "@/hooks/useObligations";
import { DownloadIcon, RefreshIcon, ClockIcon, CheckCircleIcon } from "@/lib/icons";
import { formatCNPJ } from "@/lib/masks";

// Tipos de obrigações principais (baseado na imagem)
const OBLIGATION_TYPES = [
  { code: "DCTFWeb", name: "DCTFWeb" },
  { code: "EFD-Contribuições", name: "EFD-Contribuições" },
  { code: "ECD", name: "ECD" },
  { code: "ECF", name: "ECF" },
  { code: "ISS", name: "ISS" },
  { code: "FGTS", name: "FGTS" },
  { code: "INSS/eSocial", name: "INSS/eSocial" },
] as const;

interface CompanyObligations {
  client_id: string;
  client_name: string;
  client_cnpj: string;
  obligations: Obligation[];
}

interface ObligationsMatrixTableProps {
  obligations: Obligation[];
  loading?: boolean;
  onDownload?: (obligation: Obligation) => void;
  onRefresh?: (obligation: Obligation) => void;
}

export function ObligationsMatrixTable({
  obligations,
  loading = false,
  onDownload,
  onRefresh,
}: ObligationsMatrixTableProps) {
  // Agrupar obrigações por cliente
  const groupedByClient = obligations.reduce((acc, obligation) => {
    const key = obligation.client_id;
    if (!acc[key]) {
      acc[key] = {
        client_id: obligation.client_id,
        client_name: obligation.client_name,
        client_cnpj: obligation.client_cnpj,
        obligations: [],
      };
    }
    acc[key].obligations.push(obligation);
    return acc;
  }, {} as Record<string, CompanyObligations>);

  const companies = Object.values(groupedByClient);

  const getObligationByType = (
    companyObligations: Obligation[],
    typeCode: string
  ): Obligation | undefined => {
    return companyObligations.find(
      (ob) =>
        ob.obligation_type_code === typeCode ||
        ob.obligation_type_name === typeCode
    );
  };

  const getProgress = (companyObligations: Obligation[]) => {
    const total = OBLIGATION_TYPES.length;
    const completed = companyObligations.filter(
      (ob) => ob.status === "completed" || ob.status === "concluida"
    ).length;
    return { completed, total };
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
      case "concluida":
        return "success";
      case "pending":
      case "pendente":
        return "warning";
      case "cancelled":
      case "cancelada":
        return "default";
      case "atrasada":
        return "danger";
      default:
        return "default";
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <Spinner size="lg" />
      </div>
    );
  }

  if (companies.length === 0) {
    return (
      <div className="text-center p-8 text-default-400">
        <p className="text-4xl mb-2">📋</p>
        <p>Nenhuma obrigação encontrada</p>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-divider bg-content1">
      <div className="p-4 border-b border-divider">
        <p className="text-sm text-default-500">
          Clique em Baixar para marcar a obrigação como entregue. Você pode desfazer.
        </p>
      </div>
      <Table
        aria-label="Tabela de obrigações por empresa"
        classNames={{
          wrapper: "shadow-none",
          th: "bg-default-100 text-default-600 font-semibold",
        }}
      >
        <TableHeader>
          <TableColumn>EMPRESA / CNPJ</TableColumn>
          {OBLIGATION_TYPES.map((type) => (
            <TableColumn key={type.code}>{type.name}</TableColumn>
          ))}
          <TableColumn>PROGRESSO</TableColumn>
        </TableHeader>
        <TableBody>
          {companies.map((company) => {
            const progress = getProgress(company.obligations);
            return (
              <TableRow key={company.client_id}>
                <TableCell>
                  <div>
                    <p className="font-semibold text-default-900">
                      {company.client_name}
                    </p>
                    <p className="text-sm text-default-500">
                      {formatCNPJ(company.client_cnpj)}
                    </p>
                  </div>
                </TableCell>
                {OBLIGATION_TYPES.map((type) => {
                  const obligation = getObligationByType(
                    company.obligations,
                    type.code
                  );
                  if (!obligation) {
                    return (
                      <TableCell key={type.code}>
                        <span className="text-default-300">-</span>
                      </TableCell>
                    );
                  }

                  const isCompleted =
                    obligation.status === "completed" ||
                    obligation.status === "concluida";
                  const isPending =
                    obligation.status === "pending" ||
                    obligation.status === "pendente";

                  return (
                    <TableCell key={type.code}>
                      {isCompleted ? (
                        <Chip
                          color="success"
                          size="sm"
                          variant="flat"
                          startContent={<CheckCircleIcon className="h-4 w-4" />}
                        >
                          Entregue
                        </Chip>
                      ) : (
                        <div className="flex items-center gap-2">
                          <Button
                            size="sm"
                            color="primary"
                            variant="solid"
                            onPress={() => onDownload?.(obligation)}
                            startContent={<DownloadIcon className="h-4 w-4" />}
                          >
                            Baixar
                          </Button>
                          {onRefresh && (
                            <Tooltip content="Atualizar">
                              <Button
                                isIconOnly
                                size="sm"
                                variant="light"
                                onPress={() => onRefresh(obligation)}
                              >
                                <RefreshIcon className="h-4 w-4" />
                              </Button>
                            </Tooltip>
                          )}
                          {isPending && (
                            <Tooltip content="Pendente">
                              <ClockIcon className="h-4 w-4 text-default-400" />
                            </Tooltip>
                          )}
                        </div>
                      )}
                    </TableCell>
                  );
                })}
                <TableCell>
                  <div className="flex items-center gap-2">
                    <Progress
                      value={(progress.completed / progress.total) * 100}
                      className="flex-1"
                      color="primary"
                      size="sm"
                      showValueLabel={false}
                    />
                    <span className="text-sm text-default-600 min-w-[3rem] text-right">
                      {progress.completed}/{progress.total}
                    </span>
                  </div>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}
