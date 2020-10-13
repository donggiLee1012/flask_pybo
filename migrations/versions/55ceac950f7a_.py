"""empty message

Revision ID: 55ceac950f7a
Revises: 49045af9a3b9
Create Date: 2020-10-13 16:41:32.706740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55ceac950f7a'
down_revision = '49045af9a3b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hashtag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('keyword', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_hashtag')),
    sa.UniqueConstraint('keyword', name=op.f('uq_hashtag_keyword'))
    )
    op.create_table('shoes_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=30), nullable=True),
    sa.Column('img', sa.Text(), nullable=True),
    sa.Column('brand', sa.String(length=30), nullable=False),
    sa.Column('retail_price', sa.Integer(), nullable=True),
    sa.Column('release_date', sa.DateTime(), nullable=True),
    sa.Column('colorway', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_shoes_model')),
    sa.UniqueConstraint('code', name=op.f('uq_shoes_model_code'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shoes_model')
    op.drop_table('hashtag')
    # ### end Alembic commands ###
