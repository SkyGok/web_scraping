"""Initial schema with normalized industrial tables

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-11-03 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. industrial_zones
    op.create_table(
        'industrial_zones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('province', sa.String(length=100), nullable=False, server_default='Bursa'),
        sa.Column('district', sa.String(length=100), nullable=True),
        sa.Column('official_website', sa.String(length=500), nullable=True),
        sa.Column('portal_type', sa.String(length=50), nullable=False, server_default='osb_directory'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_industrial_zones_id', 'industrial_zones', ['id'])
    op.create_index('ix_industrial_zones_name', 'industrial_zones', ['name'], unique=True)
    op.create_index('ix_industrial_zones_slug', 'industrial_zones', ['slug'], unique=True)
    op.create_index('ix_industrial_zones_province', 'industrial_zones', ['province'])
    op.create_index('ix_industrial_zones_district', 'industrial_zones', ['district'])

    # 2. companies
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('zone_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('normalized_name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('registration_number', sa.String(length=100), nullable=True),
        sa.Column('tax_number', sa.String(length=50), nullable=True),
        sa.Column('sector', sa.String(length=150), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=False, server_default='Bursa'),
        sa.Column('district', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('primary_website', sa.String(length=500), nullable=True),
        sa.Column('phone', sa.String(length=100), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['zone_id'], ['industrial_zones.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('zone_id', 'normalized_name', name='uq_zone_company_normalized_name')
    )
    op.create_index('ix_companies_id', 'companies', ['id'])
    op.create_index('ix_companies_name', 'companies', ['name'])
    op.create_index('ix_companies_normalized_name', 'companies', ['normalized_name'])
    op.create_index('ix_companies_slug', 'companies', ['slug'], unique=True)
    op.create_index('ix_companies_zone_id', 'companies', ['zone_id'])
    op.create_index('ix_companies_sector', 'companies', ['sector'])

    # 3. contacts
    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('contact_type', sa.String(length=50), nullable=False),
        sa.Column('value', sa.String(length=255), nullable=False),
        sa.Column('label', sa.String(length=100), nullable=True),
        sa.Column('person_name', sa.String(length=150), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('source_url', sa.Text(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('is_public', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('retrieved_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('company_id', 'contact_type', 'value', name='uq_company_contact_value')
    )
    op.create_index('ix_contacts_id', 'contacts', ['id'])
    op.create_index('ix_contacts_company_id', 'contacts', ['company_id'])
    op.create_index('ix_contacts_contact_type', 'contacts', ['contact_type'])
    op.create_index('ix_contacts_value', 'contacts', ['value'])

    # 4. websites
    op.create_table(
        'websites',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('zone_id', sa.Integer(), nullable=True),
        sa.Column('company_id', sa.Integer(), nullable=True),
        sa.Column('domain', sa.String(length=255), nullable=False),
        sa.Column('base_url', sa.String(length=500), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('crawl_mode', sa.String(length=50), nullable=False, server_default='new_only'),
        sa.Column('last_visited_at', sa.DateTime(), nullable=True),
        sa.Column('last_success_at', sa.DateTime(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('http_status', sa.Integer(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('robots_allowed', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('crawl_delay', sa.Float(), nullable=False, server_default='2.0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['zone_id'], ['industrial_zones.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_websites_id', 'websites', ['id'])
    op.create_index('ix_websites_domain', 'websites', ['domain'], unique=True)
    op.create_index('ix_websites_status', 'websites', ['status'])

    # 5. scraped_pages
    op.create_table(
        'scraped_pages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('website_id', sa.Integer(), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('normalized_url', sa.String(length=500), nullable=False),
        sa.Column('page_type', sa.String(length=50), nullable=False, server_default='other'),
        sa.Column('http_status', sa.Integer(), nullable=True),
        sa.Column('content_hash', sa.String(length=64), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=True),
        sa.Column('raw_text', sa.Text(), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('scraped_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['website_id'], ['websites.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('website_id', 'normalized_url', name='uq_website_page_normalized_url')
    )
    op.create_index('ix_scraped_pages_id', 'scraped_pages', ['id'])
    op.create_index('ix_scraped_pages_normalized_url', 'scraped_pages', ['normalized_url'])
    op.create_index('ix_scraped_pages_website_id', 'scraped_pages', ['website_id'])

    # 6. scraping_jobs
    op.create_table(
        'scraping_jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('zone_id', sa.Integer(), nullable=True),
        sa.Column('website_id', sa.Integer(), nullable=True),
        sa.Column('job_type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('crawl_mode', sa.String(length=50), nullable=False, server_default='new_only'),
        sa.Column('total_targets', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('processed_targets', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('success_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('error_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('finished_at', sa.DateTime(), nullable=True),
        sa.Column('error_log', sa.Text(), nullable=True),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['zone_id'], ['industrial_zones.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['website_id'], ['websites.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_scraping_jobs_id', 'scraping_jobs', ['id'])
    op.create_index('ix_scraping_jobs_status', 'scraping_jobs', ['status'])

    # 7. sources
    op.create_table(
        'sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('source_url', sa.Text(), nullable=False),
        sa.Column('source_type', sa.String(length=50), nullable=False),
        sa.Column('retrieved_at', sa.DateTime(), nullable=False),
        sa.Column('http_status', sa.Integer(), nullable=True),
        sa.Column('raw_snippet', sa.Text(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_sources_id', 'sources', ['id'])
    op.create_index('ix_sources_entity_type', 'sources', ['entity_type'])
    op.create_index('ix_sources_entity_id', 'sources', ['entity_id'])

    # 8. data_changes
    op.create_table(
        'data_changes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('field_name', sa.String(length=100), nullable=False),
        sa.Column('old_value', sa.Text(), nullable=True),
        sa.Column('new_value', sa.Text(), nullable=True),
        sa.Column('change_type', sa.String(length=50), nullable=False),
        sa.Column('reason', sa.String(length=255), nullable=True),
        sa.Column('source_url', sa.Text(), nullable=True),
        sa.Column('changed_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_data_changes_id', 'data_changes', ['id'])
    op.create_index('ix_data_changes_entity_type', 'data_changes', ['entity_type'])
    op.create_index('ix_data_changes_entity_id', 'data_changes', ['entity_id'])


def downgrade() -> None:
    op.drop_table('data_changes')
    op.drop_table('sources')
    op.drop_table('scraping_jobs')
    op.drop_table('scraped_pages')
    op.drop_table('websites')
    op.drop_table('contacts')
    op.drop_table('companies')
    op.drop_table('industrial_zones')
