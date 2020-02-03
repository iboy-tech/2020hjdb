"""增加关联表

Revision ID: fe334b260916
Revises: 7a988f55ee48
Create Date: 2020-02-01 18:28:19.897997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe334b260916'
# down_revision = '7a988f55ee48'
down_revision=None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 't_category', 't_user', ['user_id'], ['id'])
    op.drop_constraint('t_comment_ibfk_1', 't_comment', type_='foreignkey')
    op.drop_constraint('t_comment_ibfk_2', 't_comment', type_='foreignkey')
    op.create_foreign_key(None, 't_comment', 't_user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 't_comment', 't_lost_found', ['lost_found_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('t_lost_found_ibfk_1', 't_lost_found', type_='foreignkey')
    op.drop_constraint('t_lost_found_ibfk_2', 't_lost_found', type_='foreignkey')
    op.create_foreign_key(None, 't_lost_found', 't_category', ['category_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 't_lost_found', type_='foreignkey')
    op.create_foreign_key('t_lost_found_ibfk_2', 't_lost_found', 't_user', ['user_id'], ['id'])
    op.create_foreign_key('t_lost_found_ibfk_1', 't_lost_found', 't_category', ['category_id'], ['id'])
    op.drop_constraint(None, 't_comment', type_='foreignkey')
    op.drop_constraint(None, 't_comment', type_='foreignkey')
    op.create_foreign_key('t_comment_ibfk_2', 't_comment', 't_user', ['user_id'], ['id'])
    op.create_foreign_key('t_comment_ibfk_1', 't_comment', 't_lost_found', ['lost_found_id'], ['id'])
    op.drop_constraint(None, 't_category', type_='foreignkey')
    # ### end Alembic commands ###
