import re
import hashlib
import logging
from datetime import datetime
from typing import Dict, Any, List, Set, Optional, Tuple
from urllib.parse import urlparse, urljoin, urldefrag
import urllib.robotparser

import httpx
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.website import Website
from app.models.scraped_page import ScrapedPage
from app.models.company import Company
from app.models.contact import Contact
from app.models.source import Source
from app.models.data_change import DataChange
from app.models.industrial_zone import IndustrialZone

logger = logging.getLogger("industrial_scraper")

# Email regex pattern
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')

# Turkish phone regex patterns (0224..., +90..., 0850..., 05...)
PHONE_REGEX = re.compile(
    r'(?:\+?90\s?|0)?(?:224|212|216|262|232|312|850|5\d{2})\s?\d{3}\s?\d{2}\s?\d{2}'
)

# VKN (Vergi Kimlik Numarası) 10-digit tax number pattern
TAX_NUMBER_REGEX = re.compile(r'\b\d{10}\b')


def normalize_domain(url: str) -> str:
    """Extract clean domain name without www or port."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    if ":" in domain:
        domain = domain.split(":")[0]
    return domain


def normalize_url(raw_url: str, base_url: str) -> Optional[str]:
    """Join relative URLs, clean tracking parameters and fragments."""
    try:
        joined = urljoin(base_url, raw_url)
        clean, _ = urldefrag(joined)
        parsed = urlparse(clean)
        if parsed.scheme not in ("http", "https"):
            return None
        # Discard media files
        lower_path = parsed.path.lower()
        if any(lower_path.endswith(ext) for ext in ('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.css', '.js', '.svg')):
            return None
        # Clean query
        return clean
    except Exception:
        return None


def clean_company_name(name: str) -> str:
    """Normalize whitespace and strip HTML remnants."""
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def normalize_company_key(name: str) -> str:
    """Create normalization key for duplicate prevention."""
    text = name.strip()
    rep = {
        'ı': 'i', 'I': 'i', 'İ': 'i', 'ğ': 'g', 'Ğ': 'g',
        'ü': 'u', 'Ü': 'u', 'ş': 's', 'Ş': 's', 'ö': 'o',
        'Ö': 'o', 'ç': 'c', 'Ç': 'c'
    }
    for tr, en in rep.items():
        text = text.replace(tr, en)
    text = re.sub(r'\s+', ' ', text.lower())
    text = re.sub(r'\b(san|tic|ltd|sti|a\.s|as|as\.|anonim|sirketi|ve)\b', '', text)
    return re.sub(r'[^a-z0-9]', '', text)


def slugify(text: str) -> str:
    """Convert text to URL slug."""
    text = text.strip()
    rep = {
        'ı': 'i', 'I': 'i', 'İ': 'i', 'ğ': 'g', 'Ğ': 'g',
        'ü': 'u', 'Ü': 'u', 'ş': 's', 'Ş': 's', 'ö': 'o',
        'Ö': 'o', 'ç': 'c', 'Ç': 'c'
    }
    for tr, en in rep.items():
        text = text.replace(tr, en)
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text).lower()
    return re.sub(r'[\s-]+', '-', text).strip('-')


def check_robots_allowed(base_url: str, user_agent: str = settings.USER_AGENT) -> bool:
    """Check site robots.txt policy."""
    try:
        parsed = urlparse(base_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, base_url)
    except Exception as e:
        logger.debug(f"robots.txt check failed or unavailable for {base_url}: {e}")
        return True


def extract_contacts_from_text(
    text: str,
    source_url: str
) -> List[Dict[str, Any]]:
    """Extract public emails, phone numbers, and departments from page text."""
    contacts = []
    seen = set()

    # Extract emails
    for email in EMAIL_REGEX.findall(text):
        email_clean = email.lower().strip()
        # Filter invalid file-like emails
        if any(email_clean.endswith(ext) for ext in ('.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.webp')):
            continue
        if email_clean not in seen:
            seen.add(email_clean)
            label = "Genel İletişim"
            if "satis" in email_clean or "export" in email_clean:
                label = "Satış & İhracat"
            elif "ik" in email_clean or "hr" in email_clean or "kariyer" in email_clean:
                label = "İnsan Kaynakları"
            elif "muhasebe" in email_clean:
                label = "Muhasebe & Finans"

            contacts.append({
                "contact_type": "email",
                "value": email_clean,
                "label": label,
                "confidence_score": 0.95,
                "source_url": source_url,
                "is_verified": False,
                "is_public": True
            })

    # Extract phone numbers
    for phone in PHONE_REGEX.findall(text):
        clean_phone = re.sub(r'[^\d+]', '', phone)
        if len(clean_phone) >= 10 and clean_phone not in seen:
            seen.add(clean_phone)
            # Format nicely
            contacts.append({
                "contact_type": "phone",
                "value": phone.strip(),
                "label": "Santral / Telefon",
                "confidence_score": 0.90,
                "source_url": source_url,
                "is_verified": False,
                "is_public": True
            })

    return contacts


def scrape_website_sync(
    website_id: int,
    db: Session,
    max_pages: int = 15
) -> Dict[str, Any]:
    """
    Crawls website, extracts directory records or company pages,
    saves discovered companies and contacts, and logs audit changes.
    """
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise ValueError(f"Website with ID {website_id} not found")

    website.status = "in_progress"
    website.last_visited_at = datetime.utcnow()
    db.commit()

    headers = {
        "User-Agent": settings.USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    visited_urls: Set[str] = set()
    to_visit: List[Tuple[str, str]] = [(website.base_url, "home")]
    companies_discovered = 0
    contacts_discovered = 0
    pages_scraped = 0
    error_message = None
    http_status_code = None

    try:
        # Check robots.txt
        website.robots_allowed = check_robots_allowed(website.base_url)

        with httpx.Client(headers=headers, timeout=15.0, follow_redirects=True, verify=False) as client:
            while to_visit and len(visited_urls) < max_pages:
                curr_url, page_type = to_visit.pop(0)
                norm_curr_url = normalize_url(curr_url, website.base_url)
                if not norm_curr_url or norm_curr_url in visited_urls:
                    continue

                visited_urls.add(norm_curr_url)

                try:
                    resp = client.get(norm_curr_url)
                    http_status_code = resp.status_code
                    if resp.status_code >= 400:
                        continue

                    html = resp.text
                    pages_scraped += 1
                    soup = BeautifulSoup(html, "lxml")

                    title = soup.title.string.strip() if soup.title and soup.title.string else norm_curr_url
                    text_content = soup.get_text(separator=' ', strip=True)
                    content_hash = hashlib.sha256(text_content.encode("utf-8")).hexdigest()

                    # Save Scraped Page
                    existing_page = db.query(ScrapedPage).filter(
                        ScrapedPage.website_id == website.id,
                        ScrapedPage.normalized_url == norm_curr_url
                    ).first()

                    if not existing_page:
                        scraped_page = ScrapedPage(
                            website_id=website.id,
                            url=curr_url,
                            normalized_url=norm_curr_url,
                            page_type=page_type,
                            http_status=resp.status_code,
                            content_hash=content_hash,
                            title=title[:500],
                            raw_text=text_content[:20000],
                            scraped_at=datetime.utcnow()
                        )
                        db.add(scraped_page)
                    else:
                        existing_page.http_status = resp.status_code
                        existing_page.content_hash = content_hash
                        existing_page.scraped_at = datetime.utcnow()

                    db.flush()

                    # 1. Company Discovery: Look for directories, member tables, cards
                    # Common selectors on Turkish OSB portals: table, .card, .firma, .member, article
                    zone_id = website.zone_id
                    if not zone_id:
                        # Fallback to first zone
                        first_zone = db.query(IndustrialZone).first()
                        zone_id = first_zone.id if first_zone else None

                    # If this is an OSB portal, find company elements or directory links
                    candidate_elements = soup.select(
                        "table tr, .firma, .company, .member, .member-card, .kurumsal, .directory-item, .card"
                    )

                    for el in candidate_elements:
                        el_text = el.get_text(separator=' ', strip=True)
                        # Check if element looks like a company name (contains A.Ş., Ltd., Şti., Sanayi, etc.)
                        has_corp_marker = any(m in el_text.lower() for m in ['a.ş', 'ltd', 'şti', 'sanayi', 'ticaret', 'makine', 'otomotiv', 'tekstil'])
                        if has_corp_marker and len(el_text) < 400:
                            # Extract company name from first bold tag, h3, h4, or strong
                            name_el = el.find(['h2', 'h3', 'h4', 'strong', 'b', 'a'])
                            cand_name = name_el.get_text(strip=True) if name_el else el_text.split('\n')[0]
                            cand_name = clean_company_name(cand_name)

                            if 3 < len(cand_name) < 150 and zone_id:
                                norm_key = normalize_company_key(cand_name)
                                if norm_key:
                                    existing_comp = db.query(Company).filter(
                                        Company.zone_id == zone_id,
                                        Company.normalized_name == norm_key
                                    ).first()

                                    if not existing_comp:
                                        c_slug = slugify(cand_name) + f"-{zone_id}"
                                        new_comp = Company(
                                            zone_id=zone_id,
                                            name=cand_name,
                                            normalized_name=norm_key,
                                            slug=c_slug,
                                            city="Bursa",
                                            description=el_text[:500],
                                            is_active=True
                                        )
                                        db.add(new_comp)
                                        db.flush()
                                        companies_discovered += 1

                                        # Record Provenance Source
                                        src = Source(
                                            entity_type="company",
                                            entity_id=new_comp.id,
                                            source_url=norm_curr_url,
                                            source_type="osb_directory",
                                            http_status=resp.status_code,
                                            raw_snippet=el_text[:300],
                                            confidence=0.92
                                        )
                                        db.add(src)

                                        # Extract contacts for this company from the element snippet
                                        el_contacts = extract_contacts_from_text(el_text, norm_curr_url)
                                        for ct in el_contacts:
                                            contact_obj = Contact(
                                                company_id=new_comp.id,
                                                contact_type=ct["contact_type"],
                                                value=ct["value"],
                                                label=ct["label"],
                                                confidence_score=ct["confidence_score"],
                                                source_url=ct["source_url"],
                                                is_verified=False,
                                                is_public=True
                                            )
                                            db.add(contact_obj)
                                            contacts_discovered += 1

                    # 2. General Page Contact Extraction (e.g. for corporate sites or OSB central contact)
                    general_contacts = extract_contacts_from_text(text_content, norm_curr_url)
                    if website.company_id:
                        for ct in general_contacts:
                            ex_ct = db.query(Contact).filter(
                                Contact.company_id == website.company_id,
                                Contact.contact_type == ct["contact_type"],
                                Contact.value == ct["value"]
                            ).first()
                            if not ex_ct:
                                new_ct = Contact(
                                    company_id=website.company_id,
                                    contact_type=ct["contact_type"],
                                    value=ct["value"],
                                    label=ct["label"],
                                    confidence_score=ct["confidence_score"],
                                    source_url=norm_curr_url,
                                    is_verified=False,
                                    is_public=True
                                )
                                db.add(new_ct)
                                contacts_discovered += 1

                    # 3. Discover internal links for directory, member lists, and contacts
                    domain_root = normalize_domain(website.base_url)
                    for a in soup.find_all("a", href=True):
                        link_url = normalize_url(a["href"], norm_curr_url)
                        if link_url:
                            link_domain = normalize_domain(link_url)
                            if link_domain == domain_root and link_url not in visited_urls:
                                link_text = a.get_text(strip=True).lower()
                                link_path = urlparse(link_url).path.lower()

                                # Prioritize member directories and contact pages
                                is_high_priority = any(keyword in link_path or keyword in link_text for keyword in [
                                    "firma", "company", "uye", "member", "katilimci", "rehber", "directory",
                                    "iletisim", "contact", "hakkimizda", "about"
                                ])

                                ptype = "directory" if any(k in link_path for k in ["firma", "uye", "rehber"]) else "other"
                                if is_high_priority:
                                    to_visit.insert(0, (link_url, ptype))
                                elif len(to_visit) < 40:
                                    to_visit.append((link_url, "other"))

                except Exception as page_err:
                    logger.warning(f"Error crawling page {curr_url}: {page_err}")
                    continue

        # Complete status
        website.status = "completed"
        website.last_success_at = datetime.utcnow()
        website.http_status = http_status_code or 200
        website.error_message = None
        db.commit()

    except Exception as e:
        logger.error(f"Scraping failed for website {website_id}: {e}")
        error_message = str(e)
        website.status = "failed"
        website.error_message = error_message
        website.http_status = http_status_code
        website.retry_count += 1
        db.commit()

    return {
        "website_id": website.id,
        "domain": website.domain,
        "status": website.status,
        "pages_scraped": pages_scraped,
        "companies_discovered": companies_discovered,
        "contacts_discovered": contacts_discovered,
        "error": error_message
    }
