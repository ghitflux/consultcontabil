/**
 * Municipal Registration types and interfaces
 */

// Enums
export enum MunicipalRegistrationStatus {
  ATIVA = "ativa",
  INATIVA = "inativa",
  SUSPENSA = "suspensa",
  PENDENTE = "pendente",
  CANCELADA = "cancelada",
}

export enum StateCode {
  AC = "AC",
  AL = "AL",
  AP = "AP",
  AM = "AM",
  BA = "BA",
  CE = "CE",
  DF = "DF",
  ES = "ES",
  GO = "GO",
  MA = "MA",
  MT = "MT",
  MS = "MS",
  MG = "MG",
  PA = "PA",
  PB = "PB",
  PR = "PR",
  PE = "PE",
  PI = "PI",
  RJ = "RJ",
  RN = "RN",
  RS = "RS",
  RO = "RO",
  RR = "RR",
  SC = "SC",
  SP = "SP",
  SE = "SE",
  TO = "TO",
}

// Labels
export const MUNICIPAL_REGISTRATION_STATUS_LABELS: Record<MunicipalRegistrationStatus, string> = {
  [MunicipalRegistrationStatus.ATIVA]: "Ativa",
  [MunicipalRegistrationStatus.INATIVA]: "Inativa",
  [MunicipalRegistrationStatus.SUSPENSA]: "Suspensa",
  [MunicipalRegistrationStatus.PENDENTE]: "Pendente",
  [MunicipalRegistrationStatus.CANCELADA]: "Cancelada",
};

export const STATE_LABELS: Record<StateCode, string> = {
  [StateCode.AC]: "Acre",
  [StateCode.AL]: "Alagoas",
  [StateCode.AP]: "Amapá",
  [StateCode.AM]: "Amazonas",
  [StateCode.BA]: "Bahia",
  [StateCode.CE]: "Ceará",
  [StateCode.DF]: "Distrito Federal",
  [StateCode.ES]: "Espírito Santo",
  [StateCode.GO]: "Goiás",
  [StateCode.MA]: "Maranhão",
  [StateCode.MT]: "Mato Grosso",
  [StateCode.MS]: "Mato Grosso do Sul",
  [StateCode.MG]: "Minas Gerais",
  [StateCode.PA]: "Pará",
  [StateCode.PB]: "Paraíba",
  [StateCode.PR]: "Paraná",
  [StateCode.PE]: "Pernambuco",
  [StateCode.PI]: "Piauí",
  [StateCode.RJ]: "Rio de Janeiro",
  [StateCode.RN]: "Rio Grande do Norte",
  [StateCode.RS]: "Rio Grande do Sul",
  [StateCode.RO]: "Rondônia",
  [StateCode.RR]: "Roraima",
  [StateCode.SC]: "Santa Catarina",
  [StateCode.SP]: "São Paulo",
  [StateCode.SE]: "Sergipe",
  [StateCode.TO]: "Tocantins",
};

// Base interfaces
export interface MunicipalRegistrationBase {
  client_id: string;
  city: string;
  state: StateCode;
  registration_number: string;
  issue_date: string; // ISO date string
  notes: string | null;
}

export interface MunicipalRegistrationCreate extends MunicipalRegistrationBase {}

export interface MunicipalRegistrationUpdate {
  city?: string;
  state?: StateCode;
  registration_number?: string;
  issue_date?: string;
  status?: MunicipalRegistrationStatus;
  notes?: string | null;
}

export interface MunicipalRegistration extends MunicipalRegistrationBase {
  id: string;
  status: MunicipalRegistrationStatus;
  created_at: string;
  updated_at: string;
  client_name?: string;
}

// List response
export interface MunicipalRegistrationListResponse {
  items: MunicipalRegistration[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Statistics
export interface MunicipalRegistrationStatistics {
  total_registrations: number;
  active_registrations: number;
  inactive_registrations: number;
  by_state: Record<string, number>;
  by_status: Record<string, number>;
}

// Filters
export interface MunicipalRegistrationFilters {
  client_id?: string;
  state?: StateCode;
  status?: MunicipalRegistrationStatus;
  search?: string; // Search in city, registration_number
  page?: number;
  size?: number;
}

// Helper functions
export function getMunicipalRegistrationStatusColor(
  status: MunicipalRegistrationStatus
): "success" | "warning" | "danger" | "default" {
  switch (status) {
    case MunicipalRegistrationStatus.ATIVA:
      return "success";
    case MunicipalRegistrationStatus.PENDENTE:
      return "warning";
    case MunicipalRegistrationStatus.INATIVA:
    case MunicipalRegistrationStatus.SUSPENSA:
    case MunicipalRegistrationStatus.CANCELADA:
      return "danger";
    default:
      return "default";
  }
}

export function getStateLabel(code: StateCode): string {
  return STATE_LABELS[code] || code;
}

export function getStateLabelWithCode(code: StateCode): string {
  return `${STATE_LABELS[code]} (${code})`;
}
