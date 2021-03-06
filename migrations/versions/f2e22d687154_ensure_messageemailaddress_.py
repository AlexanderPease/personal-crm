"""Ensure MessageEmailAddress relationships are ForeignKeys

Revision ID: f2e22d687154
Revises: 48c22ef3a4da
Create Date: 2019-04-02 14:11:34.227546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2e22d687154'
down_revision = '48c22ef3a4da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'message_email_address', 'message', ['message_id'], ['id'])
    op.create_foreign_key(None, 'message_email_address', 'email_address', ['email_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'message_email_address', type_='foreignkey')
    op.drop_constraint(None, 'message_email_address', type_='foreignkey')
    # ### end Alembic commands ###
