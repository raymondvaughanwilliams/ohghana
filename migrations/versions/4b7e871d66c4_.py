"""empty message

Revision ID: 4b7e871d66c4
Revises: f8dab61ccd04
Create Date: 2023-08-21 08:02:12.814161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b7e871d66c4'
down_revision = 'f8dab61ccd04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('farmers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('premium_amount', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('cashcode', sa.String(length=255), nullable=True),
    sa.Column('date_added', sa.Date(), nullable=True),
    sa.Column('last_modified', sa.Date(), nullable=True),
    sa.Column('language', sa.String(length=255), nullable=True),
    sa.Column('society', sa.String(length=255), nullable=True),
    sa.Column('farmercode', sa.String(length=255), nullable=True),
    sa.Column('cooperative', sa.String(length=255), nullable=True),
    sa.Column('ordernumber', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_farmers'))
    )
    op.create_table('subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_subjects'))
    )
    op.create_table('ecom_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('cashcode', sa.String(), nullable=True),
    sa.Column('farmer_id', sa.Integer(), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('disposition', sa.String(), nullable=True),
    sa.Column('sms_disposition', sa.String(), nullable=True),
    sa.Column('sms_attempts', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['farmer_id'], ['farmers.id'], name=op.f('fk_ecom_request_farmer_id_farmers')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_ecom_request'))
    )
    op.create_table('partrequests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=512), nullable=False),
    sa.Column('model_year', sa.Integer(), nullable=False),
    sa.Column('car_make', sa.String(length=128), nullable=False),
    sa.Column('car_model', sa.String(length=128), nullable=False),
    sa.Column('note', sa.String(length=128), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=16), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_partrequests_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_partrequests'))
    )
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(length=255), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('vendor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_review_user_id_users')),
    sa.ForeignKeyConstraint(['vendor_id'], ['users.id'], name=op.f('fk_review_vendor_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_review'))
    )
    op.create_table('siprequests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channels', sa.String(length=128), nullable=True),
    sa.Column('other', sa.String(length=512), nullable=True),
    sa.Column('codecs', sa.Integer(), nullable=True),
    sa.Column('inbound', sa.String(length=128), nullable=True),
    sa.Column('outbound', sa.String(length=128), nullable=True),
    sa.Column('provider', sa.String(length=128), nullable=True),
    sa.Column('certificate', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=16), nullable=False),
    sa.Column('email', sa.String(length=106), nullable=True),
    sa.Column('name', sa.String(length=106), nullable=True),
    sa.Column('customer_id', sa.String(length=106), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_siprequests_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_siprequests'))
    )
    op.create_table('student_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('year', sa.String(length=128), nullable=True),
    sa.Column('result', sa.Integer(), nullable=False),
    sa.Column('index_number', sa.String(length=128), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], name=op.f('fk_student_results_student_id_users')),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], name=op.f('fk_student_results_subject_id_subjects')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_student_results'))
    )
    op.create_table('bids',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('part_id', sa.Integer(), nullable=False),
    sa.Column('vendor_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=16), nullable=False),
    sa.Column('delivery', sa.String(length=16), nullable=True),
    sa.Column('note', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['part_id'], ['partrequests.id'], name=op.f('fk_bids_part_id_partrequests')),
    sa.ForeignKeyConstraint(['vendor_id'], ['users.id'], name=op.f('fk_bids_vendor_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_bids'))
    )
    op.drop_table('faq')
    op.drop_table('price')
    op.drop_table('testimonial')
    op.drop_table('web_feature')
    op.drop_table('teams')
    with op.batch_alter_table('about', schema=None) as batch_op:
        batch_op.alter_column('atext',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.drop_column('text')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('number', sa.String(length=128), nullable=True))
        batch_op.add_column(sa.Column('location', sa.String(length=128), nullable=True))
        batch_op.add_column(sa.Column('role', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('phone_number', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('biography', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('status', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('index_number', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('completed_year', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('completed_year')
        batch_op.drop_column('index_number')
        batch_op.drop_column('status')
        batch_op.drop_column('biography')
        batch_op.drop_column('phone_number')
        batch_op.drop_column('role')
        batch_op.drop_column('location')
        batch_op.drop_column('number')
        batch_op.drop_column('last_name')
        batch_op.drop_column('name')

    with op.batch_alter_table('about', schema=None) as batch_op:
        batch_op.add_column(sa.Column('text', sa.TEXT(), nullable=False))
        batch_op.alter_column('atext',
               existing_type=sa.TEXT(),
               nullable=False)

    op.create_table('teams',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('position', sa.VARCHAR(), nullable=True),
    sa.Column('faceboook', sa.VARCHAR(length=140), nullable=True),
    sa.Column('instagram', sa.INTEGER(), nullable=True),
    sa.Column('twitter', sa.INTEGER(), nullable=True),
    sa.Column('picture', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_teams')
    )
    op.create_table('web_feature',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('date', sa.DATETIME(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=140), nullable=False),
    sa.Column('text', sa.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_web_feature')
    )
    op.create_table('testimonial',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('company', sa.VARCHAR(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('text', sa.VARCHAR(length=140), nullable=True),
    sa.Column('rating', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_testimonial')
    )
    op.create_table('price',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=140), nullable=False),
    sa.Column('amount', sa.TEXT(), nullable=False),
    sa.Column('features', sa.TEXT(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_price')
    )
    op.create_table('faq',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('question', sa.VARCHAR(length=140), nullable=False),
    sa.Column('answer', sa.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_faq')
    )
    op.drop_table('bids')
    op.drop_table('student_results')
    op.drop_table('siprequests')
    op.drop_table('review')
    op.drop_table('partrequests')
    op.drop_table('ecom_request')
    op.drop_table('subjects')
    op.drop_table('farmers')
    # ### end Alembic commands ###
