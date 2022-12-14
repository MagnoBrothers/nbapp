""""Add basin url column"

Revision ID: 4ed8489f1004
Revises: b49c6ff0e97d
Create Date: 2022-11-12 04:12:45.035407

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "4ed8489f1004"
down_revision = "b49c6ff0e97d"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "basin", sa.Column("url", sqlmodel.sql.sqltypes.AutoString(), nullable=True)
    )


def downgrade():
    op.drop_column("basin", "url")
