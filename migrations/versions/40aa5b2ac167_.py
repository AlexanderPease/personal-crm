"""empty message

Revision ID: 40aa5b2ac167
Revises: 59efc69f6999
Create Date: 2019-04-20 00:24:53.768533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40aa5b2ac167'
down_revision = '59efc69f6999'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('subject', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'subject')
    # ### end Alembic commands ###
