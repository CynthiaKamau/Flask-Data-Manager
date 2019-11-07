"""Renaming user table

Revision ID: 364679dcc955
Revises: 66e4ac9eb9c7
Create Date: 2019-11-07 12:34:14.034452

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '364679dcc955'
down_revision = '66e4ac9eb9c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], )
    )
    op.create_table('sample',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=64), nullable=True),
    sa.Column('species', sa.String(length=165), nullable=True),
    sa.Column('location_collected', sa.String(length=165), nullable=True),
    sa.Column('project', sa.String(length=165), nullable=True),
    sa.Column('owner', sa.String(length=150), nullable=True),
    sa.Column('retension_period', sa.Integer(), nullable=True),
    sa.Column('barcode', sa.String(length=165), nullable=True),
    sa.Column('analysis', sa.String(length=165), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sample_timestamp'), 'sample', ['timestamp'], unique=False)
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('about_me', sa.VARCHAR(length=140), autoincrement=False, nullable=True),
    sa.Column('last_seen', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'user_pkey')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=True)
    op.create_index('ix_user_email', 'user', ['email'], unique=True)
    op.drop_index(op.f('ix_sample_timestamp'), table_name='sample')
    op.drop_table('sample')
    op.drop_table('followers')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
