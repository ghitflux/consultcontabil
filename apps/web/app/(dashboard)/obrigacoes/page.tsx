"use client";

import { useState } from "react";
import { Card, CardBody, Tabs, Tab } from "@/heroui";
import { ObligationsMatrixPanel } from "@/components/features/obrigacoes/ObligationsMatrixPanel";
import { ObligationsMatrixTable } from "@/components/features/obrigacoes/ObligationsMatrixTable";
import dynamic from 'next/dynamic';

// Dynamic import for heavy components
const ObligationTimeline = dynamic(() =>
  import("@/components/features/obrigacoes/ObligationTimeline").then(mod => ({ default: mod.ObligationTimeline })),
  { ssr: false }
);

type TabKey = "minimalist" | "office" | "client";

export default function ObrigacoesPage() {
  const [activeTab, setActiveTab] = useState<TabKey>("minimalist");

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
          >
            <Tab
              key="minimalist"
              title={
                <div className="flex items-center gap-2">
                  <span>Painel Minimalista</span>
                </div>
              }
            >
              <div className="mt-4">
                <ObligationsMatrixPanel />
              </div>
            </Tab>

            <Tab
              key="office"
              title={
                <div className="flex items-center gap-2">
                  <span>Obrigações do Escritório</span>
                </div>
              }
            >
              <div className="mt-4">
                <ObligationsMatrixTable viewMode="office" />
              </div>
            </Tab>

            <Tab
              key="client"
              title={
                <div className="flex items-center gap-2">
                  <span>Cliente Específico</span>
                </div>
              }
            >
              <div className="mt-4">
                <ObligationsMatrixTable viewMode="client" />
              </div>
            </Tab>
          </Tabs>
        </CardBody>
      </Card>
    </div>
  );
}
