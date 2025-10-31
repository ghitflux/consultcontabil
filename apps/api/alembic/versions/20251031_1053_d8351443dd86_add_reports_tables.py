"""add_reports_tables

Revision ID: 20251031_1053
Revises: 20251030_2330
Create Date: 2025-10-31 10:53:37.173886

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20251031_1053'
down_revision = '20251030_2330'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create report_templates table
    op.create_table(
        'report_templates',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False, comment='Template name'),
        sa.Column('description', sa.Text(), nullable=True, comment='Template description'),
        sa.Column('report_type', sa.Enum('dre', 'fluxo_caixa', 'livro_caixa', 'receitas_cliente', 'despesas_categoria', 'projecao_fluxo', 'kpis', 'clientes', 'obrigacoes', 'licencas', 'auditoria', name='report_type'), nullable=False),
        sa.Column('default_filters', sa.JSON(), nullable=False, comment='Default filters for the report'),
        sa.Column('default_customizations', sa.JSON(), nullable=True, comment='Default customization options'),
        sa.Column('is_system', sa.Boolean(), nullable=False, default=False, comment='System templates cannot be modified by users'),
        sa.Column('created_by_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], name='fk_report_templates_created_by_id'),
        sa.PrimaryKeyConstraint('id', name='pk_report_templates')
    )

    # Create indexes for report_templates
    op.create_index('ix_report_templates_name', 'report_templates', ['name'], unique=False)
    op.create_index('ix_report_templates_report_type', 'report_templates', ['report_type'], unique=False)
    op.create_index('ix_report_templates_created_by_id', 'report_templates', ['created_by_id'], unique=False)

    # Create report_history table
    op.create_table(
        'report_history',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('template_id', sa.UUID(), nullable=True),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('report_type', sa.Enum('dre', 'fluxo_caixa', 'livro_caixa', 'receitas_cliente', 'despesas_categoria', 'projecao_fluxo', 'kpis', 'clientes', 'obrigacoes', 'licencas', 'auditoria', name='report_type'), nullable=False),
        sa.Column('filters_used', sa.JSON(), nullable=False, comment='Filters used when generating this report'),
        sa.Column('format', sa.Enum('pdf', 'csv', name='report_format'), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=True, comment='Path to generated file'),
        sa.Column('file_size', sa.Integer(), nullable=True, comment='File size in bytes'),
        sa.Column('generated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True, comment='File expiration datetime (default: 7 days after generation)'),
        sa.Column('status', sa.Enum('pending', 'completed', 'failed', name='report_status'), nullable=False, default='pending'),
        sa.ForeignKeyConstraint(['template_id'], ['report_templates.id'], name='fk_report_history_template_id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_report_history_user_id'),
        sa.PrimaryKeyConstraint('id', name='pk_report_history')
    )

    # Create indexes for report_history
    op.create_index('ix_report_history_user_id', 'report_history', ['user_id'], unique=False)
    op.create_index('ix_report_history_template_id', 'report_history', ['template_id'], unique=False)
    op.create_index('ix_report_history_report_type', 'report_history', ['report_type'], unique=False)
    op.create_index('ix_report_history_format', 'report_history', ['format'], unique=False)
    op.create_index('ix_report_history_status', 'report_history', ['status'], unique=False)
    op.create_index('ix_report_history_generated_at', 'report_history', ['generated_at'], unique=False)
    op.create_index('ix_report_history_user_report_type', 'report_history', ['user_id', 'report_type'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_report_history_user_report_type', table_name='report_history')
    op.drop_index('ix_report_history_generated_at', table_name='report_history')
    op.drop_index('ix_report_history_status', table_name='report_history')
    op.drop_index('ix_report_history_format', table_name='report_history')
    op.drop_index('ix_report_history_report_type', table_name='report_history')
    op.drop_index('ix_report_history_template_id', table_name='report_history')
    op.drop_index('ix_report_history_user_id', table_name='report_history')

    op.drop_index('ix_report_templates_created_by_id', table_name='report_templates')
    op.drop_index('ix_report_templates_report_type', table_name='report_templates')
    op.drop_index('ix_report_templates_name', table_name='report_templates')

    # Drop tables (enums will be dropped automatically via CASCADE)
    op.drop_table('report_history')
    op.drop_table('report_templates')
