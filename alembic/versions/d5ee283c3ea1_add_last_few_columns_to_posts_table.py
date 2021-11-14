"""add last few columns to posts table

Revision ID: d5ee283c3ea1
Revises: fee43f81250c
Create Date: 2021-11-14 21:12:13.989359

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import TIMESTAMP


# revision identifiers, used by Alembic.
revision = 'd5ee283c3ea1'
down_revision = 'fee43f81250c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text
        ('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
