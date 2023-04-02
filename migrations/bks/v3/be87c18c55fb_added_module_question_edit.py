"""added module question edit

Revision ID: be87c18c55fb
Revises: 8642e913d06c
Create Date: 2023-03-31 09:03:53.831518

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'be87c18c55fb'
down_revision = '8642e913d06c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('module_question_edit',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('module_question_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['module_question_id'], ['module_question.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('module_question', sa.Column('date', sa.Date(), nullable=False))
    op.add_column('module_question', sa.Column('comment_count', sa.Integer(), nullable=True))
    op.add_column('module_question', sa.Column('view_count', sa.Integer(), nullable=True))
    op.add_column('module_question', sa.Column('unique_view_count', sa.Integer(), nullable=True))
    op.alter_column('module_question', 'title',
               existing_type=mysql.VARCHAR(length=240),
               nullable=False)
    op.drop_column('module_question', 'date_sent')
    op.add_column('module_question_comment', sa.Column('sub_comment_count', sa.Integer(), nullable=True))
    op.drop_constraint('module_question_comment_ibfk_1', 'module_question_comment', type_='foreignkey')
    op.drop_column('module_question_comment', 'module_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('module_question_comment', sa.Column('module_id', mysql.VARCHAR(length=20), nullable=False))
    op.create_foreign_key('module_question_comment_ibfk_1', 'module_question_comment', 'module', ['module_id'], ['id'])
    op.drop_column('module_question_comment', 'sub_comment_count')
    op.add_column('module_question', sa.Column('date_sent', sa.DATE(), nullable=False))
    op.alter_column('module_question', 'title',
               existing_type=mysql.VARCHAR(length=240),
               nullable=True)
    op.drop_column('module_question', 'unique_view_count')
    op.drop_column('module_question', 'view_count')
    op.drop_column('module_question', 'comment_count')
    op.drop_column('module_question', 'date')
    op.drop_table('module_question_edit')
    # ### end Alembic commands ###
