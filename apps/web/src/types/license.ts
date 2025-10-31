/**
 * License types and interfaces
 */

// Enums
export enum LicenseType {
  ALVARA_FUNCIONAMENTO = "alvara_funcionamento",
  INSCRICAO_MUNICIPAL = "inscricao_municipal",
  INSCRICAO_ESTADUAL = "inscricao_estadual",
  CERTIFICADO_DIGITAL = "certificado_digital",
  LICENCA_AMBIENTAL = "licenca_ambiental",
  LICENCA_SANITARIA = "licenca_sanitaria",
  LICENCA_BOMBEIROS = "licenca_bombeiros",
  OUTROS = "outros",
}

export enum LicenseStatus {
  ATIVA = "ativa",
  VENCIDA = "vencida",
  PENDENTE_RENOVACAO = "pendente_renovacao",
  EM_PROCESSO = "em_processo",
  CANCELADA = "cancelada",
  SUSPENSA = "suspensa",
}

export enum LicenseEventType {
  CREATED = "created",
  ISSUED = "issued",
  RENEWED = "renewed",
  EXPIRED = "expired",
  CANCELLED = "cancelled",
  SUSPENDED = "suspended",
  REACTIVATED = "reactivated",
  UPDATED = "updated",
  DOCUMENT_UPLOADED = "document_uploaded",
}

// License Type Labels
export const LICENSE_TYPE_LABELS: Record<LicenseType, string> = {
  [LicenseType.ALVARA_FUNCIONAMENTO]: "Alvará de Funcionamento",
  [LicenseType.INSCRICAO_MUNICIPAL]: "Inscrição Municipal",
  [LicenseType.INSCRICAO_ESTADUAL]: "Inscrição Estadual",
  [LicenseType.CERTIFICADO_DIGITAL]: "Certificado Digital",
  [LicenseType.LICENCA_AMBIENTAL]: "Licença Ambiental",
  [LicenseType.LICENCA_SANITARIA]: "Licença Sanitária",
  [LicenseType.LICENCA_BOMBEIROS]: "Licença de Bombeiros",
  [LicenseType.OUTROS]: "Outros",
};

export const LICENSE_STATUS_LABELS: Record<LicenseStatus, string> = {
  [LicenseStatus.ATIVA]: "Ativa",
  [LicenseStatus.VENCIDA]: "Vencida",
  [LicenseStatus.PENDENTE_RENOVACAO]: "Pendente Renovação",
  [LicenseStatus.EM_PROCESSO]: "Em Processo",
  [LicenseStatus.CANCELADA]: "Cancelada",
  [LicenseStatus.SUSPENSA]: "Suspensa",
};

export const LICENSE_EVENT_TYPE_LABELS: Record<LicenseEventType, string> = {
  [LicenseEventType.CREATED]: "Criada",
  [LicenseEventType.ISSUED]: "Emitida",
  [LicenseEventType.RENEWED]: "Renovada",
  [LicenseEventType.EXPIRED]: "Vencida",
  [LicenseEventType.CANCELLED]: "Cancelada",
  [LicenseEventType.SUSPENDED]: "Suspensa",
  [LicenseEventType.REACTIVATED]: "Reativada",
  [LicenseEventType.UPDATED]: "Atualizada",
  [LicenseEventType.DOCUMENT_UPLOADED]: "Documento Anexado",
};

// Base interfaces
export interface LicenseBase {
  client_id: string;
  license_type: LicenseType;
  registration_number: string;
  issuing_authority: string;
  issue_date: string; // ISO date string
  expiration_date: string | null; // ISO date string
  notes: string | null;
}

export interface LicenseCreate extends LicenseBase {
  document_id?: string | null;
}

export interface LicenseUpdate {
  license_type?: LicenseType;
  registration_number?: string;
  issuing_authority?: string;
  issue_date?: string;
  expiration_date?: string | null;
  status?: LicenseStatus;
  notes?: string | null;
  document_id?: string | null;
}

export interface LicenseRenewal {
  new_issue_date: string;
  new_expiration_date?: string | null;
  new_registration_number?: string | null;
  notes?: string | null;
  document_id?: string | null;
}

export interface License extends LicenseBase {
  id: string;
  status: LicenseStatus;
  document_id: string | null;
  created_at: string;
  updated_at: string;

  // Computed fields
  days_until_expiration: number | null;
  is_expired: boolean;
  is_expiring_soon: boolean;

  // Related data
  client_name?: string;
  document_url?: string;
}

// License Event
export interface LicenseEventBase {
  event_type: LicenseEventType;
  description: string;
  user_id?: string | null;
}

export interface LicenseEventCreate extends LicenseEventBase {
  license_id: string;
}

export interface LicenseEvent extends LicenseEventBase {
  id: string;
  license_id: string;
  created_at: string;
  user_name?: string;
}

// Alias for API response
export type LicenseEventResponse = LicenseEvent;

// List response
export interface LicenseListResponse {
  items: License[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Statistics
export interface LicenseStatistics {
  total_licenses: number;
  active_licenses: number;
  expired_licenses: number;
  expiring_soon: number;
  pending_renewal: number;
  by_type: Record<string, number>;
  by_status: Record<string, number>;
}

// Filters
export interface LicenseFilters {
  client_id?: string;
  license_type?: LicenseType;
  status?: LicenseStatus;
  search?: string; // Search in registration_number, issuing_authority
  expiring_soon?: boolean; // Filter licenses expiring within 30 days
  expired?: boolean; // Filter expired licenses
  page?: number;
  size?: number;
}

// Helper functions
export function getLicenseStatusColor(status: LicenseStatus): "success" | "warning" | "danger" | "default" {
  switch (status) {
    case LicenseStatus.ATIVA:
      return "success";
    case LicenseStatus.PENDENTE_RENOVACAO:
    case LicenseStatus.EM_PROCESSO:
      return "warning";
    case LicenseStatus.VENCIDA:
    case LicenseStatus.CANCELADA:
    case LicenseStatus.SUSPENSA:
      return "danger";
    default:
      return "default";
  }
}

export function getExpirationBadgeColor(license: License): "success" | "warning" | "danger" {
  if (license.is_expired) {
    return "danger";
  }
  if (license.is_expiring_soon) {
    return "warning";
  }
  return "success";
}

export function formatExpirationStatus(license: License): string {
  if (license.is_expired) {
    return `Vencida há ${Math.abs(license.days_until_expiration || 0)} dias`;
  }
  if (license.is_expiring_soon && license.days_until_expiration !== null) {
    return `Vence em ${license.days_until_expiration} dias`;
  }
  return "Vigente";
}
