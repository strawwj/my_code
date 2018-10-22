"""empty message

Revision ID: 3b5d23637b30
Revises: 68352e7264a5
Create Date: 2018-10-16 20:30:45.329035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b5d23637b30'
down_revision = '68352e7264a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alerts', sa.Column('data_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'alerts', 'datas', ['data_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'alerts', type_='foreignkey')
    op.drop_column('alerts', 'data_id')
    # ### end Alembic commands ###
