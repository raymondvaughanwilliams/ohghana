"""empty message

Revision ID: 7afe89c7c875
Revises: 850de668e557
Create Date: 2022-07-24 23:13:01.376742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7afe89c7c875'
down_revision = '850de668e557'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('fk_users_rec_payment_id_payments', type_='foreignkey')
        batch_op.drop_column('rec_payment_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rec_payment_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_users_rec_payment_id_payments', 'payments', ['rec_payment_id'], ['id'])

    # ### end Alembic commands ###
