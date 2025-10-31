/**
 * CNAE types and interfaces
 */

// Enums
export enum CnaeType {
  PRINCIPAL = "principal",
  SECUNDARIO = "secundario",
}

// Type Labels
export const CNAE_TYPE_LABELS: Record<CnaeType, string> = {
  [CnaeType.PRINCIPAL]: "Principal",
  [CnaeType.SECUNDARIO]: "Secundário",
};

// Base interfaces
export interface CnaeBase {
  cnae_code: string; // Format: 0000-0/00
  description: string;
  cnae_type: CnaeType;
}

export interface CnaeCreate extends CnaeBase {
  client_id: string;
}

export interface CnaeUpdate {
  description?: string;
  cnae_type?: CnaeType;
  is_active?: boolean;
}

export interface Cnae extends CnaeBase {
  id: string;
  client_id: string;
  is_active: boolean;
  created_at: string;
  client_name?: string;
}

// List response
export interface CnaeListResponse {
  items: Cnae[];
  total: number;
}

// Set primary
export interface CnaeSetPrimary {
  cnae_id: string;
}

// Validation
export interface CnaeValidation {
  is_valid: boolean;
  cnae_code: string;
  formatted_code: string;
  error?: string | null;
}

// Helper functions
export function formatCnaeCode(code: string): string {
  // Remove all non-digit characters
  const digits = code.replace(/\D/g, "");

  // Check if we have enough digits
  if (digits.length < 7) {
    return code; // Return as-is if incomplete
  }

  // Format as 0000-0/00
  return `${digits.slice(0, 4)}-${digits.slice(4, 5)}/${digits.slice(5, 7)}`;
}

export function validateCnaeFormat(code: string): boolean {
  // CNAE format: 0000-0/00
  const pattern = /^\d{4}-\d{1}\/\d{2}$/;
  return pattern.test(code);
}

export function getCnaeTypeColor(type: CnaeType): "primary" | "default" {
  return type === CnaeType.PRINCIPAL ? "primary" : "default";
}

export function getCnaeTypeBadgeVariant(type: CnaeType): "solid" | "flat" {
  return type === CnaeType.PRINCIPAL ? "solid" : "flat";
}
