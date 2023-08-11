"""renaming posts user_id colum to owner_id

Revision ID: ccff8b996e3e
Revises: f13b8d821697
Create Date: 2023-08-11 16:45:24.557686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccff8b996e3e'
down_revision: Union[str, None] = 'f13b8d821697'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename the column "user_id" to "owner_id"
    op.alter_column("posts", "user_id", new_column_name="owner_id")
    
    # Update the foreign key constraint name
    op.drop_constraint("posts_users_fkey", "posts")
    op.create_foreign_key("posts_owner_fkey", source_table="posts", referent_table="users",
                          local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass

def downgrade() -> None:
    # Drop the updated foreign key constraint
    op.drop_constraint("posts_owner_fkey", "posts")
    
    # Rename the column "owner_id" back to "user_id"
    op.alter_column("posts", "owner_id", new_column_name="user_id")
    op.create_foreign_key("posts_users_fkey", source_table="posts", referent_table="users",
                        local_cols= ["user_id"], remote_cols= ["id"], ondelete="CASCADE")
    pass