"""lectures

Revision ID: eceefeaa6fcd
Revises: 1ebca7012e4a
Create Date: 2023-05-05 21:54:55.988908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eceefeaa6fcd'
down_revision = '1ebca7012e4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('module_lecture',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=False),
    sa.Column('date_start', sa.DateTime(), nullable=False),
    sa.Column('date_end', sa.DateTime(), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('online_link', sa.String(length=300), nullable=True),
    sa.Column('quizing_link', sa.String(length=300), nullable=True),
    sa.Column('module_id', sa.String(length=20), nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('module_lecture')
    # ### end Alembic commands ###
