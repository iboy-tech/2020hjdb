"""empty message

Revision ID: fa22f28f3f3f
Revises: 0599fa3f1b7a
Create Date: 2020-02-03 22:34:04.257971

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fa22f28f3f3f'
down_revision = '0599fa3f1b7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('t_user', 'kind',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True,
               existing_server_default=sa.text("'1'"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('t_user', 'kind',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False,
               existing_server_default=sa.text("'1'"))
    # ### end Alembic commands ###
