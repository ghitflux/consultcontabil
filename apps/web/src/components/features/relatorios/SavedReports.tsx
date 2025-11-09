"use client";

import { Card, CardBody, CardHeader, Button } from "@/heroui";
import {
  FileTextIcon,
  DownloadIcon,
  EditIcon,
  TrashIcon,
  CalendarIcon,
} from "@/lib/icons";

interface SavedReportsProps {
  onEdit: () => void;
}

const savedReports = [
  {
    id: "1",
    name: "Relatório de Clientes Ativos",
    dataSource: "Clientes",
    createdAt: "2024-01-15",
    lastRun: "2024-01-27",
  },
  {
    id: "2",
    name: "Análise Financeira Mensal",
    dataSource: "Transações Financeiras",
    createdAt: "2024-01-10",
    lastRun: "2024-01-26",
  },
  {
    id: "3",
    name: "Obrigações Pendentes",
    dataSource: "Obrigações",
    createdAt: "2024-01-20",
    lastRun: "2024-01-27",
  },
  {
    id: "4",
    name: "Licenças a Vencer",
    dataSource: "Licenças",
    createdAt: "2024-01-12",
    lastRun: "2024-01-25",
  },
];

export function SavedReports({ onEdit }: SavedReportsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {savedReports.map((report) => (
        <Card key={report.id}>
          <CardHeader>
            <div className="flex items-start justify-between">
              <div className="flex items-start gap-3">
                <div className="p-2 bg-teal-100 dark:bg-teal-900 rounded-lg">
                  <FileTextIcon className="h-5 w-5 text-teal-600 dark:text-teal-400" />
                </div>
                <div>
                  <h3 className="text-base font-semibold">{report.name}</h3>
                  <p className="text-sm text-default-500 mt-1">
                    {report.dataSource}
                  </p>
                </div>
              </div>
            </div>
          </CardHeader>
          <CardBody className="space-y-4">
            <div className="flex items-center gap-4 text-sm text-default-500">
              <div className="flex items-center gap-1">
                <CalendarIcon className="h-4 w-4" />
                <span>
                  Criado:{" "}
                  {new Date(report.createdAt).toLocaleDateString("pt-BR")}
                </span>
              </div>
            </div>
            <div className="text-sm text-default-500">
              Última execução:{" "}
              {new Date(report.lastRun).toLocaleDateString("pt-BR")}
            </div>
            <div className="flex gap-2">
              <Button
                variant="bordered"
                size="sm"
                className="flex-1 gap-2"
                startContent={<DownloadIcon className="h-4 w-4" />}
              >
                Executar
              </Button>
              <Button
                variant="bordered"
                size="sm"
                isIconOnly
                onPress={onEdit}
              >
                <EditIcon className="h-4 w-4" />
              </Button>
              <Button variant="bordered" size="sm" isIconOnly color="danger">
                <TrashIcon className="h-4 w-4" />
              </Button>
            </div>
          </CardBody>
        </Card>
      ))}
    </div>
  );
}

