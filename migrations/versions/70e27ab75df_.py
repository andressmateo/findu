"""empty message

Revision ID: 70e27ab75df
Revises: 230143355e07
Create Date: 2015-03-31 16:29:00.168876

"""

# revision identifiers, used by Alembic.
revision = '70e27ab75df'
down_revision = '230143355e07'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('career_at_headquarter',
    sa.Column('id_cat_university', sa.Integer(), nullable=True),
    sa.Column('id_university_headquarter', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_cat_university'], ['career_at_university.id'], ),
    sa.ForeignKeyConstraint(['id_university_headquarter'], ['universityheadquarter.id'], )
    )
    op.drop_table('team')
    op.add_column('career_at_university', sa.Column('university_id', sa.Integer(), nullable=True))
    op.drop_constraint(u'career_at_university_place_id_fkey', 'career_at_university', type_='foreignkey')
    op.create_foreign_key(None, 'career_at_university', 'university', ['university_id'], ['id'])
    op.drop_column('career_at_university', 'place_id')
    op.create_unique_constraint(None, 'image_campus', ['src'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'image_campus', type_='unique')
    op.add_column('career_at_university', sa.Column('place_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'career_at_university', type_='foreignkey')
    op.create_foreign_key(u'career_at_university_place_id_fkey', 'career_at_university', 'universityheadquarter', ['place_id'], ['id'])
    op.drop_column('career_at_university', 'university_id')
    op.create_table('team',
    sa.Column('username', sa.VARCHAR(length=140), autoincrement=False, nullable=False),
    sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('level', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('username', name=u'team_pkey')
    )
    op.drop_table('career_at_headquarter')
    ### end Alembic commands ###
