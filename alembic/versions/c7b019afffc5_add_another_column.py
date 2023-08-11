"""add another column

Revision ID: c7b019afffc5
Revises: dfa3cfbcfc3c
Create Date: 2023-08-11 16:16:13.569228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7b019afffc5'
down_revision: Union[str, None] = 'dfa3cfbcfc3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
