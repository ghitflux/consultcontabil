/**
 * Obligations API endpoints
 */

import { apiClient } from "../client";
import type { ClientMatrixRow } from "@/hooks/useObligationsMatrix";

export interface ObligationResponse {
  id: string;
  client_id: string;
  client_name: string;
  client_cnpj: string;
  obligation_type_id: string;
  obligation_type_name: string;
  obligation_type_code: string;
  due_date: string;
  status: string;
  priority: string;
  description?: string;
  receipt_url?: string;
  completed_at?: string;
  completed_by_name?: string;
  created_at: string;
  updated_at: string;
}

export const obligationsApi = {
  /**
   * Get obligations matrix for minimalist panel
   */
  async getMatrix(month: number, year: number, search?: string): Promise<ClientMatrixRow[]> {
    const params = new URLSearchParams({
      month: month.toString(),
      year: year.toString(),
    });

    if (search) {
      params.append("search", search);
    }

    return apiClient.get<ClientMatrixRow[]>(`/obligations/matrix?${params}`);
  },

  /**
   * Mark obligation as completed
   */
  async complete(obligationId: string): Promise<ObligationResponse> {
    return apiClient.post<ObligationResponse>(`/obligations/${obligationId}/complete`, {});
  },

  /**
   * Undo obligation completion
   */
  async undo(obligationId: string): Promise<ObligationResponse> {
    return apiClient.post<ObligationResponse>(`/obligations/${obligationId}/undo`, {});
  },
};
