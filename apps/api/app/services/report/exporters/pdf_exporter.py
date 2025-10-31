"""PDF Report Exporter using ReportLab."""

import io
from datetime import datetime
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.services.report.exporters.base import BaseExporter


class PDFExporter(BaseExporter):
    """PDF exporter for reports using ReportLab."""

    async def export(self, data: dict[str, Any], filename: str) -> tuple[bytes, Path]:
        """
        Export report data to PDF.

        Args:
            data: Report data dictionary
            filename: Output filename

        Returns:
            Tuple of (pdf_bytes, file_path)
        """
        # Generate PDF in memory
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Draw header
        self._draw_header(pdf, width, height)
        y_position = height - 4 * cm

        # Draw title and period
        pdf.setFont("Helvetica-Bold", 16)
        title = data.get("title", "RELATÓRIO")
        pdf.drawString(2 * cm, y_position, title)

        y_position -= 1 * cm

        # Draw metadata
        pdf.setFont("Helvetica", 10)
        if "period" in data:
            pdf.drawString(2 * cm, y_position, f"Período: {data['period']}")
            y_position -= 0.5 * cm

        pdf.drawString(
            2 * cm, y_position, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )

        y_position -= 1.5 * cm

        # Draw summary section
        if "summary" in data:
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(2 * cm, y_position, "RESUMO")
            y_position -= 0.8 * cm

            pdf.setFont("Helvetica", 10)
            for key, value in data["summary"].items():
                pdf.drawString(
                    2 * cm, y_position, f"{self._format_key(key)}: {self._format_value(value)}"
                )
                y_position -= 0.6 * cm

            y_position -= 0.5 * cm

        # Draw main data table
        if "table_data" in data:
            y_position = self._draw_table(pdf, width, y_position, data["table_data"])

        # Draw footer
        self._draw_footer(pdf, width, height)

        # Save PDF
        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        pdf_bytes = buffer.read()

        # Save to file
        file_path = self._save_to_file(pdf_bytes, filename)

        return pdf_bytes, file_path

    def _draw_header(self, pdf: canvas.Canvas, width: float, height: float) -> None:
        """Draw PDF header with company info."""
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(2 * cm, height - 1.5 * cm, "CONTABILCONSULT")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(2 * cm, height - 1.8 * cm, "Sistema de Gestão Contábil")
        pdf.line(2 * cm, height - 2.2 * cm, width - 2 * cm, height - 2.2 * cm)

    def _draw_footer(self, pdf: canvas.Canvas, width: float, height: float) -> None:
        """Draw PDF footer with page numbers."""
        pdf.setFont("Helvetica", 8)
        footer_text = f"Gerado por ContabilConsult em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        text_width = pdf.stringWidth(footer_text, "Helvetica", 8)
        pdf.drawString((width - text_width) / 2, 1 * cm, footer_text)

    def _draw_table(
        self, pdf: canvas.Canvas, width: float, y_start: float, table_data: list[list[str]]
    ) -> float:
        """
        Draw a data table.

        Args:
            pdf: Canvas object
            width: Page width
            y_start: Starting Y position
            table_data: Table data as list of rows

        Returns:
            Y position after table
        """
        if not table_data:
            return y_start

        pdf.setFont("Helvetica-Bold", 10)
        # Draw header row
        header = table_data[0]
        col_widths = self._calculate_column_widths(width, len(header))

        x_start = 2 * cm
        y = y_start

        # Draw header
        pdf.rect(x_start, y, sum(col_widths), 0.7 * cm)
        for i, cell in enumerate(header):
            pdf.drawString(x_start + col_widths[i] * 0.1, y + 0.4 * cm, str(cell))
            x_start += col_widths[i]

        # Draw data rows
        pdf.setFont("Helvetica", 9)
        for row in table_data[1:]:
            x_start = 2 * cm
            y -= 0.6 * cm
            pdf.rect(x_start, y, sum(col_widths), 0.6 * cm)
            for i, cell in enumerate(row):
                pdf.drawString(x_start + col_widths[i] * 0.1, y + 0.3 * cm, str(cell))
                x_start += col_widths[i]

        return y

    def _calculate_column_widths(self, page_width: float, num_cols: int) -> list[float]:
        """Calculate column widths for table."""
        total_width = page_width - 4 * cm  # Margins
        col_width = total_width / num_cols
        return [col_width] * num_cols

    def _format_key(self, key: str) -> str:
        """Format dictionary key for display."""
        key_map = {
            "total_revenue": "Receita Total",
            "total_expenses": "Despesa Total",
            "net_result": "Resultado Líquido",
            "profit_margin": "Margem de Lucro",
            "compliance_rate": "Taxa de Compliance",
        }
        return key_map.get(key, key.replace("_", " ").title())

    def _format_value(self, value: Any) -> str:
        """Format value for display."""
        if isinstance(value, float):
            if isinstance(value, float) and value > 100:  # Likely a percentage
                return f"{value:,.2f}%"
            return f"{value:,.2f}"
        if isinstance(value, (int, str)):
            return str(value)
        return str(value)

    def _save_to_file(self, pdf_bytes: bytes, filename: str) -> Path:
        """Save PDF bytes to file."""
        # Create subdirectory by date
        today = datetime.now().strftime("%Y%m%d")
        subdir = self._ensure_directory(today)

        # Ensure .pdf extension
        if not filename.endswith(".pdf"):
            filename += ".pdf"

        file_path = subdir / filename
        file_path.write_bytes(pdf_bytes)

        return file_path

