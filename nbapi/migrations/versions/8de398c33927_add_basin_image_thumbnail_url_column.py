""""Add basin image/thumbnail url column"

Revision ID: 8de398c33927
Revises: 4ed8489f1004
Create Date: 2022-11-18 15:18:26.831413

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "8de398c33927"
down_revision = "4ed8489f1004"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "basin",
        sa.Column("image_url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.add_column(
        "basin",
        sa.Column("thumbnail_url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.drop_column("basin", "url")


def downgrade():
    op.add_column(
        "basin", sa.Column("url", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.drop_column("basin", "thumbnail_url")
    op.drop_column("basin", "image_url")
