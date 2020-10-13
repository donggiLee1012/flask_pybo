"""empty message

Revision ID: 459849e1abd4
Revises: 55ceac950f7a
Create Date: 2020-10-13 16:48:27.204668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '459849e1abd4'
down_revision = '55ceac950f7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shoesmodel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=30), nullable=True),
    sa.Column('img', sa.Text(), nullable=True),
    sa.Column('brand', sa.String(length=30), nullable=False),
    sa.Column('retail_price', sa.Integer(), nullable=True),
    sa.Column('release_date', sa.DateTime(), nullable=True),
    sa.Column('colorway', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_shoesmodel')),
    sa.UniqueConstraint('code', name=op.f('uq_shoesmodel_code'))
    )
    op.drop_table('shoes_model')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shoes_model',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('code', sa.VARCHAR(length=30), nullable=True),
    sa.Column('img', sa.TEXT(), nullable=True),
    sa.Column('brand', sa.VARCHAR(length=30), nullable=False),
    sa.Column('retail_price', sa.INTEGER(), nullable=True),
    sa.Column('release_date', sa.DATETIME(), nullable=True),
    sa.Column('colorway', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_shoes_model'),
    sa.UniqueConstraint('code', name='uq_shoes_model_code')
    )
    op.drop_table('shoesmodel')
    # ### end Alembic commands ###