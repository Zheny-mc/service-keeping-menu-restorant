"""New Migration

Revision ID: f4b12cb14097
Revises: 6ce7505de8c9
Create Date: 2024-01-24 08:46:56.494712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4b12cb14097'
down_revision: Union[str, None] = '6ce7505de8c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('submenus_menu_id_key', 'submenus', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('submenus_menu_id_key', 'submenus', ['menu_id'])
    # ### end Alembic commands ###