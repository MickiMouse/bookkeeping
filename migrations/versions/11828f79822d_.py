"""empty message

Revision ID: 11828f79822d
Revises: c6e6c7153c74
Create Date: 2019-04-27 19:45:59.169960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11828f79822d'
down_revision = 'c6e6c7153c74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('category', sa.String(length=16), nullable=True))
    op.drop_index('ix_card_kind', table_name='card')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_card_kind', 'card', ['kind'], unique=False)
    op.drop_column('card', 'category')
    # ### end Alembic commands ###
