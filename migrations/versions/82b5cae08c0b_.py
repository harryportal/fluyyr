"""empty message

Revision ID: 82b5cae08c0b
Revises: 79e674eb3fae
Create Date: 2022-05-25 08:49:28.907793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82b5cae08c0b'
down_revision = '79e674eb3fae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###