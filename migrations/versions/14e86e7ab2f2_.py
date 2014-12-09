"""empty message

Revision ID: 14e86e7ab2f2
Revises: None
Create Date: 2014-12-07 05:53:17.686683

"""

# revision identifiers, used by Alembic.
revision = '14e86e7ab2f2'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('team', sa.Column('level', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'team', ['username'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'team', type_='unique')
    op.drop_column('team', 'level')
    ### end Alembic commands ###