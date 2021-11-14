"""add content column to posts table

Revision ID: 51914464aeb0
Revises: 0665fd5a0964
Create Date: 2021-11-14 20:53:03.877653

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = '51914464aeb0'
down_revision = '0665fd5a0964'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
