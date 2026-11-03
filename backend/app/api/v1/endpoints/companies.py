import re
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.company import Company
from app.models.contact import Contact
from app.models.industrial_zone import IndustrialZone
from app.models.data_change import DataChange
from app.schemas.company import CompanyOut, CompanyDetail, CompanyCreate, CompanyUpdate
from app.schemas.contact import ContactOut

router = APIRouter()


def normalize_company_name(name: str) -> str:
    """Normalize Turkish characters, uppercase, trim, and strip company suffixes."""
    text = name.strip()
    # Turkish char replacements for normalization
    rep = {
        'ı': 'i', 'I': 'i', 'İ': 'i', 'ğ': 'g', 'Ğ': 'g',
        'ü': 'u', 'Ü': 'u', 'ş': 's', 'Ş': 's', 'ö': 'o',
        'Ö': 'o', 'ç': 'c', 'Ç': 'c'
    }
    for tr, en in rep.items():
        text = text.replace(tr, en)
    text = re.sub(r'\s+', ' ', text.lower())
    # Remove common corporation suffixes for matching
    text = re.sub(r'\b(san|tic|ltd|sti|a\.s|as|as\.|anonim|sirketi|ve)\b', '', text)
    return re.sub(r'[^a-z0-9]', '', text)


@router.get("", response_model=List[CompanyOut])
def list_companies(
    zone_id: Optional[int] = Query(None, description="Filter by industrial zone ID"),
    sector: Optional[str] = Query(None, description="Filter by industrial sector"),
    search: Optional[str] = Query(None, description="Search company name or description"),
    has_contacts: Optional[bool] = Query(None, description="Filter companies with/without contacts"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Company)
    if zone_id:
        query = query.filter(Company.zone_id == zone_id)
    if sector:
        query = query.filter(Company.sector.ilike(f"%{sector}%"))
    if search:
        query = query.filter(
            (Company.name.ilike(f"%{search}%")) |
            (Company.description.ilike(f"%{search}%")) |
            (Company.sector.ilike(f"%{search}%"))
        )

    if has_contacts is True:
        query = query.filter(Company.contacts.any())
    elif has_contacts is False:
        query = query.filter(~Company.contacts.any())

    companies = query.order_by(Company.name.asc()).offset(offset).limit(limit).all()
    results = []
    for company in companies:
        contact_count = db.query(func.count(Contact.id)).filter(Contact.company_id == company.id).scalar() or 0
        zone_name = company.industrial_zone.name if company.industrial_zone else None

        results.append(
            CompanyOut(
                id=company.id,
                zone_id=company.zone_id,
                zone_name=zone_name,
                name=company.name,
                normalized_name=company.normalized_name,
                slug=company.slug,
                registration_number=company.registration_number,
                tax_number=company.tax_number,
                sector=company.sector,
                address=company.address,
                city=company.city,
                district=company.district,
                description=company.description,
                primary_website=company.primary_website,
                phone=company.phone,
                email=company.email,
                is_active=company.is_active,
                contact_count=contact_count,
                created_at=company.created_at,
                updated_at=company.updated_at
            )
        )
    return results


@router.get("/{company_id}", response_model=CompanyDetail)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    zone_name = company.industrial_zone.name if company.industrial_zone else None
    contacts = db.query(Contact).filter(Contact.company_id == company.id).all()
    contact_outs = [
        ContactOut(
            id=c.id,
            company_id=c.company_id,
            company_name=company.name,
            zone_name=zone_name,
            contact_type=c.contact_type,
            value=c.value,
            label=c.label,
            person_name=c.person_name,
            department=c.department,
            source_url=c.source_url,
            confidence_score=c.confidence_score,
            is_verified=c.is_verified,
            is_public=c.is_public,
            retrieved_at=c.retrieved_at,
            created_at=c.created_at,
            updated_at=c.updated_at
        ) for c in contacts
    ]

    return CompanyDetail(
        id=company.id,
        zone_id=company.zone_id,
        zone_name=zone_name,
        name=company.name,
        normalized_name=company.normalized_name,
        slug=company.slug,
        registration_number=company.registration_number,
        tax_number=company.tax_number,
        sector=company.sector,
        address=company.address,
        city=company.city,
        district=company.district,
        description=company.description,
        primary_website=company.primary_website,
        phone=company.phone,
        email=company.email,
        is_active=company.is_active,
        contact_count=len(contacts),
        contacts=contact_outs,
        created_at=company.created_at,
        updated_at=company.updated_at
    )


@router.post("", response_model=CompanyOut, status_code=201)
def create_company(company_in: CompanyCreate, db: Session = Depends(get_db)):
    zone = db.query(IndustrialZone).filter(IndustrialZone.id == company_in.zone_id).first()
    if not zone:
        raise HTTPException(status_code=400, detail="Invalid industrial zone ID")

    normalized_name = company_in.normalized_name or normalize_company_name(company_in.name)

    existing = db.query(Company).filter(
        Company.zone_id == company_in.zone_id,
        Company.normalized_name == normalized_name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company already registered in this industrial zone")

    company_data = company_in.model_dump()
    company_data["normalized_name"] = normalized_name
    company = Company(**company_data)
    db.add(company)
    db.flush()

    # Log data change for audit provenance
    change = DataChange(
        entity_type="company",
        entity_id=company.id,
        field_name="name",
        old_value=None,
        new_value=company.name,
        change_type="created",
        reason="Manual creation or initial discovery"
    )
    db.add(change)
    db.commit()
    db.refresh(company)

    return CompanyOut(
        id=company.id,
        zone_id=company.zone_id,
        zone_name=zone.name,
        name=company.name,
        normalized_name=company.normalized_name,
        slug=company.slug,
        registration_number=company.registration_number,
        tax_number=company.tax_number,
        sector=company.sector,
        address=company.address,
        city=company.city,
        district=company.district,
        description=company.description,
        primary_website=company.primary_website,
        phone=company.phone,
        email=company.email,
        is_active=company.is_active,
        contact_count=0,
        created_at=company.created_at,
        updated_at=company.updated_at
    )
