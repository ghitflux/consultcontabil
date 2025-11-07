"use client";

import React, { useState } from "react";
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
  Button,
  Input,
  Select,
  SelectItem,
  Slider,
  DateRangePicker,
  Badge,
} from "@heroui/react";
import { FilterIcon } from "@/lib/icons";

export type FilterType = "text" | "select" | "multiselect" | "range" | "daterange";

export interface FilterOption {
  label: string;
  value: string;
}

interface ColumnFilterProps {
  type: FilterType;
  value?: any;
  onChange: (value: any) => void;
  options?: FilterOption[];
  placeholder?: string;
  min?: number;
  max?: number;
}

export function ColumnFilter({
  type,
  value,
  onChange,
  options = [],
  placeholder = "Filtrar...",
  min = 0,
  max = 10000,
}: ColumnFilterProps) {
  const [isOpen, setIsOpen] = useState(false);
  const hasActiveFilter = value !== undefined && value !== "" && value !== null;

  const renderFilterContent = () => {
    switch (type) {
      case "text":
        return (
          <Input
            type="text"
            placeholder={placeholder}
            value={value || ""}
            onChange={(e) => onChange(e.target.value)}
            size="sm"
            autoFocus
          />
        );

      case "select":
        return (
          <Select
            placeholder={placeholder}
            selectedKeys={value ? [value] : []}
            onSelectionChange={(keys) => {
              const selected = Array.from(keys)[0];
              onChange(selected);
            }}
            size="sm"
          >
            {options.map((option) => (
              <SelectItem key={option.value}>
                {option.label}
              </SelectItem>
            ))}
          </Select>
        );

      case "multiselect":
        return (
          <Select
            placeholder={placeholder}
            selectionMode="multiple"
            selectedKeys={value || []}
            onSelectionChange={(keys) => onChange(Array.from(keys))}
            size="sm"
          >
            {options.map((option) => (
              <SelectItem key={option.value}>
                {option.label}
              </SelectItem>
            ))}
          </Select>
        );

      case "range":
        return (
          <div className="space-y-2">
            <p className="text-xs text-gray-600">
              Valor: R$ {value?.[0] || min} - R$ {value?.[1] || max}
            </p>
            <Slider
              label="Faixa de valores"
              step={100}
              minValue={min}
              maxValue={max}
              value={value || [min, max]}
              onChange={onChange}
              size="sm"
              className="max-w-md"
            />
          </div>
        );

      case "daterange":
        return (
          <DateRangePicker
            label="Período"
            value={value}
            onChange={onChange}
            size="sm"
          />
        );

      default:
        return null;
    }
  };

  return (
    <Popover isOpen={isOpen} onOpenChange={setIsOpen} placement="bottom">
      <PopoverTrigger>
        <Button
          size="sm"
          variant="light"
          isIconOnly
          className="min-w-unit-6 h-6"
        >
          {hasActiveFilter ? (
            <Badge content="" color="primary" size="sm" placement="top-right">
              <FilterIcon className="h-4 w-4" />
            </Badge>
          ) : (
            <FilterIcon className="h-4 w-4" />
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-80 p-4">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold">Filtrar</h3>
            {hasActiveFilter && (
              <Button
                size="sm"
                variant="light"
                color="danger"
                onClick={() => {
                  onChange(undefined);
                  setIsOpen(false);
                }}
              >
                Limpar
              </Button>
            )}
          </div>
          {renderFilterContent()}
        </div>
      </PopoverContent>
    </Popover>
  );
}
