/**
 * Obligation types and interfaces
 * Mirrors backend schemas from apps/api/app/schemas/obligation.py
 */

export enum ObligationStatus {
  PENDENTE = "pendente",
  EM_ANDAMENTO = "em_andamento",
  CONCLUIDA = "concluida",
  ATRASADA = "atrasada",
  CANCELADA = "cancelada",
}

export enum ObligationPriority {
  BAIXA = "baixa",
  MEDIA = "media",
  ALTA = "alta",
  URGENTE = "urgente",
}

export enum ObligationRecurrence {
  MENSAL = "mensal",
  BIMESTRAL = "bimestral",
  TRIMESTRAL = "trimestral",
  SEMESTRAL = "semestral",
  ANUAL = "anual",
}

// Obligation Type Interfaces
export interface ObligationType {
  id: string;
  name: string;
  code: string;
  description?: string;

  // Applicability
  applies_to_commerce: boolean;
  applies_to_service: boolean;
  applies_to_industry: boolean;
  applies_to_mei: boolean;

  applies_to_simples: boolean;
  applies_to_presumido: boolean;
  applies_to_real: boolean;

  // Generation settings
  recurrence: ObligationRecurrence;
  day_of_month?: number;
  month_of_year?: number;

  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface ObligationTypeCreate {
  name: string;
  code: string;
  description?: string;

  applies_to_commerce?: boolean;
  applies_to_service?: boolean;
  applies_to_industry?: boolean;
  applies_to_mei?: boolean;

  applies_to_simples?: boolean;
  applies_to_presumido?: boolean;
  applies_to_real?: boolean;

  recurrence: ObligationRecurrence;
  day_of_month?: number;
  month_of_year?: number;

  is_active?: boolean;
}

export interface ObligationTypeUpdate {
  name?: string;
  description?: string;
  is_active?: boolean;
  day_of_month?: number;
}

// Obligation Interfaces
export interface Obligation {
  id: string;
  client_id: string;
  obligation_type_id: string;
  due_date: string; // ISO date string
  status: ObligationStatus;
  priority: ObligationPriority;
  description?: string;

  // Client info
  client_name: string;
  client_cnpj: string;

  // Obligation type info
  obligation_type_name: string;
  obligation_type_code: string;

  // Completion info
  receipt_url?: string;
  completed_at?: string;
  completed_by_name?: string;

  // Timestamps
  created_at: string;
  updated_at?: string;
}

export interface ObligationCreate {
  client_id: string;
  obligation_type_id: string;
  due_date: string; // ISO date string
  description?: string;
  priority?: ObligationPriority;
}

export interface ObligationUpdate {
  status?: ObligationStatus;
  priority?: ObligationPriority;
  description?: string;
  due_date?: string;
}

export interface ObligationListResponse {
  items: Obligation[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface ObligationReceiptUpload {
  notes?: string;
}

export interface ObligationGenerateRequest {
  reference_month?: string; // ISO date string (first day of month)
  client_ids?: string[];
}

export interface ObligationGenerateResponse {
  reference_month: string;
  total_created: number;
  total_clients: number;
  status: string;
}

// Obligation Event Interfaces
export interface ObligationEvent {
  id: string;
  obligation_id: string;
  user_id?: string;
  user_name?: string;
  event_type: string;
  description: string;
  metadata?: Record<string, unknown>;
  created_at: string;
}

export interface ObligationEventCreate {
  obligation_id: string;
  user_id?: string;
  event_type: string;
  description: string;
  metadata?: Record<string, unknown>;
}

// Statistics Interfaces
export interface ObligationStatistics {
  total: number;
  by_status: Record<ObligationStatus, number>;
  by_priority: Record<ObligationPriority, number>;
  overdue: number;
  due_this_week: number;
  due_this_month: number;
  completion_rate: number; // Percentage
}

export interface ClientObligationSummary {
  client_id: string;
  client_name: string;
  client_cnpj: string;
  total_obligations: number;
  pending: number;
  completed: number;
  overdue: number;
  next_due_date?: string;
}

// Filter interfaces for API queries
export interface ObligationFilters {
  client_id?: string;
  status?: ObligationStatus;
  priority?: ObligationPriority;
  due_date_from?: string;
  due_date_to?: string;
  search?: string; // Search in description or obligation type name
  page?: number;
  size?: number;
}

// Helper type guards
export function isOverdue(obligation: Obligation): boolean {
  const dueDate = new Date(obligation.due_date);
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  return (
    obligation.status !== ObligationStatus.CONCLUIDA &&
    obligation.status !== ObligationStatus.CANCELADA &&
    dueDate < today
  );
}

export function isDueSoon(obligation: Obligation, days: number = 7): boolean {
  const dueDate = new Date(obligation.due_date);
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const diffTime = dueDate.getTime() - today.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  return (
    obligation.status !== ObligationStatus.CONCLUIDA &&
    obligation.status !== ObligationStatus.CANCELADA &&
    diffDays >= 0 &&
    diffDays <= days
  );
}

// Status colors for UI
export function getStatusColor(
  status: ObligationStatus
): "default" | "primary" | "secondary" | "success" | "warning" | "danger" {
  switch (status) {
    case ObligationStatus.CONCLUIDA:
      return "success";
    case ObligationStatus.ATRASADA:
      return "danger";
    case ObligationStatus.EM_ANDAMENTO:
      return "primary";
    case ObligationStatus.CANCELADA:
      return "default";
    case ObligationStatus.PENDENTE:
      return "warning";
    default:
      return "default";
  }
}

// Priority colors for UI
export function getPriorityColor(
  priority: ObligationPriority
): "default" | "primary" | "secondary" | "success" | "warning" | "danger" {
  switch (priority) {
    case ObligationPriority.URGENTE:
      return "danger";
    case ObligationPriority.ALTA:
      return "warning";
    case ObligationPriority.MEDIA:
      return "primary";
    case ObligationPriority.BAIXA:
      return "default";
    default:
      return "default";
  }
}

// Status labels in Portuguese
export const STATUS_LABELS: Record<ObligationStatus, string> = {
  [ObligationStatus.PENDENTE]: "Pendente",
  [ObligationStatus.EM_ANDAMENTO]: "Em Andamento",
  [ObligationStatus.CONCLUIDA]: "Concluída",
  [ObligationStatus.ATRASADA]: "Atrasada",
  [ObligationStatus.CANCELADA]: "Cancelada",
};

// Priority labels in Portuguese
export const PRIORITY_LABELS: Record<ObligationPriority, string> = {
  [ObligationPriority.BAIXA]: "Baixa",
  [ObligationPriority.MEDIA]: "Média",
  [ObligationPriority.ALTA]: "Alta",
  [ObligationPriority.URGENTE]: "Urgente",
};

// Recurrence labels in Portuguese
export const RECURRENCE_LABELS: Record<ObligationRecurrence, string> = {
  [ObligationRecurrence.MENSAL]: "Mensal",
  [ObligationRecurrence.BIMESTRAL]: "Bimestral",
  [ObligationRecurrence.TRIMESTRAL]: "Trimestral",
  [ObligationRecurrence.SEMESTRAL]: "Semestral",
  [ObligationRecurrence.ANUAL]: "Anual",
};
