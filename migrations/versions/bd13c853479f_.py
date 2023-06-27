"""empty message

Revision ID: bd13c853479f
Revises: a87dc7ea14cf
Create Date: 2023-05-25 14:53:12.897477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd13c853479f'
down_revision = 'a87dc7ea14cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ecom_request', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sms_attempts', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ecom_request', schema=None) as batch_op:
        batch_op.drop_column('sms_attempts')

    # ### end Alembic commands ###
