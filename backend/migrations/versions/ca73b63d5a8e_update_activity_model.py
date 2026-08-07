"""Update activity model

Revision ID: ca73b63d5a8e
Revises: 44711eeecf0a
Create Date: 2026-08-02 23:24:22.121647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca73b63d5a8e'
down_revision = '44711eeecf0a'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('activities', schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                'icon',
                sa.String(length=10),
                nullable=False,
                server_default="🔔"
            )
        )

        batch_op.drop_column('activity_type')


def downgrade():

    with op.batch_alter_table('activities', schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                'activity_type',
                sa.String(length=100),
                nullable=False,
                server_default="general"
            )
        )

        batch_op.drop_column('icon')
