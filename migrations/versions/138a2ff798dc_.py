"""Add Message.raw_headers

Revision ID: 138a2ff798dc
Revises: ea9cc8b79dab
Create Date: 2019-04-01 23:53:41.960786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '138a2ff798dc'
down_revision = 'ea9cc8b79dab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('raw_headers', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'raw_headers')
    # ### end Alembic commands ###