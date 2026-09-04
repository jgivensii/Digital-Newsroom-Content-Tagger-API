"""Comprehend Integration

Revision ID: 91689b06a51f
Revises: 5f25f373c4fd
Create Date: 2026-09-01 12:59:55.308279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91689b06a51f'
down_revision = '5f25f373c4fd'
branch_labels = None
depends_on = None


def upgrade():
    # Fixed: removed the invalid ForeignKeyConstraint on articles.body
    # (articles.body is a Text column with no unique constraint — Postgres
    #  requires the referenced column to be a PK or have a unique index).
    # The tag_extraction table was later renamed to tagextraction in e3543d09dbb5,
    # so we keep the original table name here and let the later migration handle the rename.
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
