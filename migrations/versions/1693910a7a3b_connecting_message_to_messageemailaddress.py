"""Connecting Message headers to MessageEmailAddress

Revision ID: 1693910a7a3b
Revises: 138a2ff798dc
Create Date: 2019-04-02 13:48:45.042670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1693910a7a3b'
down_revision = '138a2ff798dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'email_address', ['email_address'])
    op.add_column('message', sa.Column('header_from_id', sa.Integer(), nullable=True))
    op.add_column('message', sa.Column('header_to_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'message', 'message_email_address', ['header_to_id'], ['id'])
    op.create_foreign_key(None, 'message', 'message_email_address', ['header_from_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.drop_column('message', 'header_to_id')
    op.drop_column('message', 'header_from_id')
    op.drop_constraint(None, 'email_address', type_='unique')
    # ### end Alembic commands ###
