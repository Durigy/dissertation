"""module resource

Revision ID: 2f68320382e0
Revises: 72011fcc4273
Create Date: 2023-04-11 04:40:50.458330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f68320382e0'
down_revision = '72011fcc4273'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('module_resource',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('module_id', sa.String(length=20), nullable=False),
    sa.Column('image_id', sa.String(length=20), nullable=True),
    sa.Column('document_id', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['document.id'], ),
    sa.ForeignKeyConstraint(['image_id'], ['image.id'], ),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('module_resource')
    # ### end Alembic commands ###
