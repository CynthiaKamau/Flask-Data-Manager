"""Renaming user table to users

Revision ID: ef69c51a7735
Revises: dc42eb980277
Create Date: 2019-11-07 12:16:46.001039

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ef69c51a7735'
down_revision = 'dc42eb980277'
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
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_table('user')
    op.drop_constraint(u'followers_follower_id_fkey', 'followers', type_='foreignkey')
    op.drop_constraint(u'followers_followed_id_fkey', 'followers', type_='foreignkey')
    op.create_foreign_key(None, 'followers', 'users', ['follower_id'], ['id'])
    op.create_foreign_key(None, 'followers', 'users', ['followed_id'], ['id'])
    op.drop_constraint(u'sample_user_id_fkey', 'sample', type_='foreignkey')
    op.create_foreign_key(None, 'sample', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sample', type_='foreignkey')
    op.create_foreign_key(u'sample_user_id_fkey', 'sample', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'followers', type_='foreignkey')
    op.drop_constraint(None, 'followers', type_='foreignkey')
    op.create_foreign_key(u'followers_followed_id_fkey', 'followers', 'user', ['followed_id'], ['id'])
    op.create_foreign_key(u'followers_follower_id_fkey', 'followers', 'user', ['follower_id'], ['id'])
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
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###