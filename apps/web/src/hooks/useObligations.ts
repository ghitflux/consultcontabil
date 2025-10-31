"use client";

import { useState, useEffect, useCallback } from "react";

export interface Obligation {
  id: string;
  client_id: string;
  client_name: string;
  client_cnpj: string;
  obligation_type_id: string;
  obligation_type_name: string;
  obligation_type_code: string;
  status: "pending" | "completed" | "cancelled";
  due_date: string;
  completed_at?: string;
  receipt_url?: string;
  description?: string;
  created_at: string;
  updated_at?: string;
}

interface UseObligationsOptions {
  clientId?: string;
  status?: string;
  year?: number;
  month?: number;
  autoFetch?: boolean;
}

export function useObligations(options: UseObligationsOptions = {}) {
  const { clientId, status, year, month, autoFetch = true } = options;

  const [obligations, setObligations] = useState<Obligation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(0);
  const [limit] = useState(10);

  const fetchObligations = useCallback(
    async (skip = 0) => {
      if (!clientId) {
        return;
      }

      try {
        setLoading(true);
        setError(null);

        const token = localStorage.getItem("access_token");
        const params = new URLSearchParams({
          client_id: clientId,
          skip: skip.toString(),
          limit: limit.toString(),
        });

        if (status) params.append("status", status);
        if (year) params.append("year", year.toString());
        if (month) params.append("month", month.toString());

        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/obligations?${params}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch obligations");
        }

        const data = await response.json();
        setObligations(data.items);
        setTotal(data.total);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    },
    [clientId, status, year, month, limit]
  );

  const generateObligations = async (
    year: number,
    month: number,
    clientId?: string
  ) => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/obligations/generate`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            year,
            month,
            client_id: clientId,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to generate obligations");
      }

      const data = await response.json();
      await fetchObligations();
      return data;
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const uploadReceipt = async (
    obligationId: string,
    file: File,
    notes?: string
  ) => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem("access_token");
      const formData = new FormData();
      formData.append("file", file);
      if (notes) formData.append("notes", notes);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/obligations/${obligationId}/receipt`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to upload receipt");
      }

      const data = await response.json();
      await fetchObligations();
      return data;
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const cancelObligation = async (obligationId: string, reason: string) => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/obligations/${obligationId}/cancel`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ reason }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to cancel obligation");
      }

      const data = await response.json();
      await fetchObligations();
      return data;
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateDueDate = async (
    obligationId: string,
    newDueDate: string,
    reason: string
  ) => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem("access_token");
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/obligations/${obligationId}/due-date`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            new_due_date: newDueDate,
            reason,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to update due date");
      }

      const data = await response.json();
      await fetchObligations();
      return data;
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (autoFetch && clientId) {
      fetchObligations(page * limit);
    }
  }, [autoFetch, clientId, status, year, month, page, limit, fetchObligations]);

  const nextPage = () => {
    if ((page + 1) * limit < total) {
      setPage(page + 1);
    }
  };

  const prevPage = () => {
    if (page > 0) {
      setPage(page - 1);
    }
  };

  return {
    obligations,
    loading,
    error,
    total,
    page,
    limit,
    fetchObligations,
    generateObligations,
    uploadReceipt,
    cancelObligation,
    updateDueDate,
    nextPage,
    prevPage,
  };
}
