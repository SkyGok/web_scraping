from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db, SessionLocal
from app.models.scraping_job import ScrapingJob
from app.models.industrial_zone import IndustrialZone
from app.models.website import Website
from app.schemas.job import JobOut, JobCreate
from app.services.scraper import scrape_website_sync

router = APIRouter()


def execute_scraping_job_task(job_id: int):
    """Background worker task to execute scraping pipelines across targets."""
    db = SessionLocal()
    try:
        job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
        if not job:
            return

        job.status = "running"
        job.started_at = datetime.utcnow()
        db.commit()

        # Determine target websites
        query = db.query(Website)
        if job.website_id:
            query = query.filter(Website.id == job.website_id)
        elif job.zone_id:
            query = query.filter(Website.zone_id == job.zone_id)

        # Apply crawl mode filtering
        if job.crawl_mode == "new_only":
            query = query.filter(Website.status.in_(["pending", "queued"]))
        elif job.crawl_mode == "retry_failed":
            query = query.filter(Website.status == "failed")

        targets = query.all()
        job.total_targets = len(targets)
        db.commit()

        successes = 0
        errors = 0
        logs = []

        for w in targets:
            try:
                res = scrape_website_sync(w.id, db, max_pages=15)
                if res.get("error"):
                    errors += 1
                    logs.append(f"[{w.domain}] Error: {res['error']}")
                else:
                    successes += 1
                    logs.append(f"[{w.domain}] Discovered: {res['companies_discovered']} companies, {res['contacts_discovered']} contacts")
            except Exception as e:
                errors += 1
                logs.append(f"[{w.domain}] Exception: {str(e)}")

            job.processed_targets += 1
            job.success_count = successes
            job.error_count = errors
            job.error_log = "\n".join(logs[-30:])
            db.commit()

        job.status = "completed" if errors == 0 or successes > 0 else "failed"
        job.finished_at = datetime.utcnow()
        db.commit()

    except Exception as job_err:
        if job:
            job.status = "failed"
            job.error_log = str(job_err)
            job.finished_at = datetime.utcnow()
            db.commit()
    finally:
        db.close()


@router.get("", response_model=List[JobOut])
def list_jobs(
    status: Optional[str] = Query(None, description="Filter by status (pending, running, completed, failed, cancelled)"),
    job_type: Optional[str] = Query(None, description="Filter by job type"),
    zone_id: Optional[int] = Query(None, description="Filter by zone ID"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(ScrapingJob)
    if status:
        query = query.filter(ScrapingJob.status == status)
    if job_type:
        query = query.filter(ScrapingJob.job_type == job_type)
    if zone_id:
        query = query.filter(ScrapingJob.zone_id == zone_id)

    jobs = query.order_by(ScrapingJob.created_at.desc()).offset(offset).limit(limit).all()
    results = []
    for job in jobs:
        zone_name = job.industrial_zone.name if job.industrial_zone else None
        domain = job.website.domain if job.website else None
        results.append(
            JobOut(
                id=job.id,
                zone_id=job.zone_id,
                zone_name=zone_name,
                website_id=job.website_id,
                website_domain=domain,
                job_type=job.job_type,
                status=job.status,
                crawl_mode=job.crawl_mode,
                total_targets=job.total_targets,
                processed_targets=job.processed_targets,
                success_count=job.success_count,
                error_count=job.error_count,
                started_at=job.started_at,
                finished_at=job.finished_at,
                error_log=job.error_log,
                created_at=job.created_at,
                updated_at=job.updated_at
            )
        )
    return results


@router.post("", response_model=JobOut, status_code=201)
def create_job(
    job_in: JobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    zone = None
    if job_in.zone_id:
        zone = db.query(IndustrialZone).filter(IndustrialZone.id == job_in.zone_id).first()
        if not zone:
            raise HTTPException(status_code=400, detail="Invalid zone ID")

    website = None
    if job_in.website_id:
        website = db.query(Website).filter(Website.id == job_in.website_id).first()
        if not website:
            raise HTTPException(status_code=400, detail="Invalid website ID")

    job = ScrapingJob(
        zone_id=job_in.zone_id,
        website_id=job_in.website_id,
        job_type=job_in.job_type,
        status="pending",
        crawl_mode=job_in.crawl_mode,
        total_targets=0,
        processed_targets=0,
        success_count=0,
        error_count=0
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Dispatch scraping execution
    background_tasks.add_task(execute_scraping_job_task, job.id)

    return JobOut(
        id=job.id,
        zone_id=job.zone_id,
        zone_name=zone.name if zone else None,
        website_id=job.website_id,
        website_domain=website.domain if website else None,
        job_type=job.job_type,
        status=job.status,
        crawl_mode=job.crawl_mode,
        total_targets=job.total_targets,
        processed_targets=job.processed_targets,
        success_count=job.success_count,
        error_count=job.error_count,
        started_at=job.started_at,
        finished_at=job.finished_at,
        error_log=job.error_log,
        created_at=job.created_at,
        updated_at=job.updated_at
    )


@router.post("/{job_id}/cancel", response_model=JobOut)
def cancel_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Scraping job not found")

    if job.status in ["completed", "failed"]:
        raise HTTPException(status_code=400, detail="Cannot cancel a finished job")

    job.status = "cancelled"
    job.finished_at = datetime.utcnow()
    db.commit()
    db.refresh(job)

    zone_name = job.industrial_zone.name if job.industrial_zone else None
    domain = job.website.domain if job.website else None

    return JobOut(
        id=job.id,
        zone_id=job.zone_id,
        zone_name=zone_name,
        website_id=job.website_id,
        website_domain=domain,
        job_type=job.job_type,
        status=job.status,
        crawl_mode=job.crawl_mode,
        total_targets=job.total_targets,
        processed_targets=job.processed_targets,
        success_count=job.success_count,
        error_count=job.error_count,
        started_at=job.started_at,
        finished_at=job.finished_at,
        error_log=job.error_log,
        created_at=job.created_at,
        updated_at=job.updated_at
    )
