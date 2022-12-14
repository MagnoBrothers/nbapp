""""Add job date"

Revision ID: e6e5d64a564b
Revises: 7b6afe683ba2
Create Date: 2022-12-12 14:44:12.899318

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "e6e5d64a564b"
down_revision = "7b6afe683ba2"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("job", sa.Column("date", sa.DateTime(), nullable=False))


def downgrade():
    op.drop_column("job", "date")
