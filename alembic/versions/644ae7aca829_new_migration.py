"""New Migration

Revision ID: 644ae7aca829
Revises: f4b12cb14097
Create Date: 2024-01-24 09:10:25.542885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '644ae7aca829'
down_revision: Union[str, None] = 'f4b12cb14097'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('dishs_submenu_id_key', 'dishs', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('dishs_submenu_id_key', 'dishs', ['submenu_id'])
    # ### end Alembic commands ###