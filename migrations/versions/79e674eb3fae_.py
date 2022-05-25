"""empty message

Revision ID: 79e674eb3fae
Revises: dfae521dd92a
Create Date: 2022-05-24 12:19:24.419979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79e674eb3fae'
down_revision = 'dfae521dd92a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('artist_image_link', sa.String(length=250), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Shows', 'artist_image_link')
    # ### end Alembic commands ###
