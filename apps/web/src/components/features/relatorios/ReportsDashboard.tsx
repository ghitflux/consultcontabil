"use client";

import {
  Card,
  CardBody,
  CardHeader,
  Button,
  Skeleton,
} from "@/heroui";
import { useEffect, useState, useCallback, memo } from "react";
import { useReportPreview } from "@/hooks/useReportPreview";
import type { ReportType, ReportTypeInfo } from "@/types/report";
import { ReportType as ReportTypeEnum } from "@/types/report";
import { format } from "date-fns";
import { ReportPreviewRenderer } from "./ReportPreviewRenderer";
import {
  TrendingUpIcon,
  DollarSignIcon,
  UsersIcon,
  CheckCircleIcon,
  BarChartIcon,
  ArrowRightIcon,
} from "@/lib/icons";

interface ReportsDashboardProps {
  reportTypes: ReportTypeInfo[];
  onSelectReportType?: (type: ReportType) => void;
}

// KPI Card Component (memoized for performance)
const KPICard = memo(function KPICard({
  label,
  value,
  icon: Icon,
  color = "primary",
}: {
  label: string;
  value: string | number;
  icon: React.ComponentType<{ className?: string }>;
  color?: "primary" | "success" | "warning" | "default";
}) {
  const colorClasses = {
    primary: "text-primary",
    success: "text-success",
    warning: "text-warning",
    default: "text-foreground",
  };

  return (
    <Card>
      <CardBody className="gap-2">
        <div className="flex items-center justify-between">
          <p className="text-sm text-default-500">{label}</p>
          <Icon className="h-5 w-5 text-default-400" />
        </div>
        <p className={`text-2xl font-bold ${colorClasses[color]}`}>{value}</p>
      </CardBody>
    </Card>
  );
});

// Skeleton for KPI Card
function KPICardSkeleton() {
  return (
    <Card>
      <CardBody className="gap-2">
        <Skeleton className="h-4 w-3/4" />
        <Skeleton className="h-8 w-1/2" />
      </CardBody>
    </Card>
  );
}

// Report Type Button (memoized)
const ReportTypeButton = memo(function ReportTypeButton({
  type,
  onPress,
}: {
  type: ReportTypeInfo;
  onPress: () => void;
}) {
  return (
    <Button
      variant="bordered"
      className="h-auto p-4 flex-col items-start text-left group hover:border-primary"
      onPress={onPress}
    >
      <div className="flex items-center justify-between w-full">
        <div className="font-semibold">{type.name}</div>
        <ArrowRightIcon className="h-4 w-4 opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>
      <div className="text-xs text-default-500 mt-1">{type.description}</div>
    </Button>
  );
});

export function ReportsDashboard({
  reportTypes,
  onSelectReportType,
}: ReportsDashboardProps) {
  const { previewReport, preview, isLoading } = useReportPreview();
  const [selectedType, setSelectedType] = useState<ReportType | null>(null);

  const loadKPIDashboard = useCallback(async () => {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setMonth(startDate.getMonth() - 3);

    try {
      await previewReport({
        report_type: ReportTypeEnum.KPIS,
        filters: {
          period_start: format(startDate, "yyyy-MM-dd"),
          period_end: format(endDate, "yyyy-MM-dd"),
          report_type: ReportTypeEnum.KPIS,
        },
        customizations: {
          include_summary: true,
          include_charts: true,
        },
      });
    } catch (error) {
      console.error("Error loading KPI dashboard:", error);
    }
  }, [previewReport]);

  // Set default period (last 3 months)
  useEffect(() => {
    if (!selectedType && reportTypes.length > 0) {
      // Default to KPI report for dashboard
      const kpiType = reportTypes.find((t) => t.type === ReportTypeEnum.KPIS);
      if (kpiType) {
        setSelectedType(kpiType.type);
        loadKPIDashboard();
      }
    }
  }, [reportTypes, selectedType, loadKPIDashboard]);

  // Financial KPIs
  const financialTypes = reportTypes.filter(
    (t) => t.category === "financeiro"
  );
  // Operational KPIs
  const operationalTypes = reportTypes.filter(
    (t) => t.category === "operacional"
  );

  return (
    <div className="space-y-6 mt-6">
      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {preview && preview.summary ? (
          <>
            {preview.summary.margem_lucro !== undefined && (
              <KPICard
                label="Margem de Lucro"
                value={`${Number(preview.summary.margem_lucro).toFixed(2)}%`}
                icon={TrendingUpIcon}
                color="success"
              />
            )}
            {preview.summary.receita_total !== undefined && (
              <KPICard
                label="Receita Total"
                value={`R$ ${Number(preview.summary.receita_total).toLocaleString("pt-BR", {
                  minimumFractionDigits: 2,
                })}`}
                icon={DollarSignIcon}
                color="primary"
              />
            )}
            {preview.summary.total_clientes !== undefined && (
              <KPICard
                label="Total de Clientes"
                value={preview.summary.total_clientes}
                icon={UsersIcon}
                color="default"
              />
            )}
            {preview.summary.compliance_rate !== undefined && (
              <KPICard
                label="Taxa de Compliance"
                value={`${Number(preview.summary.compliance_rate).toFixed(1)}%`}
                icon={CheckCircleIcon}
                color="warning"
              />
            )}
          </>
        ) : (
          <>
            <KPICardSkeleton />
            <KPICardSkeleton />
            <KPICardSkeleton />
            <KPICardSkeleton />
          </>
        )}
      </div>

      {/* Preview Section */}
      {preview && (
        <div className="mt-6">
          <ReportPreviewRenderer preview={preview} isLoading={isLoading} />
        </div>
      )}

      {/* Report Types Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* Financial Reports */}
        <Card className="col-span-full">
          <CardHeader>
            <div className="flex items-center gap-2">
              <DollarSignIcon className="h-5 w-5 text-primary" />
              <h3 className="text-lg font-semibold">Relatórios Financeiros</h3>
            </div>
          </CardHeader>
          <CardBody>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {financialTypes.map((type) => (
                <ReportTypeButton
                  key={type.type}
                  type={type}
                  onPress={() => {
                    setSelectedType(type.type);
                    onSelectReportType?.(type.type);
                  }}
                />
              ))}
            </div>
          </CardBody>
        </Card>

        {/* Operational Reports */}
        <Card className="col-span-full">
          <CardHeader>
            <div className="flex items-center gap-2">
              <BarChartIcon className="h-5 w-5 text-success" />
              <h3 className="text-lg font-semibold">Relatórios Operacionais</h3>
            </div>
          </CardHeader>
          <CardBody>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {operationalTypes.map((type) => (
                <ReportTypeButton
                  key={type.type}
                  type={type}
                  onPress={() => {
                    setSelectedType(type.type);
                    onSelectReportType?.(type.type);
                  }}
                />
              ))}
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
