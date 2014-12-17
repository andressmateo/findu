"""empty message

Revision ID: 1b8ff49dc4e7
Revises: 27e873377fec
Create Date: 2014-12-17 03:16:08.914742

"""

# revision identifiers, used by Alembic.
revision = '1b8ff49dc4e7'
down_revision = '27e873377fec'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'career', ['id'])
    op.create_unique_constraint(None, 'career_at_university', ['id'])
    op.create_unique_constraint(None, 'other_name', ['name'])
    op.create_unique_constraint(None, 'university', ['id'])
    op.add_column('universityheadquarter', sa.Column('campus_name', sa.String(length=200), nullable=True))
    op.create_unique_constraint(None, 'universityheadquarter', ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'universityheadquarter', type_='unique')
    op.drop_column('universityheadquarter', 'campus_name')
    op.drop_constraint(None, 'university', type_='unique')
    op.drop_constraint(None, 'other_name', type_='unique')
    op.drop_constraint(None, 'career_at_university', type_='unique')
    op.drop_constraint(None, 'career', type_='unique')
    ### end Alembic commands ###