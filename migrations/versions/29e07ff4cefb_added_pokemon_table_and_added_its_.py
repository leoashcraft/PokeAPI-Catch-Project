"""Added Pokemon table and added its attribute

Revision ID: 29e07ff4cefb
Revises: 
Create Date: 2021-09-18 08:40:51.891617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29e07ff4cefb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('hp', sa.JSON(), nullable=True),
    sa.Column('attack', sa.JSON(), nullable=True),
    sa.Column('defense', sa.JSON(), nullable=True),
    sa.Column('special_attack', sa.JSON(), nullable=True),
    sa.Column('special_defense', sa.JSON(), nullable=True),
    sa.Column('speed', sa.JSON(), nullable=True),
    sa.Column('spritedata', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=150), nullable=True),
    sa.Column('last_name', sa.String(length=150), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('password', sa.String(length=200), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('userpokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('pokemon_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userpokemon')
    op.drop_table('user')
    op.drop_table('pokemon')
    # ### end Alembic commands ###
