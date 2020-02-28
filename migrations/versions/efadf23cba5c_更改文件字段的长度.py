"""更改文件字段的长度

Revision ID: efadf23cba5c
Revises: e65a29be53cc
Create Date: 2020-02-28 13:38:06.479632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efadf23cba5c'
down_revision = 'e65a29be53cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_report', sa.Column('file_name', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('t_report', 'file_name')
    # ### end Alembic commands ###
