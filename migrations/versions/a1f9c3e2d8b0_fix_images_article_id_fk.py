"""Fix images.article_id FK — was pointing to publications.id, should be articles.id

Revision ID: a1f9c3e2d8b0
Revises: e7b38531b6c5
Create Date: 2026-09-04

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1f9c3e2d8b0'
down_revision = 'e7b38531b6c5'
branch_labels = None
depends_on = None


def upgrade():
    # Drop the incorrect FK that references publications.id
    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.drop_constraint('images_article_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(
            'images_article_id_fkey',
            'articles',
            ['article_id'],
            ['id'],
            ondelete='CASCADE'
        )


def downgrade():
    # Revert to the original (incorrect) FK pointing to publications.id
    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.drop_constraint('images_article_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(
            'images_article_id_fkey',
            'publications',
            ['article_id'],
            ['id'],
            ondelete='CASCADE'
        )
