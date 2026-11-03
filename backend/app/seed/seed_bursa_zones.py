from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.industrial_zone import IndustrialZone
from app.models.website import Website

BURSA_OSB_SEED_DATA: List[Dict[str, Any]] = [
    {
        "name": "Bursa Organize Sanayi Bölgesi (Bursa OSB)",
        "slug": "bursa-osb",
        "province": "Bursa",
        "district": "Nilüfer / Osmangazi",
        "official_website": "https://bosb.org.tr",
        "portal_type": "osb_directory",
        "description": "Türkiye'nin ilk organize sanayi bölgesi (1961). Otomotiv, tekstil, makine ve metal sektörlerinde öncü dev sanayi kuruluşlarını barındırır.",
        "domain": "bosb.org.tr"
    },
    {
        "name": "Demirtaş Organize Sanayi Bölgesi (DOSAB)",
        "slug": "dosab",
        "province": "Bursa",
        "district": "Osmangazi",
        "official_website": "https://dosab.org.tr",
        "portal_type": "osb_directory",
        "description": "Tekstil, otomotiv yan sanayi ve kimya sektörlerinde Türkiye'nin en büyük üretim ve ihracat merkezlerinden biri.",
        "domain": "dosab.org.tr"
    },
    {
        "name": "Nilüfer Organize Sanayi Bölgesi (NOSAB)",
        "slug": "nosab",
        "province": "Bursa",
        "district": "Nilüfer",
        "official_website": "https://nosab.org.tr",
        "portal_type": "osb_directory",
        "description": "Makine, kalıpçılık, plastik ve otomotiv yan sanayinde yüksek katma değerli üretim gerçekleştiren modern sanayi bölgesi.",
        "domain": "nosab.org.tr"
    },
    {
        "name": "Hasanağa Organize Sanayi Bölgesi (HOSAB)",
        "slug": "hasanaga-osb",
        "province": "Bursa",
        "district": "Nilüfer",
        "official_website": "https://hosab.org.tr",
        "portal_type": "osb_directory",
        "description": "Otomotiv sanayi, metal işleme ve kauçuk sektörlerinde uzmanlaşmış hızla büyüyen ihtisas sanayi bölgesi.",
        "domain": "hosab.org.tr"
    },
    {
        "name": "Kayapa Organize Sanayi Bölgesi",
        "slug": "kayapa-osb",
        "province": "Bursa",
        "district": "Nilüfer",
        "official_website": "https://kayapaosb.org.tr",
        "portal_type": "osb_directory",
        "description": "Gelişmiş altyapısıyla makine, elektrik-elektronik, geri dönüşüm ve otomotiv parça üretimi.",
        "domain": "kayapaosb.org.tr"
    },
    {
        "name": "İnegöl Organize Sanayi Bölgesi",
        "slug": "inegol-osb",
        "province": "Bursa",
        "district": "İnegöl",
        "official_website": "https://inegolosb.org.tr",
        "portal_type": "osb_directory",
        "description": "Türkiye'nin mobilya ve orman ürünleri başkenti; ayrıca tekstil ve kimya üretim üssü.",
        "domain": "inegolosb.org.tr"
    },
    {
        "name": "Bursa Teknoloji Organize Sanayi Bölgesi (TEKNOSAB)",
        "slug": "teknosab",
        "province": "Bursa",
        "district": "Karacabey",
        "official_website": "https://teknosab.org.tr",
        "portal_type": "osb_directory",
        "description": "Sanayi 4.0, yüksek teknoloji, yapay zekâ, nanoteknoloji ve biyoteknoloji odaklı Türkiye'nin mega teknoloji OSB'si.",
        "domain": "teknosab.org.tr"
    },
    {
        "name": "Bursa İhtisas Deri ve Karma Organize Sanayi Bölgesi",
        "slug": "bursa-deri-osb",
        "province": "Bursa",
        "district": "Nilüfer",
        "official_website": "https://deriosb.org.tr",
        "portal_type": "osb_directory",
        "description": "Badırga mevkiinde deri sanayi, kimya ve ileri arıtma teknolojilerine sahip ihtisas bölgesi.",
        "domain": "deriosb.org.tr"
    },
    {
        "name": "Barakfakih Organize Sanayi Bölgesi",
        "slug": "barakfakih-osb",
        "province": "Bursa",
        "district": "Kestel",
        "official_website": "https://barakfakihosb.org.tr",
        "portal_type": "osb_directory",
        "description": "Tekstil terbiye, metal işleme, döküm ve kimya tesislerinin yer aldığı sanayi kümelenmesi.",
        "domain": "barakfakihosb.org.tr"
    },
    {
        "name": "Kestel Organize Sanayi Bölgesi",
        "slug": "kestel-osb",
        "province": "Bursa",
        "district": "Kestel",
        "official_website": "https://kestelosb.org.tr",
        "portal_type": "osb_directory",
        "description": "Tekstil sanayi, dokuma, iplik ve boyahane tesisleri ile metal sanayi kümelenmesi.",
        "domain": "kestelosb.org.tr"
    },
    {
        "name": "Gürsu Organize Sanayi Bölgesi",
        "slug": "gursu-osb",
        "province": "Bursa",
        "district": "Gürsu",
        "official_website": "https://gursuosb.org.tr",
        "portal_type": "osb_directory",
        "description": "Bursa doğu aksında dokuma, konfeksiyon ve metal mamul imalatı yapan sanayi tesisleri.",
        "domain": "gursuosb.org.tr"
    },
    {
        "name": "Mustafakemalpaşa Organize Sanayi Bölgesi",
        "slug": "mkp-osb",
        "province": "Bursa",
        "district": "Mustafakemalpaşa",
        "official_website": "https://mkposb.org.tr",
        "portal_type": "osb_directory",
        "description": "Gıda sanayi, tarım makineleri, ambalaj ve inşaat malzemeleri üretimi.",
        "domain": "mkposb.org.tr"
    }
]


def seed_bursa_industrial_zones(db: Session) -> int:
    """
    Seeds initial Bursa industrial zones and their portal websites.
    Safe to run repeatedly; does not recreate existing zones.
    """
    seeded_count = 0
    for item in BURSA_OSB_SEED_DATA:
        existing = db.query(IndustrialZone).filter(IndustrialZone.slug == item["slug"]).first()
        if not existing:
            zone = IndustrialZone(
                name=item["name"],
                slug=item["slug"],
                province=item["province"],
                district=item["district"],
                official_website=item["official_website"],
                portal_type=item["portal_type"],
                description=item["description"],
                is_active=True
            )
            db.add(zone)
            db.flush()

            # Create corresponding website entry in website registry
            website = Website(
                zone_id=zone.id,
                domain=item["domain"],
                base_url=item["official_website"],
                status="pending",
                crawl_mode="new_only",
                crawl_delay=2.0,
                robots_allowed=True
            )
            db.add(website)
            seeded_count += 1

    db.commit()
    return seeded_count
