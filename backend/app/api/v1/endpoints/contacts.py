from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.contact import Contact
from app.models.company import Company
from app.models.data_change import DataChange
from app.schemas.contact import ContactOut, ContactCreate, ContactUpdate

router = APIRouter()


@router.get("", response_model=List[ContactOut])
def list_contacts(
    company_id: Optional[int] = Query(None, description="Filter by company ID"),
    zone_id: Optional[int] = Query(None, description="Filter by industrial zone ID"),
    contact_type: Optional[str] = Query(None, description="Filter by contact type (email, phone, sales_email, etc.)"),
    is_verified: Optional[bool] = Query(None, description="Filter verified contacts only"),
    search: Optional[str] = Query(None, description="Search contact value, person name, or department"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Contact).join(Company)
    if company_id:
        query = query.filter(Contact.company_id == company_id)
    if zone_id:
        query = query.filter(Company.zone_id == zone_id)
    if contact_type:
        query = query.filter(Contact.contact_type == contact_type)
    if is_verified is not None:
        query = query.filter(Contact.is_verified == is_verified)
    if search:
        query = query.filter(
            (Contact.value.ilike(f"%{search}%")) |
            (Contact.person_name.ilike(f"%{search}%")) |
            (Contact.department.ilike(f"%{search}%")) |
            (Company.name.ilike(f"%{search}%"))
        )

    contacts = query.order_by(Contact.id.desc()).offset(offset).limit(limit).all()
    results = []
    for c in contacts:
        results.append(
            ContactOut(
                id=c.id,
                company_id=c.company_id,
                company_name=c.company.name if c.company else None,
                zone_name=c.company.industrial_zone.name if c.company and c.company.industrial_zone else None,
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
            )
        )
    return results


@router.post("", response_model=ContactOut, status_code=201)
def create_contact(contact_in: ContactCreate, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == contact_in.company_id).first()
    if not company:
        raise HTTPException(status_code=400, detail="Company does not exist")

    # Check duplicate contact for this company
    existing = db.query(Contact).filter(
        Contact.company_id == contact_in.company_id,
        Contact.contact_type == contact_in.contact_type,
        Contact.value == contact_in.value
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="This contact already exists for this company")

    contact = Contact(**contact_in.model_dump())
    db.add(contact)
    db.flush()

    # Log data change
    change = DataChange(
        entity_type="contact",
        entity_id=contact.id,
        field_name=contact.contact_type,
        old_value=None,
        new_value=contact.value,
        change_type="created",
        reason="Manual creation or extraction",
        source_url=contact.source_url
    )
    db.add(change)
    db.commit()
    db.refresh(contact)

    return ContactOut(
        id=contact.id,
        company_id=contact.company_id,
        company_name=company.name,
        zone_name=company.industrial_zone.name if company.industrial_zone else None,
        contact_type=contact.contact_type,
        value=contact.value,
        label=contact.label,
        person_name=contact.person_name,
        department=contact.department,
        source_url=contact.source_url,
        confidence_score=contact.confidence_score,
        is_verified=contact.is_verified,
        is_public=contact.is_public,
        retrieved_at=contact.retrieved_at,
        created_at=contact.created_at,
        updated_at=contact.updated_at
    )


@router.put("/{contact_id}/verify", response_model=ContactOut)
def toggle_verify_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    old_status = contact.is_verified
    contact.is_verified = not contact.is_verified

    change = DataChange(
        entity_type="contact",
        entity_id=contact.id,
        field_name="is_verified",
        old_value=str(old_status),
        new_value=str(contact.is_verified),
        change_type="updated",
        reason="Verification status toggled"
    )
    db.add(change)
    db.commit()
    db.refresh(contact)

    return ContactOut(
        id=contact.id,
        company_id=contact.company_id,
        company_name=contact.company.name if contact.company else None,
        zone_name=contact.company.industrial_zone.name if contact.company and contact.company.industrial_zone else None,
        contact_type=contact.contact_type,
        value=contact.value,
        label=contact.label,
        person_name=contact.person_name,
        department=contact.department,
        source_url=contact.source_url,
        confidence_score=contact.confidence_score,
        is_verified=contact.is_verified,
        is_public=contact.is_public,
        retrieved_at=contact.retrieved_at,
        created_at=contact.created_at,
        updated_at=contact.updated_at
    )
