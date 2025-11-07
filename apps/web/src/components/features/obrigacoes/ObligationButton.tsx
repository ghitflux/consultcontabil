"use client";

import React, { useState } from "react";
import { Button, Tooltip } from "@heroui/react";
import { CheckCircleIcon, RefreshIcon, DownloadIcon } from "@/lib/icons";

interface ObligationData {
  id: string;
  status: string;
  receipt_url?: string;
  due_date?: string;
  obligation_type_name?: string;
}

interface ObligationButtonProps {
  obligation: ObligationData | null;
  obligationTypeName: string;
  clientName: string;
  onUpload: (obligationId: string) => void;
  onDownload: (receiptUrl: string) => void;
  onUndo: (obligationId: string) => void;
}

export function ObligationButton({
  obligation,
  obligationTypeName,
  clientName,
  onUpload,
  onDownload,
  onUndo,
}: ObligationButtonProps) {
  const [isLoading, setIsLoading] = useState(false);

  if (!obligation) {
    // N/A - obrigação não se aplica
    return (
      <td className="px-2 py-3 text-center">
        <span className="text-default-400 text-sm">-</span>
      </td>
    );
  }

  const isCompleted = obligation.status === "concluida";
  const formattedDate = obligation.due_date
    ? new Date(obligation.due_date).toLocaleDateString("pt-BR")
    : "";

  const handleUndo = async () => {
    try {
      setIsLoading(true);
      await onUndo(obligation.id);
    } catch (error) {
      console.error("Error undoing obligation:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <td className="px-2 py-3 text-center">
      {!isCompleted ? (
        <Tooltip content={`Vencimento: ${formattedDate}`}>
          <Button
            size="sm"
            variant="flat"
            color="default"
            onPress={() => onUpload(obligation.id)}
            isLoading={isLoading}
            className="min-w-[80px]"
          >
            Baixar
          </Button>
        </Tooltip>
      ) : (
        <div className="flex items-center justify-center gap-1">
          <Tooltip content={`Concluída em ${formattedDate}`}>
            <Button
              isIconOnly
              size="sm"
              variant="light"
              color="success"
              className="min-w-unit-6"
            >
              <CheckCircleIcon className="h-4 w-4" />
            </Button>
          </Tooltip>
          <Tooltip content="Desfazer baixa">
            <Button
              isIconOnly
              size="sm"
              variant="light"
              onPress={handleUndo}
              isLoading={isLoading}
              className="min-w-unit-6"
            >
              <RefreshIcon className="h-4 w-4" />
            </Button>
          </Tooltip>
          {obligation.receipt_url && (
            <Tooltip content="Baixar comprovante">
              <Button
                isIconOnly
                size="sm"
                variant="light"
                onPress={() => onDownload(obligation.receipt_url!)}
                className="min-w-unit-6"
              >
                <DownloadIcon className="h-4 w-4" />
              </Button>
            </Tooltip>
          )}
        </div>
      )}
    </td>
  );
}
