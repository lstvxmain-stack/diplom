"""Improved import from cultreg.ru API with better district handling."""
import json, time, urllib.request, sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from project import create_app, db
from project.models.venue import Venue, Category

API = "https://bel.cultreg.ru/api/1.0/places"
LIMIT = 100

CAT_MAP = {
    "teatry": 1, "kinoteatry": 2, "koncertnye-ploshchadki": 3,
    "muzei": 7, "dvorcy-kultury-i-kluby": 6, "sport": 5,
    "biblioteki": 9, "parki": 10, "zooparki": 10, "zapovedniki": 10,
    "katki": 5, "bazy-otdykha": 10, "plyazh": 10, "priroda": 10,
}

CITY_DIST = {
    "Белгород": "Белгород", "Старый Оскол": "Старооскольский",
    "Губкин": "Губкинский", "Шебекино": "Шебекинский",
    "Новый Оскол": "Новооскольский", "Валуйки": "Валуйский",
    "Строитель": "Яковлевский", "Алексеевка": "Алексеевский",
    "Бирюч": "Красногвардейский", "Грайворон": "Грайворонский",
    "Короча": "Корочанский", "Борисовка": "Борисовский",
    "Волоконовка": "Волоконовский", "Ивня": "Ивнянский",
    "Красная Яруга": "Краснояружский", "Красное": "Красненский",
    "Прохоровка": "Прохоровский", "Ракитное": "Ракитянский",
    "Ровеньки": "Ровеньский", "Вейделевка": "Вейделевский",
    "Чернянка": "Чернянский",
}

def build_address(addr, locale_name):
    """Build address string from API address object + locale."""
    city = (addr.get("city") or {}).get("name", "")
    street = (addr.get("street") or {}).get("name", "")
    stype = (addr.get("street") or {}).get("type", "")
    house = (addr.get("house") or {}).get("name", "")
    comment = (addr.get("comment") or "")
    
    parts = []
    if not city and locale_name and locale_name not in ("Белгородская область", "РФ"):
        city = locale_name
    
    type_map = {"ул": "ул.", "пр-кт": "просп.", "б-р": "бул.", "пер": "пер.", "пл": "пл.", "ш": "ш."}
    
    has_any = bool(city or street or house)
    
    if city:
        parts.append(f"г. {city}")
    if street:
        st = type_map.get(stype, stype + " ") if stype else "ул. "
        parts.append(f"{st}{street}".rstrip())
    if house:
        parts.append(f", д. {house}")
    if comment:
        parts.append(f" ({comment})")
    
    result = " ".join(parts) if parts else ""
    return result

def guess_district(city_name, locale_name, address):
    """Guess district from available info."""
    for name in [city_name, locale_name]:
        if name in CITY_DIST:
            return CITY_DIST[name]
    # Check if address has city reference
    for cname, dist in CITY_DIST.items():
        if cname in address:
            return dist
    return ""

def fetch_all():
    app = create_app()
    with app.app_context():
        existing_names = {v.name for v in Venue.query.all()}
        old_count = len(existing_names)
        
        offset = 0
        added = 0
        skipped = 0
        
        while True:
            req = urllib.request.Request(f"{API}?offset={offset}&limit={LIMIT}",
                headers={"User-Agent": "BelgorodMap/4.0"})
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode())
            except Exception as e:
                print(f"Error at offset {offset}: {e}")
                time.sleep(5)
                continue
            
            places = data.get("places", [])
            total = data.get("total", 0)
            if not places:
                break
            
            for p in places:
                name = p.get("name", "").strip()
                if not name or name in existing_names:
                    skipped += 1
                    continue
                
                cat = p.get("category") or {}
                our_cat = CAT_MAP.get(cat.get("sysName", ""))
                if our_cat is None:
                    skipped += 1
                    continue
                
                addr_obj = p.get("address", {})
                loc_name = (p.get("locale") or {}).get("name", "")
                city_name = (addr_obj.get("city") or {}).get("name", "")
                
                address = build_address(addr_obj, loc_name)
                district = guess_district(city_name, loc_name, address)
                
                pos = (p.get("mapPosition") or {}).get("coordinates") or []
                lat, lon = (pos[0], pos[1]) if len(pos) >= 2 else (0, 0)
                
                phone = next((c.get("phone","") for c in p.get("contacts",[]) if c.get("type")=="phone"), "")
                if phone:
                    phone = "+7 " + phone
                website = next((c.get("website","") for c in p.get("contacts",[]) if c.get("type")=="website"), "")
                
                desc = ""
                for c in p.get("content", []):
                    if c.get("type") == "text":
                        text = re.sub(r"<[^>]+>", "", c.get("text",""))
                        desc = text[:500]
                        break
                
                venue = Venue(
                    name=name, address=address, latitude=lat, longitude=lon,
                    phone=phone, website=website, description=desc,
                    district=district, category_id=our_cat,
                    source_url=f"https://bel.cultreg.ru/places/{p['_id']}",
                )
                db.session.add(venue)
                existing_names.add(name)
                added += 1
            
            db.session.commit()
            offset += LIMIT
            print(f"  {offset}/{total} - added: {added}, skipped: {skipped}")
            if offset >= total:
                break
            time.sleep(0.3)
        
        final = Venue.query.count()
        print(f"\nDone! Total venues: {final}")
        print(f"  Added: {added} (was {old_count})")
        
        # Stats
        from collections import Counter
        dc = Counter()
        for v in Venue.query.all():
            dc[v.district or "(none)"] += 1
        print("\nDistrict distribution:")
        for d, c in sorted(dc.items(), key=lambda x: -x[1])[:15]:
            print(f"  {d}: {c}")

if __name__ == "__main__":
    fetch_all()
