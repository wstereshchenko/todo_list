"""users table

Revision ID: a25e755946f9
Revises: e9649da8aaa6
Create Date: 2019-01-11 12:41:38.771037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a25e755946f9'
down_revision = 'e9649da8aaa6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('head', sa.String(length=50), nullable=True))
    op.drop_column('post', 'head_post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('head_post', sa.VARCHAR(length=50), nullable=True))
    op.drop_column('post', 'head')
    # ### end Alembic commands ###
