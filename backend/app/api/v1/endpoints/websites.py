from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.website import Website
from app.models.scraped_page import ScrapedPage
from app.schemas.website import WebsiteOut, WebsiteCrawlModeUpdate, WebsiteUpdate

router = APIRouter()


@router.get("", response_model=List[WebsiteOut])
def list_websites(
    status: Optional[str] = Query(None, description="Filter by status (pending, completed, failed, in_progress, paused)"),
    crawl_mode: Optional[str] = Query(None, description="Filter by crawl mode (new_only, retry_failed, refresh_all)"),
    search: Optional[str] = Query(None, description="Search domain or base URL"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Website)
    if status:
        query = query.filter(Website.status == status)
    if crawl_mode:
        query = query.filter(Website.crawl_mode == crawl_mode)
    if search:
        query = query.filter(
            (Website.domain.ilike(f"%{search}%")) |
            (Website.base_url.ilike(f"%{search}%"))
        )

    websites = query.order_by(Website.id.asc()).offset(offset).limit(limit).all()
    results = []
    for w in websites:
        pages_count = db.query(func.count(ScrapedPage.id)).filter(ScrapedPage.website_id == w.id).scalar() or 0
        zone_name = w.industrial_zone.name if w.industrial_zone else None
        company_name = w.company.name if w.company else None

        results.append(
            WebsiteOut(
                id=w.id,
                domain=w.domain,
                base_url=w.base_url,
                zone_id=w.zone_id,
                zone_name=zone_name,
                company_id=w.company_id,
                company_name=company_name,
                status=w.status,
                crawl_mode=w.crawl_mode,
                crawl_delay=w.crawl_delay,
                robots_allowed=w.robots_allowed,
                pages_count=pages_count,
                last_visited_at=w.last_visited_at,
                last_success_at=w.last_success_at,
                error_message=w.error_message,
                http_status=w.http_status,
                retry_count=w.retry_count,
                created_at=w.created_at,
                updated_at=w.updated_at
            )
        )
    return results


@router.put("/{website_id}/crawl-mode", response_model=WebsiteOut)
def update_crawl_mode(
    website_id: int,
    mode_in: WebsiteCrawlModeUpdate,
    db: Session = Depends(get_db)
):
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    valid_modes = ["new_only", "retry_failed", "refresh_all"]
    if mode_in.crawl_mode not in valid_modes:
        raise HTTPException(status_code=400, detail=f"Invalid crawl mode. Must be one of: {valid_modes}")

    website.crawl_mode = mode_in.crawl_mode
    db.commit()
    db.refresh(website)

    pages_count = db.query(func.count(ScrapedPage.id)).filter(ScrapedPage.website_id == website.id).scalar() or 0
    zone_name = website.industrial_zone.name if website.industrial_zone else None
    company_name = website.company.name if website.company else None

    return WebsiteOut(
        id=website.id,
        domain=website.domain,
        base_url=website.base_url,
        zone_id=website.zone_id,
        zone_name=zone_name,
        company_id=website.company_id,
        company_name=company_name,
        status=website.status,
        crawl_mode=website.crawl_mode,
        crawl_delay=website.crawl_delay,
        robots_allowed=website.robots_allowed,
        pages_count=pages_count,
        last_visited_at=website.last_visited_at,
        last_success_at=website.last_success_at,
        error_message=website.error_message,
        http_status=website.http_status,
        retry_count=website.retry_count,
        created_at=website.created_at,
        updated_at=website.updated_at
    )


@router.post("/{website_id}/retry", response_model=WebsiteOut)
def retry_failed_website(website_id: int, db: Session = Depends(get_db)):
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    website.status = "queued"
    website.error_message = None
    website.retry_count += 1
    db.commit()
    db.refresh(website)

    pages_count = db.query(func.count(ScrapedPage.id)).filter(ScrapedPage.website_id == website.id).scalar() or 0
    zone_name = website.industrial_zone.name if website.industrial_zone else None
    company_name = website.company.name if website.company else None

    return WebsiteOut(
        id=website.id,
        domain=website.domain,
        base_url=website.base_url,
        zone_id=website.zone_id,
        zone_name=zone_name,
        company_id=website.company_id,
        company_name=company_name,
        status=website.status,
        crawl_mode=website.crawl_mode,
        crawl_delay=website.crawl_delay,
        robots_allowed=website.robots_allowed,
        pages_count=pages_count,
        last_visited_at=website.last_visited_at,
        last_success_at=website.last_success_at,
        error_message=website.error_message,
        http_status=website.http_status,
        retry_count=website.retry_count,
        created_at=website.created_at,
        updated_at=website.updated_at
    )
