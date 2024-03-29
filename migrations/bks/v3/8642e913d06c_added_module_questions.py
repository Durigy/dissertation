"""added module questions

Revision ID: 8642e913d06c
Revises: 3b7ba909d2eb
Create Date: 2023-03-29 09:09:47.691236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8642e913d06c'
down_revision = '3b7ba909d2eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('module_question',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('date_sent', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('title', sa.String(length=240), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('solved', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('module_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('module_question_comment',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('date_sent', sa.Date(), nullable=False),
    sa.Column('date_edited', sa.Date(), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('module_id', sa.String(length=20), nullable=False),
    sa.Column('module_question_id', sa.String(length=20), nullable=False),
    sa.Column('parent_comment_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['module_question_id'], ['module_question.id'], ),
    sa.ForeignKeyConstraint(['parent_comment_id'], ['module_question_comment.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('module_question_comment')
    op.drop_table('module_question')
    # ### end Alembic commands ###
