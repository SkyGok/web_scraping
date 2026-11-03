def test_overview_endpoint(client):
    response = client.get("/api/v1/overview")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "osb_summaries" in data
    assert "recent_jobs" in data
    assert "total_zones" in data["metrics"]


def test_zones_crud_and_seed(client):
    # List zones
    res = client.get("/api/v1/zones")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

    # Create new zone
    new_zone = {
        "name": "Gemlik Serbest Bölgesi",
        "slug": "gemlik-serbest-bolge",
        "province": "Bursa",
        "district": "Gemlik",
        "official_website": "https://buseb.com.tr",
        "portal_type": "osb_directory"
    }
    create_res = client.post("/api/v1/zones", json=new_zone)
    assert create_res.status_code == 201
    zone_data = create_res.json()
    assert zone_data["slug"] == "gemlik-serbest-bolge"

    # Get zone detail
    detail_res = client.get(f"/api/v1/zones/{zone_data['id']}")
    assert detail_res.status_code == 200
    assert detail_res.json()["name"] == "Gemlik Serbest Bölgesi"


def test_company_creation_and_contacts(client):
    # Ensure zone exists
    zone_res = client.post("/api/v1/zones", json={
        "name": "Kayapa Test Zone",
        "slug": "kayapa-test-zone",
        "province": "Bursa"
    })
    zone_id = zone_res.json()["id"]

    # Create company
    company_payload = {
        "name": "Örnek Metal Teknolojileri A.Ş.",
        "slug": "ornek-metal-tekno",
        "zone_id": zone_id,
        "sector": "Metal ve Makine",
        "city": "Bursa",
        "district": "Nilüfer",
        "email": "info@ornekmetal.com.tr"
    }
    comp_res = client.post("/api/v1/companies", json=company_payload)
    assert comp_res.status_code == 201
    comp_data = comp_res.json()
    company_id = comp_data["id"]

    # Add verified business contact
    contact_payload = {
        "company_id": company_id,
        "contact_type": "sales_email",
        "value": "satis@ornekmetal.com.tr",
        "label": "Satış ve Pazarlama",
        "confidence_score": 0.95,
        "is_verified": True
    }
    contact_res = client.post("/api/v1/contacts", json=contact_payload)
    assert contact_res.status_code == 201
    contact_data = contact_res.json()
    assert contact_data["is_verified"] is True

    # List companies with has_contacts filter
    list_res = client.get(f"/api/v1/companies?zone_id={zone_id}&has_contacts=true")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1


def test_website_management_and_crawl_mode(client):
    # List websites
    res = client.get("/api/v1/websites")
    assert res.status_code == 200
    websites = res.json()
    if len(websites) > 0:
        target_website = websites[0]
        # Update crawl mode to retry_failed
        mode_res = client.put(
            f"/api/v1/websites/{target_website['id']}/crawl-mode",
            json={"crawl_mode": "retry_failed"}
        )
        assert mode_res.status_code == 200
        assert mode_res.json()["crawl_mode"] == "retry_failed"


def test_jobs_api(client):
    # Create scraping job
    job_payload = {
        "job_type": "company_discovery",
        "crawl_mode": "new_only"
    }
    res = client.post("/api/v1/jobs", json=job_payload)
    assert res.status_code == 201
    job_data = res.json()
    assert job_data["status"] == "pending"

    # Cancel job
    cancel_res = client.post(f"/api/v1/jobs/{job_data['id']}/cancel")
    assert cancel_res.status_code == 200
    assert cancel_res.json()["status"] == "cancelled"
