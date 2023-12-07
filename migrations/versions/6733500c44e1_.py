"""empty message

Revision ID: 6733500c44e1
Revises: 687c54d50291
Create Date: 2023-11-11 19:33:10.527080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6733500c44e1'
down_revision = '687c54d50291'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('polls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_polls'))
    )
    op.create_table('polloptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('poll_id', sa.Integer(), nullable=True),
    sa.Column('option_text', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['poll_id'], ['polls.id'], name=op.f('fk_polloptions_poll_id_polls')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_polloptions'))
    )
    op.create_table('pollvotes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('poll_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('option_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['option_id'], ['polloptions.id'], name=op.f('fk_pollvotes_option_id_polloptions')),
    sa.ForeignKeyConstraint(['poll_id'], ['polls.id'], name=op.f('fk_pollvotes_poll_id_polls')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_pollvotes_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_pollvotes'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pollvotes')
    op.drop_table('polloptions')
    op.drop_table('polls')
    # ### end Alembic commands ###
