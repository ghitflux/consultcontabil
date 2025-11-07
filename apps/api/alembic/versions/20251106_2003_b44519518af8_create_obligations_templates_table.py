"""create_obligations_templates_table

Revision ID: b44519518af8
Revises: d3365fae53fd
Create Date: 2025-11-06 20:03:01.918136

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'b44519518af8'
down_revision = 'd3365fae53fd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create obligations_templates table and required enums."""

    # Create NEW enums only (regime_tributario already exists)
    # Check if enum already exists to avoid errors
    conn = op.get_bind()
    result = conn.execute(sa.text(
        "SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'servico_contratado')"
    ))
    if not result.scalar():
        servico_contratado_enum = postgresql.ENUM(
            'fiscal', 'contabil', 'pessoal',
            name='servico_contratado',
            create_type=True
        )
        servico_contratado_enum.create(conn)

    result = conn.execute(sa.text(
        "SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'obligation_periodicidade')"
    ))
    if not result.scalar():
        obligation_periodicidade_enum = postgresql.ENUM(
            'mensal', 'anual',
            name='obligation_periodicidade',
            create_type=True
        )
        obligation_periodicidade_enum.create(conn)

    # Create obligations_templates table
    op.create_table(
        'obligations_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('nome', sa.String(255), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column(
            'regime_tributario',
            postgresql.ENUM('simples_nacional', 'lucro_presumido', 'lucro_real', 'mei', name='regime_tributario', create_type=False),
            nullable=False
        ),
        sa.Column(
            'servico_contratado',
            postgresql.ENUM('fiscal', 'contabil', 'pessoal', name='servico_contratado', create_type=False),
            nullable=False
        ),
        sa.Column(
            'periodicidade',
            postgresql.ENUM('mensal', 'anual', name='obligation_periodicidade', create_type=False),
            nullable=False
        ),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for efficient querying
    op.create_index('ix_obligations_templates_regime', 'obligations_templates', ['regime_tributario'])
    op.create_index('ix_obligations_templates_servico', 'obligations_templates', ['servico_contratado'])


def downgrade() -> None:
    """Remove obligations_templates table and enums."""

    # Drop indexes
    op.drop_index('ix_obligations_templates_servico', table_name='obligations_templates')
    op.drop_index('ix_obligations_templates_regime', table_name='obligations_templates')

    # Drop table
    op.drop_table('obligations_templates')

    # Drop enums
    obligation_periodicidade_enum = postgresql.ENUM(
        'mensal', 'anual',
        name='obligation_periodicidade'
    )
    obligation_periodicidade_enum.drop(op.get_bind(), checkfirst=True)

    servico_contratado_enum = postgresql.ENUM(
        'fiscal', 'contabil', 'pessoal',
        name='servico_contratado'
    )
    servico_contratado_enum.drop(op.get_bind(), checkfirst=True)
