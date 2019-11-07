"""Renaming type column to types

Revision ID: 33f743bdcfb6
Revises: 364679dcc955
Create Date: 2019-11-07 13:04:49.248391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33f743bdcfb6'
down_revision = '364679dcc955'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sample', sa.Column('types', sa.String(length=64), nullable=True))
    op.drop_column('sample', 'type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sample', sa.Column('type', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.drop_column('sample', 'types')
    # ### end Alembic commands ###
