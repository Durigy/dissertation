"""added module subscriptions

Revision ID: 3b7ba909d2eb
Revises: 5df7b7d8d92b
Create Date: 2023-03-28 13:58:49.724994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b7ba909d2eb'
down_revision = '5df7b7d8d92b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('module_subscription',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('module_id', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('module_subscription')
    # ### end Alembic commands ###
