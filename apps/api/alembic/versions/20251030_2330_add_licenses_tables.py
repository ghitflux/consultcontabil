"""add licenses tables

Revision ID: 20251030_2330
Revises: 1c5611d9c74d
Create Date: 2025-10-30 23:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20251030_2330'
down_revision = '1c5611d9c74d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create CNAE enum
    op.execute("CREATE TYPE cnaetype AS ENUM ('PRINCIPAL', 'SECUNDARIO')")

    # Create License enums
    op.execute("""
        CREATE TYPE licensetype AS ENUM (
            'ALVARA_FUNCIONAMENTO',
            'INSCRICAO_MUNICIPAL',
            'INSCRICAO_ESTADUAL',
            'CERTIFICADO_DIGITAL',
            'LICENCA_AMBIENTAL',
            'LICENCA_SANITARIA',
            'LICENCA_BOMBEIROS',
            'OUTROS'
        )
    """)

    op.execute("""
        CREATE TYPE licensestatus AS ENUM (
            'ATIVA',
            'VENCIDA',
            'PENDENTE_RENOVACAO',
            'EM_PROCESSO',
            'CANCELADA',
            'SUSPENSA'
        )
    """)

    op.execute("""
        CREATE TYPE licenseeventtype AS ENUM (
            'CREATED',
            'ISSUED',
            'RENEWED',
            'EXPIRED',
            'CANCELLED',
            'SUSPENDED',
            'REACTIVATED',
            'UPDATED',
            'DOCUMENT_UPLOADED'
        )
    """)

    # Create Municipal Registration enum
    op.execute("""
        CREATE TYPE municipalregistrationstatus AS ENUM (
            'ATIVA',
            'INATIVA',
            'SUSPENSA',
            'PENDENTE',
            'CANCELADA'
        )
    """)

    op.execute("""
        CREATE TYPE statecode AS ENUM (
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
            'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
            'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        )
    """)

    # Create CNAEs table
    op.create_table('cnaes',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('client_id', sa.UUID(), nullable=False, comment='Cliente associado'),
        sa.Column('cnae_code', sa.String(length=10), nullable=False, comment='Código CNAE (formato: 0000-0/00)'),
        sa.Column('description', sa.String(length=500), nullable=False, comment='Descrição da atividade'),
        sa.Column('cnae_type', postgresql.ENUM(name='cnaetype', create_type=False), nullable=False, comment='Tipo: principal ou secundário'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true', comment='Se o CNAE está ativo'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('client_id', 'cnae_code', name='uq_client_cnae')
    )
    op.create_index('ix_cnaes_client_active', 'cnaes', ['client_id', 'is_active'])
    op.create_index(op.f('ix_cnaes_client_id'), 'cnaes', ['client_id'])
    op.create_index('ix_cnaes_client_type', 'cnaes', ['client_id', 'cnae_type'])
    op.create_index(op.f('ix_cnaes_cnae_code'), 'cnaes', ['cnae_code'])
    op.create_index(op.f('ix_cnaes_cnae_type'), 'cnaes', ['cnae_type'])
    op.create_index(op.f('ix_cnaes_is_active'), 'cnaes', ['is_active'])

    # Create Licenses table
    op.create_table('licenses',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('client_id', sa.UUID(), nullable=False, comment='Cliente associado'),
        sa.Column('license_type', postgresql.ENUM(name='licensetype', create_type=False), nullable=False, comment='Tipo de licença'),
        sa.Column('registration_number', sa.String(length=100), nullable=False, comment='Número de registro/licença'),
        sa.Column('issuing_authority', sa.String(length=200), nullable=False, comment='Órgão emissor'),
        sa.Column('issue_date', sa.Date(), nullable=False, comment='Data de emissão'),
        sa.Column('expiration_date', sa.Date(), nullable=True, comment='Data de vencimento'),
        sa.Column('status', postgresql.ENUM(name='licensestatus', create_type=False), nullable=False, server_default='EM_PROCESSO', comment='Status da licença'),
        sa.Column('notes', sa.Text(), nullable=True, comment='Notas adicionais'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('expiration_date IS NULL OR expiration_date > issue_date', name='check_expiration_after_issue'),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_licenses_client_id'), 'licenses', ['client_id'])
    op.create_index('ix_licenses_client_type', 'licenses', ['client_id', 'license_type'])
    op.create_index(op.f('ix_licenses_expiration_date'), 'licenses', ['expiration_date'])
    op.create_index(op.f('ix_licenses_license_type'), 'licenses', ['license_type'])
    op.create_index(op.f('ix_licenses_registration_number'), 'licenses', ['registration_number'])
    op.create_index(op.f('ix_licenses_status'), 'licenses', ['status'])
    op.create_index('ix_licenses_status_expiration', 'licenses', ['status', 'expiration_date'])

    # Create Municipal Registrations table
    op.create_table('municipal_registrations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('client_id', sa.UUID(), nullable=False, comment='Cliente associado'),
        sa.Column('city', sa.String(length=100), nullable=False, comment='Cidade'),
        sa.Column('state', postgresql.ENUM(name='statecode', create_type=False), nullable=False, comment='Estado (UF)'),
        sa.Column('registration_number', sa.String(length=50), nullable=False, comment='Número da inscrição municipal (CCM)'),
        sa.Column('issue_date', sa.Date(), nullable=False, comment='Data de emissão'),
        sa.Column('status', postgresql.ENUM(name='municipalregistrationstatus', create_type=False), nullable=False, server_default='PENDENTE', comment='Status da inscrição'),
        sa.Column('notes', sa.Text(), nullable=True, comment='Notas adicionais'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('city', 'state', 'registration_number', name='uq_city_state_registration')
    )
    op.create_index('ix_mun_reg_client_status', 'municipal_registrations', ['client_id', 'status'])
    op.create_index('ix_mun_reg_state_city', 'municipal_registrations', ['state', 'city'])
    op.create_index(op.f('ix_municipal_registrations_city'), 'municipal_registrations', ['city'])
    op.create_index(op.f('ix_municipal_registrations_client_id'), 'municipal_registrations', ['client_id'])
    op.create_index(op.f('ix_municipal_registrations_registration_number'), 'municipal_registrations', ['registration_number'])
    op.create_index(op.f('ix_municipal_registrations_state'), 'municipal_registrations', ['state'])
    op.create_index(op.f('ix_municipal_registrations_status'), 'municipal_registrations', ['status'])

    # Create License Events table
    op.create_table('license_events',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('license_id', sa.UUID(), nullable=False, comment='Licença associada'),
        sa.Column('user_id', sa.UUID(), nullable=True, comment='Usuário que executou a ação'),
        sa.Column('event_type', postgresql.ENUM(name='licenseeventtype', create_type=False), nullable=False, comment='Tipo de evento'),
        sa.Column('description', sa.Text(), nullable=False, comment='Descrição do evento'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Data/hora do evento'),
        sa.ForeignKeyConstraint(['license_id'], ['licenses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_license_events_created_at'), 'license_events', ['created_at'])
    op.create_index(op.f('ix_license_events_event_type'), 'license_events', ['event_type'])
    op.create_index('ix_license_events_license_created', 'license_events', ['license_id', 'created_at'])
    op.create_index(op.f('ix_license_events_license_id'), 'license_events', ['license_id'])
    op.create_index('ix_license_events_type_created', 'license_events', ['event_type', 'created_at'])


def downgrade() -> None:
    # Drop tables
    op.drop_table('license_events')
    op.drop_table('municipal_registrations')
    op.drop_table('licenses')
    op.drop_table('cnaes')

    # Drop enums
    op.execute('DROP TYPE IF EXISTS licenseeventtype')
    op.execute('DROP TYPE IF EXISTS municipalregistrationstatus')
    op.execute('DROP TYPE IF EXISTS statecode')
    op.execute('DROP TYPE IF EXISTS licensestatus')
    op.execute('DROP TYPE IF EXISTS licensetype')
    op.execute('DROP TYPE IF EXISTS cnaetype')
