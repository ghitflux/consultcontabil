/**
 * Hook for managing reports state and operations.
 */

import { reportsApi } from "@/lib/api/endpoints/reports";
import type {
  ReportHistoryListResponse,
  ReportTemplate,
  ReportTemplateCreate,
  ReportTemplateUpdate,
  ReportTypesListResponse,
} from "@/types/report";
import { useCallback, useState } from "react";

type LoadingState = {
  reportTypes: boolean;
  templates: boolean;
  history: boolean;
  mutation: boolean;
};

export function useReports() {
  const [reportTypes, setReportTypes] = useState<ReportTypesListResponse | null>(
    null
  );
  const [templates, setTemplates] = useState<ReportTemplate[]>([]);
  const [history, setHistory] = useState<ReportHistoryListResponse | null>(
    null
  );
  const [loading, setLoading] = useState<LoadingState>({
    reportTypes: false,
    templates: false,
    history: false,
    mutation: false,
  });
  const [error, setError] = useState<string | null>(null);

  const updateLoading = useCallback(
    (key: keyof LoadingState, value: boolean) => {
      setLoading((prev) => ({ ...prev, [key]: value }));
    },
    []
  );

  /**
   * Fetch all available report types.
   */
  const fetchReportTypes = useCallback(async () => {
    updateLoading("reportTypes", true);
    setError(null);

    try {
      const data = await reportsApi.getReportTypes();
      setReportTypes(data);
      return data;
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Failed to fetch report types";
      setError(message);
      throw err;
    } finally {
      updateLoading("reportTypes", false);
    }
  }, [updateLoading]);

  /**
   * Fetch report templates.
   */
  const fetchTemplates = useCallback(
    async (includeSystem: boolean = true) => {
      updateLoading("templates", true);
      setError(null);

      try {
        const data = await reportsApi.getTemplates(includeSystem);
        setTemplates(data);
        return data;
      } catch (err) {
        const message =
          err instanceof Error ? err.message : "Failed to fetch templates";
        setError(message);
        throw err;
      } finally {
        updateLoading("templates", false);
      }
    },
    [updateLoading]
  );

  /**
   * Create a new report template.
   */
  const createTemplate = useCallback(
    async (data: ReportTemplateCreate) => {
      updateLoading("mutation", true);
      setError(null);

      try {
        const newTemplate = await reportsApi.createTemplate(data);
        // Refresh templates list
        await fetchTemplates();
        return newTemplate;
      } catch (err) {
        const message =
          err instanceof Error ? err.message : "Failed to create template";
        setError(message);
        throw err;
      } finally {
        updateLoading("mutation", false);
      }
    },
    [fetchTemplates, updateLoading]
  );

  /**
   * Update a report template.
   */
  const updateTemplate = useCallback(
    async (id: string, data: ReportTemplateUpdate) => {
      updateLoading("mutation", true);
      setError(null);

      try {
        const updatedTemplate = await reportsApi.updateTemplate(id, data);
        // Refresh templates list
        await fetchTemplates();
        return updatedTemplate;
      } catch (err) {
        const message =
          err instanceof Error ? err.message : "Failed to update template";
        setError(message);
        throw err;
      } finally {
        updateLoading("mutation", false);
      }
    },
    [fetchTemplates, updateLoading]
  );

  /**
   * Delete a report template.
   */
  const deleteTemplate = useCallback(
    async (id: string) => {
      updateLoading("mutation", true);
      setError(null);

      try {
        await reportsApi.deleteTemplate(id);
        // Refresh templates list
        await fetchTemplates();
      } catch (err) {
        const message =
          err instanceof Error ? err.message : "Failed to delete template";
        setError(message);
        throw err;
      } finally {
        updateLoading("mutation", false);
      }
    },
    [fetchTemplates, updateLoading]
  );

  /**
   * Fetch report history with filters.
   */
  const fetchHistory = useCallback(
    async (params?: {
      report_type?: string;
      format?: string;
      page?: number;
      size?: number;
    }) => {
      updateLoading("history", true);
      setError(null);

      try {
        const data = await reportsApi.getHistory(params);
        setHistory(data);
        return data;
      } catch (err) {
        const message =
          err instanceof Error ? err.message : "Failed to fetch history";
        setError(message);
        throw err;
      } finally {
        updateLoading("history", false);
      }
    },
    [updateLoading]
  );

  return {
    reportTypes,
    templates,
    history,
    loading,
    error,
    fetchReportTypes,
    fetchTemplates,
    createTemplate,
    updateTemplate,
    deleteTemplate,
    fetchHistory,
  };
}
