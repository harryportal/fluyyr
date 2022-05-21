"""empty message

Revision ID: 82c8944ecfe1
Revises: 77ae204397a6
Create Date: 2022-05-21 19:04:56.321730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82c8944ecfe1'
down_revision = '77ae204397a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('looking_for_talent', sa.Boolean(), nullable=True))
    op.drop_column('Venue', 'looking_for_venues')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('looking_for_venues', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'looking_for_talent')
    # ### end Alembic commands ###