"use client";

import { Select, SelectItem, Button } from "@/heroui";
import { useState } from "react";

interface ObligationFiltersProps {
  onFilterChange?: (filters: {
    status?: string;
    year?: number;
    month?: number;
  }) => void;
  onGenerateClick?: () => void;
}

export function ObligationFilters({
  onFilterChange,
  onGenerateClick,
}: ObligationFiltersProps) {
  const [status, setStatus] = useState<string>("all");
  const [year, setYear] = useState<string>("all");
  const [month, setMonth] = useState<string>("all");

  const currentYear = new Date().getFullYear();
  const yearItems = [
    { key: "all", label: "Todos" },
    ...Array.from({ length: 5 }, (_, i) => {
      const year = currentYear - 2 + i;
      return { key: year.toString(), label: year.toString() };
    }),
  ];
  const monthItems = [
    { key: "all", label: "Todos" },
    { key: "1", label: "Janeiro" },
    { key: "2", label: "Fevereiro" },
    { key: "3", label: "Março" },
    { key: "4", label: "Abril" },
    { key: "5", label: "Maio" },
    { key: "6", label: "Junho" },
    { key: "7", label: "Julho" },
    { key: "8", label: "Agosto" },
    { key: "9", label: "Setembro" },
    { key: "10", label: "Outubro" },
    { key: "11", label: "Novembro" },
    { key: "12", label: "Dezembro" },
  ];

  const handleApplyFilters = () => {
    onFilterChange?.({
      status: status && status !== "all" ? status : undefined,
      year: year && year !== "all" ? parseInt(year) : undefined,
      month: month && month !== "all" ? parseInt(month) : undefined,
    });
  };

  const handleClearFilters = () => {
    setStatus("all");
    setYear("all");
    setMonth("all");
    onFilterChange?.({});
  };

  return (
    <div className="flex flex-wrap gap-4 items-end">
      <Select
        label="Status"
        placeholder="Todos"
        className="w-40"
        value={status}
        onChange={(e) => setStatus(e.target.value)}
      >
        <SelectItem key="all">
          Todos
        </SelectItem>
        <SelectItem key="pending">
          Pendente
        </SelectItem>
        <SelectItem key="completed">
          Concluída
        </SelectItem>
        <SelectItem key="cancelled">
          Cancelada
        </SelectItem>
      </Select>

      <Select
        label="Ano"
        placeholder="Todos"
        className="w-32"
        selectedKeys={year ? [year] : []}
        onSelectionChange={(keys) => setYear(Array.from(keys)[0] as string)}
        items={yearItems}
      >
        {(item) => <SelectItem key={item.key}>{item.label}</SelectItem>}
      </Select>

      <Select
        label="Mês"
        placeholder="Todos"
        className="w-40"
        selectedKeys={month ? [month] : []}
        onSelectionChange={(keys) => setMonth(Array.from(keys)[0] as string)}
        items={monthItems}
      >
        {(item) => <SelectItem key={item.key}>{item.label}</SelectItem>}
      </Select>

      <div className="flex gap-2">
        <Button color="primary" onPress={handleApplyFilters}>
          Aplicar
        </Button>
        <Button variant="flat" onPress={handleClearFilters}>
          Limpar
        </Button>
      </div>

      <div className="flex-1" />

      {onGenerateClick && (
        <Button color="success" onPress={onGenerateClick}>
          Gerar Obrigações
        </Button>
      )}
    </div>
  );
}
