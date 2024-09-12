"""add_username

Revision ID: 009138e5f0a5
Revises: a94f35adf1a7
Create Date: 2024-08-31 13:24:48.187439

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "009138e5f0a5"
down_revision: Union[str, None] = "a94f35adf1a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("username", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "username")
    # ### end Alembic commands ###