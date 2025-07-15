"""create materialized view for checking regional heatmaps

Revision ID: ca12f24ee33f
Revises: 31b938c0ab0f
Create Date: 2025-05-03 22:09:53.666580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca12f24ee33f'
down_revision = '31b938c0ab0f'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE MATERIALIZED VIEW regional_heatmap AS 
        SELECT last_known_location, COUNT(*) AS location_count
        FROM missing_person
        GROUP BY last_known_location 
        ORDER BY location_count DESC
        
        ;
    """)


def downgrade():
        op.execute("DROP MATERIALIZED VIEW IF EXISTS regional_heatmap;")

