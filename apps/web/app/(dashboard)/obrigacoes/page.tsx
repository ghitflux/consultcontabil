"use client";

import { useState } from "react";
import { Card, CardBody, Tabs, Tab } from "@/heroui";
import { ObligationsMatrixPanel } from "@/components/features/obrigacoes/ObligationsMatrixPanel";
import { ObligationsOfficeView } from "@/components/features/obrigacoes/ObligationsOfficeView";
import { ObligationsClientView } from "@/components/features/obrigacoes/ObligationsClientView";
import { TableIcon, Building2Icon, UserIcon } from "@/lib/icons";

type TabKey = "matrix" | "office" | "client";

export default function ObrigacoesPage() {
  const [activeTab, setActiveTab] = useState<TabKey>("matrix");

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Obrigações</h1>
        <p className="text-sm text-default-500 mt-1">
          Gerenciar e acompanhar obrigações fiscais
        </p>
      </div>

      {/* Tabs */}
      <Card>
        <CardBody>
          <Tabs
            selectedKey={activeTab}
            onSelectionChange={(key) => setActiveTab(key as TabKey)}
            aria-label="Visualizações de obrigações"
            color="primary"
            variant="underlined"
            classNames={{
              tabList: "gap-6",
              cursor: "w-full",
              tab: "max-w-fit",
              tabContent: "group-data-[selected=true]:text-primary"
            }}
          >
            <Tab
              key="matrix"
              title={
                <div className="flex items-center gap-2">
                  <TableIcon className="h-4 w-4" />
                  <span>Matriz Completa</span>
                </div>
              }
            >
              <div className="mt-6">
                <ObligationsMatrixPanel />
              </div>
            </Tab>

            <Tab
              key="office"
              title={
                <div className="flex items-center gap-2">
                  <Building2Icon className="h-4 w-4" />
                  <span>Visão do Escritório</span>
                </div>
              }
            >
              <div className="mt-6">
                <ObligationsOfficeView />
              </div>
            </Tab>

            <Tab
              key="client"
              title={
                <div className="flex items-center gap-2">
                  <UserIcon className="h-4 w-4" />
                  <span>Cliente Específico</span>
                </div>
              }
            >
              <div className="mt-6">
                <ObligationsClientView />
              </div>
            </Tab>
          </Tabs>
        </CardBody>
      </Card>
    </div>
  );
}
