"""
Integration tests for report routes.

Tests the main report endpoints including types, preview, export, and templates.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.contracts.report.enums import ReportType, ReportFormat


class TestReportRoutes:
    """Test report API endpoints."""

    @pytest.mark.asyncio
    async def test_get_report_types(self, client: AsyncClient, admin_token: str):
        """Test getting available report types."""
        response = await client.get(
            "/api/v1/reports/types",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "types" in data
        assert len(data["types"]) == 11  # All report types

        # Check structure of first type
        first_type = data["types"][0]
        assert "type" in first_type
        assert "name" in first_type
        assert "description" in first_type
        assert "category" in first_type

    @pytest.mark.asyncio
    async def test_preview_report_kpi(self, client: AsyncClient, admin_token: str):
        """Test generating a KPI report preview."""
        response = await client.post(
            "/api/v1/reports/preview",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "report_type": ReportType.KPIS.value,
                "filters": {
                    "period_start": "2025-01-01",
                    "period_end": "2025-01-31",
                    "report_type": ReportType.KPIS.value,
                },
                "customizations": {
                    "include_summary": True,
                    "include_charts": True,
                },
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "report_type" in data
        assert data["report_type"] == ReportType.KPIS.value
        assert "summary" in data
        assert "data" in data

    @pytest.mark.asyncio
    async def test_preview_report_unauthorized(self, client: AsyncClient):
        """Test preview fails without authorization."""
        response = await client.post(
            "/api/v1/reports/preview",
            json={
                "report_type": ReportType.KPIS.value,
                "filters": {
                    "period_start": "2025-01-01",
                    "period_end": "2025-01-31",
                    "report_type": ReportType.KPIS.value,
                },
            },
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_export_report_pdf(self, client: AsyncClient, admin_token: str):
        """Test exporting a report as PDF."""
        response = await client.post(
            "/api/v1/reports/export",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "report_type": ReportType.DRE.value,
                "format": ReportFormat.PDF.value,
                "filters": {
                    "period_start": "2025-01-01",
                    "period_end": "2025-01-31",
                    "report_type": ReportType.DRE.value,
                },
                "customizations": {
                    "include_summary": True,
                    "include_charts": False,
                },
                "filename": "teste-dre",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "report_id" in data
        assert "file_name" in data
        assert data["file_name"].endswith(".pdf")
        assert "file_path" in data
        assert "generated_at" in data

    @pytest.mark.asyncio
    async def test_export_report_csv(self, client: AsyncClient, admin_token: str):
        """Test exporting a report as CSV."""
        response = await client.post(
            "/api/v1/reports/export",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "report_type": ReportType.CLIENTES.value,
                "format": ReportFormat.CSV.value,
                "filters": {
                    "report_type": ReportType.CLIENTES.value,
                },
                "customizations": {
                    "include_summary": False,
                    "include_charts": False,
                },
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "report_id" in data
        assert data["file_name"].endswith(".csv")

    @pytest.mark.asyncio
    async def test_list_templates(self, client: AsyncClient, admin_token: str):
        """Test listing report templates."""
        response = await client.get(
            "/api/v1/reports/templates",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        templates = response.json()
        assert isinstance(templates, list)

        # After seed, we should have system templates
        if templates:
            first = templates[0]
            assert "id" in first
            assert "name" in first
            assert "report_type" in first
            assert "is_system" in first

    @pytest.mark.asyncio
    async def test_create_template(self, client: AsyncClient, admin_token: str):
        """Test creating a custom template."""
        response = await client.post(
            "/api/v1/reports/templates",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "name": "Template de Teste",
                "description": "Template criado durante teste",
                "report_type": ReportType.KPIS.value,
                "default_filters": {
                    "period_start": "2025-01-01",
                    "period_end": "2025-12-31",
                    "report_type": ReportType.KPIS.value,
                },
                "default_customizations": {
                    "include_summary": True,
                    "include_charts": True,
                },
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Template de Teste"
        assert data["is_system"] == False
        assert "id" in data

        # Clean up: delete the template
        await client.delete(
            f"/api/v1/reports/templates/{data['id']}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

    @pytest.mark.asyncio
    async def test_get_history(self, client: AsyncClient, admin_token: str):
        """Test getting report generation history."""
        # First generate a report
        await client.post(
            "/api/v1/reports/export",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "report_type": ReportType.KPIS.value,
                "format": ReportFormat.PDF.value,
                "filters": {
                    "period_start": "2025-01-01",
                    "period_end": "2025-01-31",
                    "report_type": ReportType.KPIS.value,
                },
            },
        )

        # Now check history
        response = await client.get(
            "/api/v1/reports/history",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data

        if data["items"]:
            first = data["items"][0]
            assert "id" in first
            assert "report_type" in first
            assert "format" in first
            assert "generated_at" in first

    @pytest.mark.asyncio
    async def test_history_with_filters(self, client: AsyncClient, admin_token: str):
        """Test filtering history by report type."""
        response = await client.get(
            "/api/v1/reports/history?report_type=kpis&format=pdf",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "items" in data

        # All returned items should match filters
        for item in data["items"]:
            assert item["report_type"] == "kpis"
            assert item["format"] == "pdf"

    @pytest.mark.asyncio
    async def test_cliente_cannot_access_admin_reports(
        self, client: AsyncClient, cliente_token: str
    ):
        """Test that clients cannot access admin-only reports."""
        response = await client.post(
            "/api/v1/reports/preview",
            headers={"Authorization": f"Bearer {cliente_token}"},
            json={
                "report_type": ReportType.AUDITORIA.value,  # Admin only
                "filters": {
                    "period_start": "2025-01-01",
                    "period_end": "2025-01-31",
                    "report_type": ReportType.AUDITORIA.value,
                },
            },
        )

        # Should be forbidden
        assert response.status_code in [403, 401]

    @pytest.mark.asyncio
    async def test_invalid_report_type(self, client: AsyncClient, admin_token: str):
        """Test preview with invalid report type."""
        response = await client.post(
            "/api/v1/reports/preview",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "report_type": "invalid_type",
                "filters": {
                    "period_start": "2025-01-01",
                    "period_end": "2025-01-31",
                    "report_type": "invalid_type",
                },
            },
        )

        assert response.status_code == 422  # Validation error
