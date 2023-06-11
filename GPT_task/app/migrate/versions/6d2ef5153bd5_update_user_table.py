"""update user table

Revision ID: 6d2ef5153bd5
Revises: e662ab8c6463
Create Date: 2023-06-11 10:38:19.747741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d2ef5153bd5'
down_revision = 'e662ab8c6463'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(), nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'is_superuser')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'password')
    # ### end Alembic commands ###