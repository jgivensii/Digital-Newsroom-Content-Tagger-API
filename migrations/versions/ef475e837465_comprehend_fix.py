"""Comprehend Fix

Revision ID: ef475e837465
Revises: 17132eda8646
Create Date: 2026-09-01 14:46:57.374272

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ef475e837465'
down_revision = '17132eda8646'
branch_labels = None
depends_on = None


def upgrade():
    # tagextraction already exists with JSONB columns after 17132eda8646.
    # Drop and recreate cleanly with the final correct schema.
    op.drop_table('tagextraction')
    op.create_table(
        'tagextraction',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('article_id', sa.UUID(), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('entities', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('tagextraction')
