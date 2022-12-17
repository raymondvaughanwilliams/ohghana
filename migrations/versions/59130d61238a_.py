"""empty message

Revision ID: 59130d61238a
Revises: 2c6c7b5b096b
Create Date: 2022-06-29 22:43:39.050474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59130d61238a'
down_revision = '2c6c7b5b096b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web_feature', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('type', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('web_feature', schema=None) as batch_op:
        batch_op.drop_column('type')
        batch_op.drop_column('price')

    # ### end Alembic commands ###
