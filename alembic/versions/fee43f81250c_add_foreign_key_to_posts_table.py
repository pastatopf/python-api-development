"""add foreign-key to posts table

Revision ID: fee43f81250c
Revises: 0564cb9914c2
Create Date: 2021-11-14 21:05:02.100737

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import table


# revision identifiers, used by Alembic.
revision = 'fee43f81250c'
down_revision = '0564cb9914c2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
