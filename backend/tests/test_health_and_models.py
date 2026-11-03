from app.models.industrial_zone import IndustrialZone
from app.models.company import Company
from app.models.contact import Contact
from app.models.website import Website
from app.models.scraped_page import ScrapedPage
from app.models.scraping_job import ScrapingJob
from app.seed.seed_bursa_zones import seed_bursa_industrial_zones


def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "healthy" in data["database"]


def test_seed_bursa_zones(db):
    zones = db.query(IndustrialZone).all()
    if len(zones) == 0:
        seeded = seed_bursa_industrial_zones(db)
        assert seeded >= 12
    else:
        assert len(zones) >= 12
    # Verify records exist in database
    websites = db.query(Website).all()
    assert len(websites) >= 12


def test_unique_company_per_zone(db):
    zone = IndustrialZone(
        name="Test Unique OSB",
        slug="test-unique-osb",
        province="Bursa",
        district="Nilüfer"
    )
    db.add(zone)
    db.commit()
    db.refresh(zone)

    c1 = Company(
        zone_id=zone.id,
        name="Akasya Otomotiv Sanayi A.Ş.",
        normalized_name="akasyaotomotiv",
        slug="akasya-otomotiv",
        city="Bursa"
    )
    db.add(c1)
    db.commit()

    # Attempt to insert duplicate company in same zone should fail uniqueness
    import pytest
    from sqlalchemy.exc import IntegrityError
    with pytest.raises(IntegrityError):
        c2 = Company(
            zone_id=zone.id,
            name="Akasya Otomotiv Sanayi Ltd. Şti.",
            normalized_name="akasyaotomotiv",
            slug="akasya-otomotiv-2",
            city="Bursa"
        )
        db.add(c2)
        db.commit()
    db.rollback()


def test_unique_contact_per_company(db):
    zone = IndustrialZone(name="Contact Test OSB", slug="contact-test-osb", province="Bursa")
    db.add(zone)
    db.commit()
    db.refresh(zone)

    company = Company(
        zone_id=zone.id,
        name="Beta Makine A.Ş.",
        normalized_name="betamakine",
        slug="beta-makine"
    )
    db.add(company)
    db.commit()
    db.refresh(company)

    contact1 = Contact(
        company_id=company.id,
        contact_type="email",
        value="info@betamakine.com",
        label="Genel İletişim"
    )
    db.add(contact1)
    db.commit()

    # Duplicate contact type + value should raise IntegrityError
    import pytest
    from sqlalchemy.exc import IntegrityError
    with pytest.raises(IntegrityError):
        contact2 = Contact(
            company_id=company.id,
            contact_type="email",
            value="info@betamakine.com",
            label="İkincil"
        )
        db.add(contact2)
        db.commit()
    db.rollback()
