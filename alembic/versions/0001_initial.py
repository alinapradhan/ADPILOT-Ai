"""initial schema"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "organizations",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
    )
    op.create_table(
        "clients",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("organization_id", sa.String(length=64), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
    )
    op.create_table(
        "advertising_accounts",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("client_id", sa.String(length=64), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("connector", sa.String(length=64), nullable=False),
        sa.Column("external_account_id", sa.String(length=255), nullable=False),
    )
    op.create_table(
        "analysis_runs",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("client_id", sa.String(length=64), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("account_id", sa.String(length=64), sa.ForeignKey("advertising_accounts.id"), nullable=False),
        sa.Column("analysis_type", sa.String(length=64), nullable=False),
        sa.Column("model_version", sa.String(length=64), nullable=True),
        sa.Column("prompt_version", sa.String(length=64), nullable=True),
        sa.Column("input_payload", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "findings",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("run_id", sa.String(length=64), sa.ForeignKey("analysis_runs.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("fact", sa.Text(), nullable=False),
        sa.Column("hypothesis", sa.Text(), nullable=True),
        sa.Column("severity", sa.String(length=16), nullable=False),
    )
    op.create_table(
        "user_preferences",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("key", sa.String(length=128), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
    )
    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("actor_id", sa.String(length=64), nullable=False),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column("details", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("audit_events")
    op.drop_table("user_preferences")
    op.drop_table("findings")
    op.drop_table("analysis_runs")
    op.drop_table("advertising_accounts")
    op.drop_table("clients")
    op.drop_table("organizations")
