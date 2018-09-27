"""empty message

Revision ID: 2843257e6b5b
Revises: 
Create Date: 2018-09-22 19:43:21.888468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2843257e6b5b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('db.Integer,default=1', sa.NullType(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students', 'db.Integer,default=1')
    # ### end Alembic commands ###
