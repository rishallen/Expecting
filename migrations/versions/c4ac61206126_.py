"""empty message

Revision ID: c4ac61206126
Revises: 9c2d4135e8a6
Create Date: 2021-07-24 14:50:39.899170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4ac61206126'
down_revision = '9c2d4135e8a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'post', 'user', ['user_id'], ['user_id'])
    op.drop_column('post', 'like_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('like_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'user_id')
    # ### end Alembic commands ###
