/**
 * Client types and interfaces.
 */

export enum ClientStatus {
  ATIVO = "ativo",
  INATIVO = "inativo",
  PENDENTE = "pendente",
}

export enum RegimeTributario {
  SIMPLES_NACIONAL = "simples_nacional",
  LUCRO_PRESUMIDO = "lucro_presumido",
  LUCRO_REAL = "lucro_real",
  MEI = "mei",
}

export enum TipoEmpresa {
  COMERCIO = "comercio",
  SERVICO = "servico",
  INDUSTRIA = "industria",
  MISTO = "misto",
}

export interface ClientBase {
  razao_social: string;
  nome_fantasia: string | null;
  cnpj: string;
  inscricao_estadual: string | null;
  inscricao_municipal: string | null;

  // Contact
  email: string;
  telefone: string | null;
  celular: string | null;

  // Address
  cep: string | null;
  logradouro: string | null;
  numero: string | null;
  complemento: string | null;
  bairro: string | null;
  cidade: string | null;
  uf: string | null;

  // Financial
  honorarios_mensais: number;
  dia_vencimento: number;

  // Tax info
  regime_tributario: RegimeTributario;
  tipo_empresa: TipoEmpresa;
  data_abertura: string | null;

  // Responsible person
  responsavel_nome: string | null;
  responsavel_cpf: string | null;
  responsavel_email: string | null;
  responsavel_telefone: string | null;

  // Notes
  observacoes: string | null;
}

export interface ClientCreate extends ClientBase {
  status?: ClientStatus;
}

export interface ClientUpdate extends Partial<ClientBase> {
  status?: ClientStatus;
}

export interface Client extends ClientBase {
  id: string;
  status: ClientStatus;
  created_at: string;
  updated_at: string;
}

export interface ClientListItem {
  id: string;
  razao_social: string;
  nome_fantasia: string | null;
  cnpj: string;
  email: string;
  status: ClientStatus;
  honorarios_mensais: number;
  regime_tributario: RegimeTributario;
  tipo_empresa: TipoEmpresa;
  created_at: string;
  updated_at: string;
}

export interface ClientFilters {
  query?: string;
  status?: ClientStatus | "";
  regime_tributario?: RegimeTributario | "";
  tipo_empresa?: TipoEmpresa | "";
  starts_with?: string; // A-Z alphabetical filter
  page?: number;
  size?: number;
}

export interface ClientListResponse {
  items: ClientListItem[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

/**
 * Helper function to format CNPJ for display.
 */
export function formatCNPJ(cnpj: string): string {
  const digits = cnpj.replace(/\D/g, "");
  if (digits.length !== 14) return cnpj;
  return `${digits.slice(0, 2)}.${digits.slice(2, 5)}.${digits.slice(5, 8)}/${digits.slice(8, 12)}-${digits.slice(12)}`;
}

/**
 * Helper function to format phone number for display.
 */
export function formatPhone(phone: string | null): string | null {
  if (!phone) return null;
  const digits = phone.replace(/\D/g, "");
  if (digits.length === 10) {
    return `(${digits.slice(0, 2)}) ${digits.slice(2, 6)}-${digits.slice(6)}`;
  }
  if (digits.length === 11) {
    return `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7)}`;
  }
  return phone;
}

/**
 * Helper function to get status display label.
 */
export function getStatusLabel(status: ClientStatus): string {
  const labels: Record<ClientStatus, string> = {
    [ClientStatus.ATIVO]: "Ativo",
    [ClientStatus.INATIVO]: "Inativo",
    [ClientStatus.PENDENTE]: "Pendente",
  };
  return labels[status];
}

/**
 * Helper function to get regime tributario display label.
 */
export function getRegimeLabel(regime: RegimeTributario): string {
  const labels: Record<RegimeTributario, string> = {
    [RegimeTributario.SIMPLES_NACIONAL]: "Simples Nacional",
    [RegimeTributario.LUCRO_PRESUMIDO]: "Lucro Presumido",
    [RegimeTributario.LUCRO_REAL]: "Lucro Real",
    [RegimeTributario.MEI]: "MEI",
  };
  return labels[regime];
}

/**
 * Helper function to get tipo empresa display label.
 */
export function getTipoEmpresaLabel(tipo: TipoEmpresa): string {
  const labels: Record<TipoEmpresa, string> = {
    [TipoEmpresa.COMERCIO]: "Comércio",
    [TipoEmpresa.SERVICO]: "Serviço",
    [TipoEmpresa.INDUSTRIA]: "Indústria",
    [TipoEmpresa.MISTO]: "Misto",
  };
  return labels[tipo];
}
