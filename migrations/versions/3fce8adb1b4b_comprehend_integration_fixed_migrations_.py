"""Comprehend Integration - Fixed Migrations error

Revision ID: 3fce8adb1b4b
Revises: 91689b06a51f
Create Date: 2026-09-01 13:19:12.781765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fce8adb1b4b'
down_revision = '91689b06a51f'
branch_labels = None
depends_on = None


def upgrade():
    # Drop the version created by 91689b06a51f (which had the bad body FK)
    # and recreate cleanly with body as Text (not a FK reference).
    op.drop_table('tag_extraction')
    op.create_table(
        'tag_extraction',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('article_id', sa.UUID(), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('tags', sa.ARRAY(sa.String()), nullable=False),
        sa.Column('entities', sa.ARRAY(sa.String()), nullable=False),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('tag_extraction')
