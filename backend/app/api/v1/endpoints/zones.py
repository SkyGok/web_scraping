from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.industrial_zone import IndustrialZone
from app.models.company import Company
from app.models.contact import Contact
from app.schemas.zone import ZoneOut, ZoneCreate, ZoneUpdate
from app.seed.seed_bursa_zones import seed_bursa_industrial_zones

router = APIRouter()


@router.get("", response_model=List[ZoneOut])
def list_zones(
    province: Optional[str] = Query(None, description="Filter by province"),
    search: Optional[str] = Query(None, description="Search by zone name or district"),
    db: Session = Depends(get_db)
):
    query = db.query(IndustrialZone)
    if province:
        query = query.filter(IndustrialZone.province.ilike(f"%{province}%"))
    if search:
        query = query.filter(
            (IndustrialZone.name.ilike(f"%{search}%")) |
            (IndustrialZone.district.ilike(f"%{search}%"))
        )

    zones = query.order_by(IndustrialZone.name.asc()).all()
    results = []
    for zone in zones:
        company_count = db.query(func.count(Company.id)).filter(Company.zone_id == zone.id).scalar() or 0
        contact_count = db.query(func.count(Contact.id)).join(Company).filter(Company.zone_id == zone.id).scalar() or 0

        zone_out = ZoneOut(
            id=zone.id,
            name=zone.name,
            slug=zone.slug,
            province=zone.province,
            district=zone.district,
            official_website=zone.official_website,
            portal_type=zone.portal_type,
            description=zone.description,
            is_active=zone.is_active,
            company_count=company_count,
            contact_count=contact_count,
            created_at=zone.created_at,
            updated_at=zone.updated_at
        )
        results.append(zone_out)

    return results


@router.post("/seed", status_code=201)
def seed_zones(db: Session = Depends(get_db)):
    """Seed initial Bursa industrial zones and portal websites."""
    count = seed_bursa_industrial_zones(db)
    return {"message": f"Successfully seeded {count} Bursa industrial zones and portal websites.", "seeded": count}


@router.get("/{zone_id}", response_model=ZoneOut)
def get_zone(zone_id: int, db: Session = Depends(get_db)):
    zone = db.query(IndustrialZone).filter(IndustrialZone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Industrial zone not found")

    company_count = db.query(func.count(Company.id)).filter(Company.zone_id == zone.id).scalar() or 0
    contact_count = db.query(func.count(Contact.id)).join(Company).filter(Company.zone_id == zone.id).scalar() or 0

    return ZoneOut(
        id=zone.id,
        name=zone.name,
        slug=zone.slug,
        province=zone.province,
        district=zone.district,
        official_website=zone.official_website,
        portal_type=zone.portal_type,
        description=zone.description,
        is_active=zone.is_active,
        company_count=company_count,
        contact_count=contact_count,
        created_at=zone.created_at,
        updated_at=zone.updated_at
    )


@router.post("", response_model=ZoneOut, status_code=201)
def create_zone(zone_in: ZoneCreate, db: Session = Depends(get_db)):
    existing = db.query(IndustrialZone).filter(IndustrialZone.slug == zone_in.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Zone with this slug already exists")

    zone = IndustrialZone(**zone_in.model_dump())
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return ZoneOut(
        id=zone.id,
        name=zone.name,
        slug=zone.slug,
        province=zone.province,
        district=zone.district,
        official_website=zone.official_website,
        portal_type=zone.portal_type,
        description=zone.description,
        is_active=zone.is_active,
        company_count=0,
        contact_count=0,
        created_at=zone.created_at,
        updated_at=zone.updated_at
    )
