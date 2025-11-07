"""change_client_status_default_to_ativo

Revision ID: 7aff3ebd7a1f
Revises: e36a219511ce
Create Date: 2025-11-07 10:33:46.693551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7aff3ebd7a1f'
down_revision = 'e36a219511ce'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Alterar o default da coluna status de 'PENDENTE' para 'ATIVO'
    op.alter_column('clients', 'status',
                    server_default='ATIVO',
                    existing_nullable=False)


def downgrade() -> None:
    # Reverter para 'PENDENTE'
    op.alter_column('clients', 'status',
                    server_default='PENDENTE',
                    existing_nullable=False)
