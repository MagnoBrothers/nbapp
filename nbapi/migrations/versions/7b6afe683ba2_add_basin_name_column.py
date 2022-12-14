""""Add basin name column"

Revision ID: 7b6afe683ba2
Revises: 8de398c33927
Create Date: 2022-11-20 18:17:55.796174

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "7b6afe683ba2"
down_revision = "8de398c33927"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "basin", sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False)
    )


def downgrade():
    op.drop_column("basin", "name")
