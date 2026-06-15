"""add unique constraints for schedule and slots

Revision ID: 95d09f86eb7b
Revises: 88ee2026c936
Create Date: 2026-06-15 23:40:21.532812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95d09f86eb7b'
down_revision: Union[str, None] = '88ee2026c936'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_unique_constraint(
        "uq_room_day_schedule",
        "schedules",
        ["room_id", "day_of_week"]
    )

    op.create_unique_constraint(
        "uq_room_start_slot",
        "slots",
        ["room_id", "start_at"]
    )


def downgrade():
    op.drop_constraint("uq_room_day_schedule", "schedules", type_="unique")
    op.drop_constraint("uq_room_start_slot", "slots", type_="unique")