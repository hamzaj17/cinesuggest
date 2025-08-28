"""add role to users

Revision ID: 216020235fec
Revises: 597d01620d0d
Create Date: 2025-08-29 03:24:04.184828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '216020235fec'
down_revision: Union[str, Sequence[str], None] = '597d01620d0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Step 1: Add column with default="user" (so old rows are backfilled)
    op.add_column('users', sa.Column('role', sa.String(), server_default='user', nullable=False))

    # Step 2 (optional but recommended): drop server_default, so new rows must explicitly set role in app logic
    op.alter_column('users', 'role', server_default=None)

    # Add index
    op.create_index('ix_users_role', 'users', ['role'], unique=False)


def downgrade():
    op.drop_index('ix_users_role', table_name='users')
    op.drop_column('users', 'role')

