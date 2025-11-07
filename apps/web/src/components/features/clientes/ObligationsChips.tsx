"use client";

import React from "react";
import { Chip, Button } from "@heroui/react";
import { PlusIcon } from "@/lib/icons";
import type { Obligation } from "@/types/client";

interface ObligationsChipsProps {
  obligations: Obligation[];
  onRemove: (index: number) => void;
  onAdd?: () => void;
  readonly?: boolean;
}

export function ObligationsChips({ obligations, onRemove, onAdd, readonly = false }: ObligationsChipsProps) {
  if (obligations.length === 0 && readonly) {
    return <p className="text-sm text-gray-500">Nenhuma obrigação selecionada</p>;
  }

  return (
    <div className="flex flex-wrap gap-2">
      {obligations.map((obligation, index) => (
        <Chip
          key={`${obligation.nome}-${index}`}
          onClose={readonly ? undefined : () => onRemove(index)}
          variant="flat"
          color={obligation.periodicidade === "mensal" ? "primary" : "secondary"}
        >
          {obligation.nome}
        </Chip>
      ))}
      {!readonly && onAdd && (
        <Button
          size="sm"
          variant="bordered"
          startContent={<PlusIcon className="h-4 w-4" />}
          onClick={onAdd}
        >
          Adicionar
        </Button>
      )}
    </div>
  );
}

interface ObligationsGroupedProps {
  obligations: Obligation[];
  onRemove: (index: number) => void;
  readonly?: boolean;
}

export function ObligationsGrouped({ obligations, onRemove, readonly = false }: ObligationsGroupedProps) {
  // Group obligations by type and periodicidade
  const grouped = React.useMemo(() => {
    const result: Record<string, Obligation[]> = {
      fiscal_mensal: [],
      fiscal_anual: [],
      contabil_mensal: [],
      contabil_anual: [],
      pessoal_mensal: [],
      pessoal_anual: [],
    };

    obligations.forEach((obligation) => {
      const key = `${obligation.tipo}_${obligation.periodicidade}`;
      if (result[key]) {
        result[key].push(obligation);
      }
    });

    return result;
  }, [obligations]);

  const sections = [
    { key: "fiscal_mensal", label: "Fiscais — Mensal", color: "primary" as const },
    { key: "fiscal_anual", label: "Fiscais — Anual", color: "primary" as const },
    { key: "contabil_mensal", label: "Contábeis — Mensal", color: "success" as const },
    { key: "contabil_anual", label: "Contábeis — Anual", color: "success" as const },
    { key: "pessoal_mensal", label: "Trabalhistas — Mensal", color: "warning" as const },
    { key: "pessoal_anual", label: "Trabalhistas — Anual", color: "warning" as const },
  ];

  return (
    <div className="space-y-4">
      {sections.map(({ key, label, color }) => {
        const items = grouped[key];
        if (!items || items.length === 0) return null;

        return (
          <div key={key}>
            <p className="text-sm font-medium text-gray-700 mb-2">{label}</p>
            <div className="flex flex-wrap gap-2">
              {items.map((obligation) => {
                // Find global index
                const globalIndex = obligations.findIndex((o) => o === obligation);
                return (
                  <Chip
                    key={`${obligation.nome}-${globalIndex}`}
                    onClose={readonly ? undefined : () => onRemove(globalIndex)}
                    variant="flat"
                    color={color}
                  >
                    {obligation.nome}
                  </Chip>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}
