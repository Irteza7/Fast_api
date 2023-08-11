"""add foriegn key to post table

Revision ID: 1f1aee8fa7ae
Revises: 88d58e31ea0d
Create Date: 2023-08-11 16:31:11.407839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f1aee8fa7ae'
down_revision: Union[str, None] = '88d58e31ea0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer, nullable=False))
    op.create_foreign_key("posts_users_fkey", source_table="posts", referent_table="users",
                          local_cols= ["user_id"], remote_cols= ["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fkey","posts")
    op.drop_column("posts", "user_id")
    pass
