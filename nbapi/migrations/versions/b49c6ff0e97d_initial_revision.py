""""Initial revision"

Revision ID: b49c6ff0e97d
Revises: 
Create Date: 2022-11-04 19:40:17.028416

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "b49c6ff0e97d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "basin",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False, primary_key=True),
        sa.Column("imw", sa.Integer(), nullable=False),
        sa.Column("imh", sa.Integer(), nullable=False),
        sa.Column("coefs", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("crmin", sa.Float(), nullable=False),
        sa.Column("crmax", sa.Float(), nullable=False),
        sa.Column("cimin", sa.Float(), nullable=False),
        sa.Column("cimax", sa.Float(), nullable=False),
        sa.Column("itmax", sa.Integer(), nullable=False),
        sa.Column("tol", sa.Float(), nullable=False),
    )
    op.create_index(op.f("ix_basin_id"), "basin", ["id"], unique=True)
    op.create_table(
        "job",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False, primary_key=True),
        sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("progress", sa.Integer(), nullable=False),
        sa.Column("basin_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.ForeignKeyConstraint(["basin_id"], ["basin.id"]),
    )
    op.create_index(op.f("ix_job_id"), "job", ["id"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_job_id"), table_name="job")
    op.drop_table("job")
    op.drop_index(op.f("ix_basin_id"), table_name="basin")
    op.drop_table("basin")
