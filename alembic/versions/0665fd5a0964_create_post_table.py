"""create post table

Revision ID: 0665fd5a0964
Revises: 
Create Date: 2021-11-14 20:34:32.268557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0665fd5a0964'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass