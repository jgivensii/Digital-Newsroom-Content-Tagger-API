"""Comprehend Integration - Corrected data type from ARRAY(String) -> JSONB for tags, entities

Revision ID: 17132eda8646
Revises: e3543d09dbb5
Create Date: 2026-09-01 14:36:54.820018

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '17132eda8646'
down_revision = 'e3543d09dbb5'
branch_labels = None
depends_on = None


def upgrade():
    # PostgreSQL cannot auto-cast ARRAY(VARCHAR) -> JSONB.
    # We must supply a USING expression that converts each text array to a
    # JSON array string and then casts it to jsonb.
    op.execute(
        "ALTER TABLE tagextraction "
        "ALTER COLUMN tags TYPE JSONB "
        "USING to_jsonb(tags)"
    )
    op.execute(
        "ALTER TABLE tagextraction "
        "ALTER COLUMN entities TYPE JSONB "
        "USING to_jsonb(entities)"
    )


def downgrade():
    op.execute(
        "ALTER TABLE tagextraction "
        "ALTER COLUMN tags TYPE VARCHAR[] "
        "USING ARRAY(SELECT jsonb_array_elements_text(tags))"
    )
    op.execute(
        "ALTER TABLE tagextraction "
        "ALTER COLUMN entities TYPE VARCHAR[] "
        "USING ARRAY(SELECT jsonb_array_elements_text(entities))"
    )
