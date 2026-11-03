from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.industrial_zone import IndustrialZone
from app.models.company import Company
from app.models.contact import Contact
from app.models.website import Website
from app.models.scraped_page import ScrapedPage
from app.models.scraping_job import ScrapingJob
from app.schemas.overview import OverviewResponse, MetricStats, OSBSummary, RecentJobSummary

router = APIRouter()


@router.get("", response_model=OverviewResponse)
def get_overview_data(db: Session = Depends(get_db)):
    # Total counts
    total_zones = db.query(func.count(IndustrialZone.id)).scalar() or 0
    total_companies = db.query(func.count(Company.id)).scalar() or 0
    total_contacts = db.query(func.count(Contact.id)).scalar() or 0
    total_websites = db.query(func.count(Website.id)).scalar() or 0
    scraped_pages = db.query(func.count(ScrapedPage.id)).scalar() or 0
    verified_contacts_count = db.query(func.count(Contact.id)).filter(Contact.is_verified == True).scalar() or 0

    active_jobs = db.query(func.count(ScrapingJob.id)).filter(ScrapingJob.status == "running").scalar() or 0
    completed_jobs = db.query(func.count(ScrapingJob.id)).filter(ScrapingJob.status == "completed").scalar() or 0
    failed_jobs = db.query(func.count(ScrapingJob.id)).filter(ScrapingJob.status == "failed").scalar() or 0

    metrics = MetricStats(
        total_zones=total_zones,
        total_companies=total_companies,
        total_contacts=total_contacts,
        total_websites=total_websites,
        active_jobs=active_jobs,
        completed_jobs=completed_jobs,
        failed_jobs=failed_jobs,
        scraped_pages=scraped_pages,
        verified_contacts_count=verified_contacts_count
    )

    # OSB summaries
    zones = db.query(IndustrialZone).order_by(IndustrialZone.name.asc()).all()
    osb_summaries = []
    for zone in zones:
        company_count = db.query(func.count(Company.id)).filter(Company.zone_id == zone.id).scalar() or 0
        contact_count = db.query(func.count(Contact.id)).join(Company).filter(Company.zone_id == zone.id).scalar() or 0
        website = db.query(Website).filter(Website.zone_id == zone.id).first()
        website_status = website.status if website else "not_configured"

        osb_summaries.append(
            OSBSummary(
                id=zone.id,
                name=zone.name,
                province=zone.province,
                district=zone.district,
                company_count=company_count,
                contact_count=contact_count,
                website_status=website_status,
                portal_type=zone.portal_type
            )
        )

    # Recent jobs
    recent_jobs_db = db.query(ScrapingJob).order_by(ScrapingJob.created_at.desc()).limit(10).all()
    recent_jobs = []
    for job in recent_jobs_db:
        zone_name = job.industrial_zone.name if job.industrial_zone else None
        recent_jobs.append(
            RecentJobSummary(
                id=job.id,
                job_type=job.job_type,
                status=job.status,
                crawl_mode=job.crawl_mode,
                zone_name=zone_name,
                total_targets=job.total_targets,
                processed_targets=job.processed_targets,
                success_count=job.success_count,
                error_count=job.error_count,
                started_at=job.started_at.isoformat() if job.started_at else None,
                finished_at=job.finished_at.isoformat() if job.finished_at else None
            )
        )

    return OverviewResponse(
        metrics=metrics,
        osb_summaries=osb_summaries,
        recent_jobs=recent_jobs
    )
