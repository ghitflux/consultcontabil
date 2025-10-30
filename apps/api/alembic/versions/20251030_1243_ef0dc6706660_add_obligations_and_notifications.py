"""add_obligations_and_notifications

Revision ID: ef0dc6706660
Revises: f774110e9d18
Create Date: 2025-10-30 12:43:14.470718

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ef0dc6706660'
down_revision = 'f774110e9d18'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enums (if not exist)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE obligationstatus AS ENUM ('pendente', 'em_andamento', 'concluida', 'atrasada', 'cancelada');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    op.execute("""
        DO $$ BEGIN
            CREATE TYPE obligationpriority AS ENUM ('baixa', 'media', 'alta', 'urgente');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    op.execute("""
        DO $$ BEGIN
            CREATE TYPE obligationrecurrence AS ENUM ('mensal', 'bimestral', 'trimestral', 'semestral', 'anual');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    op.execute("""
        DO $$ BEGIN
            CREATE TYPE notificationtype AS ENUM (
                'obligation_created', 'obligation_due_soon', 'obligation_overdue',
                'obligation_completed', 'obligation_canceled',
                'client_created', 'client_updated', 'client_document_uploaded',
                'user_mention', 'user_assigned',
                'system_alert', 'system_maintenance'
            );
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Define enum references for table creation
    obligation_status_enum = postgresql.ENUM(
        'pendente', 'em_andamento', 'concluida', 'atrasada', 'cancelada',
        name='obligationstatus',
        create_type=False
    )

    obligation_priority_enum = postgresql.ENUM(
        'baixa', 'media', 'alta', 'urgente',
        name='obligationpriority',
        create_type=False
    )

    obligation_recurrence_enum = postgresql.ENUM(
        'mensal', 'bimestral', 'trimestral', 'semestral', 'anual',
        name='obligationrecurrence',
        create_type=False
    )

    notification_type_enum = postgresql.ENUM(
        'obligation_created', 'obligation_due_soon', 'obligation_overdue',
        'obligation_completed', 'obligation_canceled',
        'client_created', 'client_updated', 'client_document_uploaded',
        'user_mention', 'user_assigned',
        'system_alert', 'system_maintenance',
        name='notificationtype',
        create_type=False
    )

    # Create obligation_types table
    op.create_table(
        'obligation_types',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False, comment='Nome da obrigação'),
        sa.Column('code', sa.String(50), nullable=False, unique=True, index=True, comment='Código único'),
        sa.Column('description', sa.Text, nullable=True, comment='Descrição detalhada'),

        # Applicability - tipo de empresa
        sa.Column('applies_to_commerce', sa.Boolean, default=False, comment='Aplica para comércio'),
        sa.Column('applies_to_service', sa.Boolean, default=False, comment='Aplica para serviços'),
        sa.Column('applies_to_industry', sa.Boolean, default=False, comment='Aplica para indústria'),
        sa.Column('applies_to_mei', sa.Boolean, default=False, comment='Aplica para MEI'),

        # Applicability - regime tributário
        sa.Column('applies_to_simples', sa.Boolean, default=False, comment='Aplica para Simples Nacional'),
        sa.Column('applies_to_presumido', sa.Boolean, default=False, comment='Aplica para Lucro Presumido'),
        sa.Column('applies_to_real', sa.Boolean, default=False, comment='Aplica para Lucro Real'),

        # Generation settings
        sa.Column('recurrence', obligation_recurrence_enum, nullable=False, comment='Periodicidade'),
        sa.Column('day_of_month', sa.Integer, nullable=True, comment='Dia do mês (1-31)'),
        sa.Column('month_of_year', sa.Integer, nullable=True, comment='Mês do ano (1-12)'),

        sa.Column('is_active', sa.Boolean, default=True, index=True, comment='Ativo/Inativo'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )

    # Create obligations table
    op.create_table(
        'obligations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False, index=True, comment='Cliente associado'),
        sa.Column('obligation_type_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('obligation_types.id', ondelete='RESTRICT'), nullable=False, index=True, comment='Tipo de obrigação'),

        sa.Column('due_date', sa.Date, nullable=False, index=True, comment='Data de vencimento'),
        sa.Column('status', obligation_status_enum, nullable=False, default='pendente', index=True, comment='Status'),
        sa.Column('priority', obligation_priority_enum, nullable=False, default='media', comment='Prioridade'),
        sa.Column('description', sa.Text, nullable=True, comment='Descrição adicional'),

        # Completion info
        sa.Column('receipt_url', sa.String(500), nullable=True, comment='URL do comprovante'),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True, comment='Data/hora de conclusão'),
        sa.Column('completed_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, comment='Usuário que concluiu'),

        # Timestamps
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True, comment='Soft delete'),
    )

    # Create composite indexes for obligations
    op.create_index('idx_obligations_client_due', 'obligations', ['client_id', 'due_date'])
    op.create_index('idx_obligations_status_due', 'obligations', ['status', 'due_date'])
    op.create_index('idx_obligations_type_status', 'obligations', ['obligation_type_id', 'status'])

    # Create obligation_events table
    op.create_table(
        'obligation_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('obligation_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('obligations.id', ondelete='CASCADE'), nullable=False, index=True, comment='Obrigação associada'),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, comment='Usuário que executou a ação'),

        sa.Column('event_type', sa.String(50), nullable=False, comment='Tipo de evento'),
        sa.Column('description', sa.Text, nullable=False, comment='Descrição do evento'),
        sa.Column('extra_data', postgresql.JSONB, nullable=True, comment='Dados adicionais (JSON)'),

        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, index=True),
    )

    # Create notifications table
    op.create_table(
        'notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='Usuário destinatário'),

        sa.Column('type', notification_type_enum, nullable=False, index=True, comment='Tipo de notificação'),
        sa.Column('title', sa.String(200), nullable=False, comment='Título'),
        sa.Column('message', sa.Text, nullable=False, comment='Mensagem'),
        sa.Column('link', sa.String(500), nullable=True, comment='Link relacionado'),
        sa.Column('extra_data', postgresql.JSONB, nullable=True, comment='Dados adicionais (JSON)'),

        sa.Column('read', sa.Boolean, default=False, nullable=False, index=True, comment='Lida?'),
        sa.Column('read_at', sa.DateTime(timezone=True), nullable=True, comment='Data/hora de leitura'),

        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, index=True),
    )

    # Create composite indexes for notifications
    op.create_index('idx_notifications_user_unread', 'notifications', ['user_id', 'read', 'created_at'])
    op.create_index('idx_notifications_user_type', 'notifications', ['user_id', 'type'])


def downgrade() -> None:
    # Drop tables
    op.drop_table('notifications')
    op.drop_table('obligation_events')
    op.drop_table('obligations')
    op.drop_table('obligation_types')

    # Drop enums
    op.execute('DROP TYPE IF EXISTS notificationtype')
    op.execute('DROP TYPE IF EXISTS obligationrecurrence')
    op.execute('DROP TYPE IF EXISTS obligationpriority')
    op.execute('DROP TYPE IF EXISTS obligationstatus')
