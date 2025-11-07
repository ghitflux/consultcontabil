import { useState, useCallback } from 'react';
import { obligationsApi } from '@/lib/api/endpoints/obligations';

export interface ObligationData {
  id: string;
  status: string;
  receipt_url?: string;
  due_date?: string;
}

export interface ClientMatrixRow {
  client_id: string;
  client_name: string;
  client_cnpj: string;
  obligations: (ObligationData | null)[];
  progress: {
    completed: number;
    total: number;
  };
}

export function useObligationsMatrix() {
  const [matrix, setMatrix] = useState<ClientMatrixRow[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchMatrix = useCallback(async (month: number, year: number, search?: string) => {
    try {
      setIsLoading(true);
      setError(null);

      const data = await obligationsApi.getMatrix(month, year, search);
      setMatrix(data);
    } catch (err) {
      console.error('Error fetching matrix:', err);
      setError('Erro ao carregar matriz de obrigações');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const completeObligation = useCallback(async (obligationId: string) => {
    try {
      await obligationsApi.complete(obligationId);

      // Update matrix locally
      setMatrix((prev) =>
        prev.map((row) => ({
          ...row,
          obligations: row.obligations.map((ob) =>
            ob && ob.id === obligationId
              ? { ...ob, status: 'CONCLUIDA' }
              : ob
          ),
          progress: {
            ...row.progress,
            completed:
              row.obligations.filter((ob) => ob && (ob.id === obligationId || ob.status === 'CONCLUIDA')).length,
          },
        }))
      );
    } catch (err) {
      console.error('Error completing obligation:', err);
      throw err;
    }
  }, []);

  const undoObligation = useCallback(async (obligationId: string) => {
    try {
      await obligationsApi.undo(obligationId);

      // Update matrix locally
      setMatrix((prev) =>
        prev.map((row) => ({
          ...row,
          obligations: row.obligations.map((ob) =>
            ob && ob.id === obligationId
              ? { ...ob, status: 'PENDENTE' }
              : ob
          ),
          progress: {
            ...row.progress,
            completed: row.obligations.filter(
              (ob) => ob && ob.status === 'CONCLUIDA' && ob.id !== obligationId
            ).length,
          },
        }))
      );
    } catch (err) {
      console.error('Error undoing obligation:', err);
      throw err;
    }
  }, []);

  const downloadReceipt = useCallback((receiptUrl: string) => {
    window.open(receiptUrl, '_blank');
  }, []);

  return {
    matrix,
    isLoading,
    error,
    fetchMatrix,
    completeObligation,
    undoObligation,
    downloadReceipt,
  };
}
