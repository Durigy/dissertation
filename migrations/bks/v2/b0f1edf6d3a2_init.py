"""init

Revision ID: b0f1edf6d3a2
Revises: 
Create Date: 2023-03-20 07:51:01.744347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0f1edf6d3a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('university',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('url', sa.String(length=300), nullable=False),
    sa.Column('date_created', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('date_established', sa.Date(), nullable=True),
    sa.Column('first_line', sa.String(length=120), nullable=True),
    sa.Column('second_line', sa.String(length=120), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('country', sa.String(length=100), nullable=True),
    sa.Column('postcode', sa.String(length=20), nullable=True),
    sa.Column('user_count', sa.Integer(), nullable=False),
    sa.Column('avg_rating', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('university_school',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('user_count', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('university_year',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('user_count', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_role',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('date_created', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('user_count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('module',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=240), nullable=False),
    sa.Column('code', sa.String(length=30), nullable=False),
    sa.Column('avg_rating', sa.Float(), nullable=False),
    sa.Column('desctription', sa.Text(), nullable=True),
    sa.Column('tutor', sa.String(length=240), nullable=True),
    sa.Column('date_created', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('university_id', sa.String(length=20), nullable=True),
    sa.Column('university_school_id', sa.String(length=20), nullable=True),
    sa.Column('university_year_id', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['university_id'], ['university.id'], ),
    sa.ForeignKeyConstraint(['university_school_id'], ['university_school.id'], ),
    sa.ForeignKeyConstraint(['university_year_id'], ['university_year.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('username', sa.String(length=120), nullable=False),
    sa.Column('firstname', sa.String(length=120), nullable=True),
    sa.Column('lastname', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('join_date', sa.DateTime(), nullable=True),
    sa.Column('university_id', sa.String(length=20), nullable=True),
    sa.Column('university_year_id', sa.String(length=20), nullable=True),
    sa.Column('university_school_id', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['university_id'], ['university.id'], ),
    sa.ForeignKeyConstraint(['university_school_id'], ['university_school.id'], ),
    sa.ForeignKeyConstraint(['university_year_id'], ['university_year.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('document',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('title', sa.String(length=240), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date_added', sa.Date(), nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('image',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('title', sa.String(length=240), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date_added', sa.Date(), nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message_thread',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=240), nullable=True),
    sa.Column('date_created', sa.Date(), nullable=False),
    sa.Column('date_last_message', sa.Date(), nullable=True),
    sa.Column('member_count', sa.Integer(), nullable=False),
    sa.Column('message_count', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('module_file',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=240), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date_created', sa.Date(), nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('module_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('module_lecture',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('date_sent', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('module_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('module_note',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('date_created', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('title', sa.String(length=240), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('module_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('module_post',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('date_sent', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('module_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('module_review',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('date_sent', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=240), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('module_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('module_subscription',
    sa.Column('id', sa.String(length=12), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.String(length=32), nullable=False),
    sa.Column('module_id', sa.String(length=12), nullable=False),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('public_post',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('date_sent', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('public_profile',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('date_created', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('university_review',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=240), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date_created', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_role_link',
    sa.Column('user', sa.String(length=20), nullable=False),
    sa.Column('user_role', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_role'], ['user_role.id'], )
    )
    op.create_table('user_settings',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('darkmode', sa.Boolean(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_stats',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('posts', sa.Integer(), nullable=False),
    sa.Column('comments', sa.Integer(), nullable=False),
    sa.Column('friends', sa.Integer(), nullable=False),
    sa.Column('reviews', sa.Integer(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_university_link',
    sa.Column('user', sa.String(length=20), nullable=False),
    sa.Column('university', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['university'], ['university.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], )
    )
    op.create_table('message',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('date_sent', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('message_thread_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['message_thread_id'], ['message_thread.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('module_lectue_vote',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('date_sent', sa.Date(), nullable=False),
    sa.Column('vote', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('module_id', sa.String(length=20), nullable=False),
    sa.Column('module_lecture_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['module_lecture_id'], ['module_lecture.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('module_post_comment',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('date_sent', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('module_id', sa.String(length=20), nullable=False),
    sa.Column('module_post_id', sa.String(length=20), nullable=False),
    sa.Column('parent_comment_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['module_post_id'], ['module_post.id'], ),
    sa.ForeignKeyConstraint(['parent_comment_id'], ['module_post_comment.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('public_post_comment',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('date_sent', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('public_post_id', sa.String(length=20), nullable=False),
    sa.Column('parent_comment_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['parent_comment_id'], ['public_post_comment.id'], ),
    sa.ForeignKeyConstraint(['public_post_id'], ['public_post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('public_post_comment')
    op.drop_table('module_post_comment')
    op.drop_table('module_lectue_vote')
    op.drop_table('message')
    op.drop_table('user_university_link')
    op.drop_table('user_stats')
    op.drop_table('user_settings')
    op.drop_table('user_role_link')
    op.drop_table('university_review')
    op.drop_table('public_profile')
    op.drop_table('public_post')
    op.drop_table('module_subscription')
    op.drop_table('module_review')
    op.drop_table('module_post')
    op.drop_table('module_note')
    op.drop_table('module_lecture')
    op.drop_table('module_file')
    op.drop_table('message_thread')
    op.drop_table('image')
    op.drop_table('document')
    op.drop_table('user')
    op.drop_table('module')
    op.drop_table('user_role')
    op.drop_table('university_year')
    op.drop_table('university_school')
    op.drop_table('university')
    # ### end Alembic commands ###
