"use client";

import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Chip,
  Button,
  Tooltip,
  Spinner,
} from "@/heroui";
import { Obligation } from "@/hooks/useObligations";

interface ObligationsTableProps {
  obligations: Obligation[];
  loading?: boolean;
  onViewDetails?: (obligation: Obligation) => void;
  onUploadReceipt?: (obligation: Obligation) => void;
  onCancel?: (obligation: Obligation) => void;
}

export function ObligationsTable({
  obligations,
  loading,
  onViewDetails,
  onUploadReceipt,
  onCancel,
}: ObligationsTableProps) {
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

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("pt-BR", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    }).format(date);
  };

  const isOverdue = (dueDate: string, status: string) => {
    if (status !== "pending") return false;
    const due = new Date(dueDate);
    const now = new Date();
    return due < now;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <Spinner size="lg" />
      </div>
    );
  }

  if (obligations.length === 0) {
    return (
      <div className="text-center p-8 text-default-400">
        <p className="text-4xl mb-2">📋</p>
        <p>Nenhuma obrigação encontrada</p>
      </div>
    );
  }

  return (
    <Table aria-label="Tabela de obrigações">
      <TableHeader>
        <TableColumn>CLIENTE</TableColumn>
        <TableColumn>OBRIGAÇÃO</TableColumn>
        <TableColumn>VENCIMENTO</TableColumn>
        <TableColumn>STATUS</TableColumn>
        <TableColumn>AÇÕES</TableColumn>
      </TableHeader>
      <TableBody>
        {obligations.map((obligation) => (
          <TableRow key={obligation.id}>
            <TableCell>
              <div>
                <p className="font-semibold">{obligation.client_name}</p>
                <p className="text-xs text-default-400">
                  {obligation.client_cnpj}
                </p>
              </div>
            </TableCell>
            <TableCell>
              <div>
                <p className="font-medium">{obligation.obligation_type_name}</p>
                <p className="text-xs text-default-400">
                  {obligation.obligation_type_code}
                </p>
              </div>
            </TableCell>
            <TableCell>
              <div>
                <p
                  className={
                    isOverdue(obligation.due_date, obligation.status)
                      ? "text-danger font-semibold"
                      : ""
                  }
                >
                  {formatDate(obligation.due_date)}
                </p>
                {isOverdue(obligation.due_date, obligation.status) && (
                  <p className="text-xs text-danger">Vencida</p>
                )}
              </div>
            </TableCell>
            <TableCell>
              <Chip
                color={getStatusColor(obligation.status) as any}
                size="sm"
                variant="flat"
              >
                {getStatusLabel(obligation.status)}
              </Chip>
            </TableCell>
            <TableCell>
              <div className="flex gap-2">
                {onViewDetails && (
                  <Tooltip content="Ver detalhes">
                    <Button
                      isIconOnly
                      size="sm"
                      variant="light"
                      onPress={() => onViewDetails(obligation)}
                    >
                      👁️
                    </Button>
                  </Tooltip>
                )}

                {onUploadReceipt && obligation.status === "pending" && (
                  <Tooltip content="Enviar comprovante">
                    <Button
                      isIconOnly
                      size="sm"
                      variant="light"
                      color="success"
                      onPress={() => onUploadReceipt(obligation)}
                    >
                      📎
                    </Button>
                  </Tooltip>
                )}

                {onCancel && obligation.status === "pending" && (
                  <Tooltip content="Cancelar">
                    <Button
                      isIconOnly
                      size="sm"
                      variant="light"
                      color="danger"
                      onPress={() => onCancel(obligation)}
                    >
                      ❌
                    </Button>
                  </Tooltip>
                )}

                {obligation.receipt_url && (
                  <Tooltip content="Ver comprovante">
                    <Button
                      isIconOnly
                      size="sm"
                      variant="light"
                      as="a"
                      href={obligation.receipt_url}
                      target="_blank"
                    >
                      📄
                    </Button>
                  </Tooltip>
                )}
              </div>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
