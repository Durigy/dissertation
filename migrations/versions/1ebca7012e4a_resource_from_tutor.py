"""resource from tutor

Revision ID: 1ebca7012e4a
Revises: 8d441fbe1175
Create Date: 2023-04-27 13:53:50.451484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ebca7012e4a'
down_revision = '8d441fbe1175'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('module_resource', sa.Column('is_tutor_resource', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('module_resource', 'is_tutor_resource')
    # ### end Alembic commands ###