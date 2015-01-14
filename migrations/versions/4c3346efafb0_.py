"""empty message

Revision ID: 4c3346efafb0
Revises: 1afc5bc6003
Create Date: 2015-01-13 16:38:44.014196

"""

# revision identifiers, used by Alembic.
revision = '4c3346efafb0'
down_revision = '1afc5bc6003'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('knowledge_area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('definition', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.add_column(u'university', sa.Column('established', sa.Integer(), nullable=True))
    op.add_column(u'university', sa.Column('motto', sa.Text(), nullable=True))
    op.add_column(u'university', sa.Column('principal', sa.String(length=200), nullable=True))
    op.add_column(u'university', sa.Column('students', sa.Integer(), nullable=True))
    op.add_column(u'university', sa.Column('type', sa.String(length=100), nullable=True))
    op.add_column(u'university', sa.Column('web_site', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'university', 'web_site')
    op.drop_column(u'university', 'type')
    op.drop_column(u'university', 'students')
    op.drop_column(u'university', 'principal')
    op.drop_column(u'university', 'motto')
    op.drop_column(u'university', 'established')
    op.drop_table('knowledge_area')
    ### end Alembic commands ###