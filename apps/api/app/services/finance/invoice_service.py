"""Invoice Service - Generate and manage invoices/receipts."""

import io
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import UUID

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.transaction import TransactionRepository

logger = logging.getLogger(__name__)


class InvoiceService:
    """Service for generating invoices and receipts."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.transaction_repo = TransactionRepository(db)
        self.output_dir = Path("var/invoices")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_invoice_pdf(
        self,
        transaction_id: UUID,
        save_to_file: bool = True,
    ) -> bytes:
        """
        Generate invoice PDF for a transaction.

        Args:
            transaction_id: Transaction UUID
            save_to_file: Whether to save PDF to file

        Returns:
            PDF bytes

        Raises:
            ValueError: If transaction not found
        """
        # Get transaction with relationships
        transaction = await self.transaction_repo.get_by_id_with_relations(
            transaction_id
        )

        if not transaction:
            raise ValueError(f"Transaction with ID {transaction_id} not found")

        # Generate PDF
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Company header
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(2 * cm, height - 2 * cm, "CONTABILCONSULT")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(2 * cm, height - 2.5 * cm, "CNPJ: 12.345.678/0001-90")
        pdf.drawString(2 * cm, height - 3 * cm, "Endereço: Rua Exemplo, 123 - São Paulo/SP")
        pdf.drawString(2 * cm, height - 3.5 * cm, "Tel: (11) 1234-5678")
        pdf.drawString(2 * cm, height - 4 * cm, "Email: contato@contabilconsult.com.br")

        # Invoice title
        pdf.setFont("Helvetica-Bold", 18)
        invoice_title = "NOTA FISCAL" if transaction.payment_status == "pago" else "FATURA"
        pdf.drawString(width / 2 - 3 * cm, height - 5.5 * cm, invoice_title)

        # Invoice number
        pdf.setFont("Helvetica", 10)
        invoice_number = transaction.invoice_number or f"NF-{transaction.id.hex[:8].upper()}"
        pdf.drawString(2 * cm, height - 6.5 * cm, f"Número: {invoice_number}")
        pdf.drawString(2 * cm, height - 7 * cm, f"Data de Emissão: {datetime.now().strftime('%d/%m/%Y')}")

        # Client info
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(2 * cm, height - 8.5 * cm, "DADOS DO CLIENTE")
        pdf.setFont("Helvetica", 10)

        if transaction.client:
            pdf.drawString(2 * cm, height - 9 * cm, f"Razão Social: {transaction.client.razao_social}")
            pdf.drawString(2 * cm, height - 9.5 * cm, f"CNPJ: {transaction.client.cnpj}")
            if transaction.client.endereco:
                pdf.drawString(2 * cm, height - 10 * cm, f"Endereço: {transaction.client.endereco}")
            if transaction.client.email:
                pdf.drawString(2 * cm, height - 10.5 * cm, f"Email: {transaction.client.email}")
            if transaction.client.telefone:
                pdf.drawString(2 * cm, height - 11 * cm, f"Telefone: {transaction.client.telefone}")

        # Services/Items table
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(2 * cm, height - 12.5 * cm, "DESCRIÇÃO DOS SERVIÇOS")

        # Table data
        data = [
            ["Descrição", "Ref. Mês", "Valor"],
            [
                transaction.description,
                transaction.reference_month.strftime("%m/%Y"),
                f"R$ {transaction.amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            ],
        ]

        # Create table
        table_y = height - 14 * cm
        col_widths = [10 * cm, 3 * cm, 3 * cm]

        for i, row in enumerate(data):
            y_position = table_y - (i * 0.7 * cm)

            if i == 0:
                pdf.setFont("Helvetica-Bold", 10)
            else:
                pdf.setFont("Helvetica", 10)

            x_position = 2 * cm
            for j, cell in enumerate(row):
                pdf.drawString(x_position, y_position, str(cell))
                x_position += col_widths[j]

        # Draw table borders
        pdf.rect(2 * cm, table_y - 1 * cm, sum(col_widths), 1.4 * cm)
        pdf.line(2 * cm, table_y - 0.3 * cm, 2 * cm + sum(col_widths), table_y - 0.3 * cm)

        # Totals
        pdf.setFont("Helvetica-Bold", 12)
        total_y = table_y - 2.5 * cm
        pdf.drawString(11 * cm, total_y, "VALOR TOTAL:")
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(
            14 * cm,
            total_y,
            f"R$ {transaction.amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        )

        # Payment info
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(2 * cm, total_y - 1.5 * cm, "INFORMAÇÕES DE PAGAMENTO")
        pdf.setFont("Helvetica", 10)

        pdf.drawString(2 * cm, total_y - 2 * cm, f"Vencimento: {transaction.due_date.strftime('%d/%m/%Y')}")

        if transaction.payment_status == "pago" and transaction.paid_date:
            pdf.drawString(
                2 * cm,
                total_y - 2.5 * cm,
                f"Data do Pagamento: {transaction.paid_date.strftime('%d/%m/%Y %H:%M')}",
            )
            if transaction.payment_method:
                pdf.drawString(
                    2 * cm,
                    total_y - 3 * cm,
                    f"Forma de Pagamento: {transaction.payment_method.upper()}",
                )

        # Payment instructions (if not paid)
        if transaction.payment_status != "pago":
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(2 * cm, total_y - 4 * cm, "INSTRUÇÕES PARA PAGAMENTO:")
            pdf.setFont("Helvetica", 9)
            pdf.drawString(2 * cm, total_y - 4.5 * cm, "1. PIX: CNPJ 12.345.678/0001-90")
            pdf.drawString(2 * cm, total_y - 5 * cm, "2. Transferência: Banco do Brasil - Ag: 1234-5 - CC: 12345-6")
            pdf.drawString(
                2 * cm,
                total_y - 5.5 * cm,
                "3. Após o pagamento, enviar comprovante para financeiro@contabilconsult.com.br",
            )

        # Notes
        if transaction.notes:
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(2 * cm, total_y - 7 * cm, "OBSERVAÇÕES:")
            pdf.setFont("Helvetica", 9)

            # Wrap text if too long
            notes_lines = transaction.notes.split("\n")
            y_offset = 0
            for line in notes_lines[:5]:  # Max 5 lines
                pdf.drawString(2 * cm, total_y - 7.5 * cm - y_offset, line[:80])
                y_offset += 0.5 * cm

        # Footer
        footer_y = 3 * cm
        pdf.setFont("Helvetica", 8)
        pdf.drawCentredString(
            width / 2,
            footer_y,
            "Este documento foi gerado eletronicamente e não necessita de assinatura.",
        )
        pdf.drawCentredString(
            width / 2,
            footer_y - 0.5 * cm,
            f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
        )

        # Page number
        pdf.drawRightString(width - 2 * cm, 1.5 * cm, "Página 1 de 1")

        # Save PDF
        pdf.save()

        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()

        # Save to file if requested
        if save_to_file:
            filename = f"invoice_{transaction_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = self.output_dir / filename

            with open(filepath, "wb") as f:
                f.write(pdf_bytes)

            logger.info(f"Invoice PDF saved to {filepath}")

            # Update transaction with file path
            transaction.receipt_url = f"/invoices/{filename}"
            await self.db.commit()

        return pdf_bytes

    async def generate_receipt_pdf(
        self,
        transaction_id: UUID,
        save_to_file: bool = True,
    ) -> bytes:
        """
        Generate payment receipt PDF for a paid transaction.

        Args:
            transaction_id: Transaction UUID
            save_to_file: Whether to save PDF to file

        Returns:
            PDF bytes

        Raises:
            ValueError: If transaction not found or not paid
        """
        # Get transaction
        transaction = await self.transaction_repo.get_by_id_with_relations(
            transaction_id
        )

        if not transaction:
            raise ValueError(f"Transaction with ID {transaction_id} not found")

        if transaction.payment_status != "pago":
            raise ValueError("Cannot generate receipt for unpaid transaction")

        # For now, use the same PDF generation as invoice
        # In a real scenario, you might want a different layout for receipts
        return await self.generate_invoice_pdf(transaction_id, save_to_file)

    async def get_invoice_path(self, transaction_id: UUID) -> Optional[Path]:
        """
        Get the file path for an existing invoice.

        Args:
            transaction_id: Transaction UUID

        Returns:
            Path to invoice PDF or None if not found
        """
        # Check if invoice exists
        files = list(self.output_dir.glob(f"invoice_{transaction_id}_*.pdf"))

        if files:
            # Return most recent file
            return sorted(files, reverse=True)[0]

        return None

    def cleanup_old_invoices(self, days: int = 90):
        """
        Clean up invoice PDFs older than specified days.

        Args:
            days: Number of days to keep invoices

        Returns:
            Number of files deleted
        """
        if not self.output_dir.exists():
            return 0

        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        deleted_count = 0

        for file in self.output_dir.glob("invoice_*.pdf"):
            if file.stat().st_mtime < cutoff_date:
                file.unlink()
                deleted_count += 1
                logger.info(f"Deleted old invoice: {file.name}")

        return deleted_count
