"""empty message

Revision ID: fc4e6711385d
Revises: 820b14818c99
Create Date: 2020-10-07 16:21:19.661459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc4e6711385d'
down_revision = '820b14818c99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shoes', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shoes', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)

    # ### end Alembic commands ###
