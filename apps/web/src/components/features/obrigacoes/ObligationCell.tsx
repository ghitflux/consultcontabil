"use client";

import React, { useState } from "react";
import { Button } from "@heroui/react";
import { CheckCircleIcon, RefreshIcon, DownloadIcon } from "@/lib/icons";
import type { ObligationData } from "@/hooks/useObligationsMatrix";
import { UploadReceiptModal } from "./UploadReceiptModal";

interface ObligationCellProps {
  obligation: ObligationData | null;
  onComplete: (file: File, notes?: string) => Promise<void>;
  onUndo: () => Promise<void>;
  onDownload?: () => void;
  clientName: string;
}

export function ObligationCell({
  obligation,
  onComplete,
  onUndo,
  onDownload,
  clientName
}: ObligationCellProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  if (!obligation) {
    // N/A - obrigação não se aplica
    return (
      <td className="px-2 py-3 text-center">
        <span className="text-default-400 text-sm">-</span>
      </td>
    );
  }

  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleUpload = async (file: File, notes?: string) => {
    try {
      setIsLoading(true);
      await onComplete(file, notes);
      setIsModalOpen(false);
    } catch (error) {
      console.error("Error uploading receipt:", error);
      throw error; // Propagar erro para o modal
    } finally {
      setIsLoading(false);
    }
  };

  const handleUndo = async () => {
    try {
      setIsLoading(true);
      await onUndo();
    } catch (error) {
      console.error("Error undoing obligation:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const isCompleted = obligation.status === "concluida";

  return (
    <>
      <td className="px-2 py-3 text-center">
        {!isCompleted ? (
          // Estado pendente: botão "Baixar" abre modal
          <Button
            size="sm"
            variant="flat"
            color="default"
            onPress={handleOpenModal}
            isLoading={isLoading}
            className="min-w-[80px]"
          >
            Baixar
          </Button>
        ) : (
          // Estado concluído: ícones de ação
          <div className="flex items-center justify-center gap-1">
            <Button
              isIconOnly
              size="sm"
              variant="light"
              color="success"
              className="min-w-unit-6"
              title="Concluída"
            >
              <CheckCircleIcon className="h-4 w-4" />
            </Button>
            <Button
              isIconOnly
              size="sm"
              variant="light"
              onPress={handleUndo}
              isLoading={isLoading}
              className="min-w-unit-6"
              title="Desfazer"
            >
              <RefreshIcon className="h-4 w-4" />
            </Button>
            {obligation.receipt_url && (
              <Button
                isIconOnly
                size="sm"
                variant="light"
                onPress={onDownload}
                className="min-w-unit-6"
                title="Baixar comprovante"
              >
                <DownloadIcon className="h-4 w-4" />
              </Button>
            )}
          </div>
        )}
      </td>

      {/* Modal de upload */}
      <UploadReceiptModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onUpload={handleUpload}
        obligationName={obligation.obligation_type_name || "Obrigação"}
        clientName={clientName}
      />
    </>
  );
}
