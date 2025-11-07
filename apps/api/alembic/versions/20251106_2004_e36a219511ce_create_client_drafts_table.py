"""create_client_drafts_table

Revision ID: e36a219511ce
Revises: b44519518af8
Create Date: 2025-11-06 20:04:41.766797

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'e36a219511ce'
down_revision = 'b44519518af8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create client_drafts table."""

    op.create_table(
        'client_drafts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('draft_data', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', name='uq_client_drafts_user_id')
    )

    # Create index for efficient querying
    op.create_index('ix_client_drafts_user_id', 'client_drafts', ['user_id'])


def downgrade() -> None:
    """Remove client_drafts table."""

    op.drop_index('ix_client_drafts_user_id', table_name='client_drafts')
    op.drop_table('client_drafts')
