/**
 * Hook for previewing reports.
 */

import { reportsApi } from "@/lib/api/endpoints/reports";
import type {
  ReportPreviewRequest,
  ReportPreviewResponse,
} from "@/types/report";
import { useCallback, useState } from "react";

export function useReportPreview() {
  const [preview, setPreview] = useState<ReportPreviewResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Generate a preview of the report.
   */
  const previewReport = useCallback(async (request: ReportPreviewRequest) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await reportsApi.previewReport(request);
      setPreview(data);
      return data;
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Failed to preview report";
      setError(message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * Clear the current preview.
   */
  const clearPreview = useCallback(() => {
    setPreview(null);
    setError(null);
  }, []);

  return {
    preview,
    isLoading,
    error,
    previewReport,
    clearPreview,
  };
}

