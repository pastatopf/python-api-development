"""Add user table

Revision ID: 0564cb9914c2
Revises: 51914464aeb0
Create Date: 2021-11-14 20:57:38.471428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0564cb9914c2'
down_revision = '51914464aeb0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
