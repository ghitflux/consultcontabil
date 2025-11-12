"""add_client_users_relationship_table

Revision ID: f329c1a83bf3
Revises: 7aff3ebd7a1f
Create Date: 2025-11-11 10:46:37.048475

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'f329c1a83bf3'
down_revision = '7aff3ebd7a1f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Note: client_access_level enum must be created manually before running this migration:
    # DO $$ BEGIN CREATE TYPE client_access_level AS ENUM ('OWNER', 'MANAGER', 'VIEWER'); EXCEPTION WHEN duplicate_object THEN null; END $$;

    # Create client_users relationship table
    # Using text for access_level to reference the existing enum without SQLAlchemy trying to create it
    conn = op.get_bind()
    conn.execute(sa.text("""
        CREATE TABLE client_users (
            id UUID PRIMARY KEY,
            client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
            user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            access_level client_access_level NOT NULL DEFAULT 'VIEWER'::client_access_level,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            CONSTRAINT uq_client_users_client_user UNIQUE (client_id, user_id)
        )
    """))

    # Create indexes for better query performance
    op.create_index('ix_client_users_client_id', 'client_users', ['client_id'])
    op.create_index('ix_client_users_user_id', 'client_users', ['user_id'])

    # Add optional primary_client_id to users table for quick access
    op.add_column('users', sa.Column('primary_client_id', sa.UUID(), nullable=True))
    op.create_foreign_key('fk_users_primary_client', 'users', 'clients', ['primary_client_id'], ['id'], ondelete='SET NULL')
    op.create_index('ix_users_primary_client_id', 'users', ['primary_client_id'])


def downgrade() -> None:
    # Remove primary_client_id from users
    op.drop_index('ix_users_primary_client_id', table_name='users')
    op.drop_constraint('fk_users_primary_client', 'users', type_='foreignkey')
    op.drop_column('users', 'primary_client_id')

    # Drop client_users table
    op.drop_index('ix_client_users_user_id', table_name='client_users')
    op.drop_index('ix_client_users_client_id', table_name='client_users')
    op.drop_table('client_users')

    # Drop access_level enum
    sa.Enum(name='client_access_level').drop(op.get_bind(), checkfirst=True)
