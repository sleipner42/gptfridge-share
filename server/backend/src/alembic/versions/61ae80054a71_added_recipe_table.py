"""Added recipe table

Revision ID: 61ae80054a71
Revises: 7e40ff74f735
Create Date: 2024-01-15 20:12:11.220301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "61ae80054a71"
down_revision: Union[str, None] = "7e40ff74f735"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "recipes",
        sa.Column("primary_key", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("image_url", sa.String(length=200), nullable=False),
        sa.Column("url", sa.String(length=200), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("primary_key"),
    )
    op.create_table(
        "association_table",
        sa.Column("recipe_pk", sa.UUID(), nullable=True),
        sa.Column("ingredient_pk", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["ingredient_pk"],
            ["ingredients.primary_key"],
        ),
        sa.ForeignKeyConstraint(
            ["recipe_pk"],
            ["recipes.primary_key"],
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("association_table")
    op.drop_table("recipes")
    # ### end Alembic commands ###
