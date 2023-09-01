"""empty message

Revision ID: 075cdf45f438
Revises: 9e88f8b3cbe0
Create Date: 2023-08-30 01:58:06.448652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '075cdf45f438'
down_revision = '9e88f8b3cbe0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('confirmed_on', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('registered_on', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'registered_on')
    op.drop_column('users', 'confirmed_on')
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###