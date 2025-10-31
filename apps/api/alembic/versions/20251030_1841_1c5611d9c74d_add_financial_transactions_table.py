"""add_financial_transactions_table

Revision ID: 1c5611d9c74d
Revises: ef0dc6706660
Create Date: 2025-10-30 18:41:27.075581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c5611d9c74d'
down_revision = 'ef0dc6706660'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create financial_transactions table
    op.create_table(
        'financial_transactions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('client_id', sa.UUID(), nullable=False),
        sa.Column('obligation_id', sa.UUID(), nullable=True),
        sa.Column('created_by_id', sa.UUID(), nullable=False),
        sa.Column('transaction_type', sa.String(length=10), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False, comment='Transaction amount in BRL'),
        sa.Column('payment_method', sa.String(length=20), nullable=True),
        sa.Column('payment_status', sa.String(length=15), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False, comment='Payment due date'),
        sa.Column('paid_date', sa.DateTime(), nullable=True, comment='Date when payment was received'),
        sa.Column('reference_month', sa.Date(), nullable=False, comment='Reference month (competência)'),
        sa.Column('description', sa.String(length=500), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('invoice_number', sa.String(length=100), nullable=True),
        sa.Column('receipt_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], name='fk_financial_transactions_client_id'),
        sa.ForeignKeyConstraint(['obligation_id'], ['obligations.id'], name='fk_financial_transactions_obligation_id'),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], name='fk_financial_transactions_created_by_id'),
        sa.PrimaryKeyConstraint('id', name='pk_financial_transactions')
    )

    # Create indexes for performance
    op.create_index('ix_financial_transactions_client_id', 'financial_transactions', ['client_id'])
    op.create_index('ix_financial_transactions_payment_status', 'financial_transactions', ['payment_status'])
    op.create_index('ix_financial_transactions_due_date', 'financial_transactions', ['due_date'])
    op.create_index('ix_financial_transactions_reference_month', 'financial_transactions', ['reference_month'])
    op.create_index('ix_financial_transactions_created_at', 'financial_transactions', ['created_at'])
    op.create_index('ix_financial_transactions_deleted_at', 'financial_transactions', ['deleted_at'])

    # Composite indexes for common queries
    op.create_index('ix_financial_transactions_client_status', 'financial_transactions', ['client_id', 'payment_status'])
    op.create_index('ix_financial_transactions_client_reference', 'financial_transactions', ['client_id', 'reference_month'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_financial_transactions_client_reference', 'financial_transactions')
    op.drop_index('ix_financial_transactions_client_status', 'financial_transactions')
    op.drop_index('ix_financial_transactions_deleted_at', 'financial_transactions')
    op.drop_index('ix_financial_transactions_created_at', 'financial_transactions')
    op.drop_index('ix_financial_transactions_reference_month', 'financial_transactions')
    op.drop_index('ix_financial_transactions_due_date', 'financial_transactions')
    op.drop_index('ix_financial_transactions_payment_status', 'financial_transactions')
    op.drop_index('ix_financial_transactions_client_id', 'financial_transactions')

    # Drop table
    op.drop_table('financial_transactions')
