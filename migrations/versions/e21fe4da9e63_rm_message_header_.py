"""Rm Message.header_*

Revision ID: e21fe4da9e63
Revises: 03776c9f130e
Create Date: 2019-04-04 14:38:50.509730

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e21fe4da9e63'
down_revision = '03776c9f130e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'raw_headers')
    op.drop_column('message', 'headers_raw')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('headers_raw', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('message', sa.Column('raw_headers', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
