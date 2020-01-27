"""empty message

Revision ID: 9a12378693d6
Revises: eebcff4e6c33
Create Date: 2020-01-27 20:35:35.945217

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9a12378693d6'
down_revision = 'eebcff4e6c33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('t_lost_found', 'fix_top')
    op.drop_column('t_lost_found', 'record_status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_lost_found', sa.Column('record_status', mysql.INTEGER(display_width=11), server_default=sa.text("'0'"), autoincrement=False, nullable=False))
    op.add_column('t_lost_found', sa.Column('fix_top', mysql.INTEGER(display_width=11), server_default=sa.text("'0'"), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
