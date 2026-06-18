"""Import all venues from cultreg.ru API into the database."""
import json, time, urllib.request, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from project import create_app, db
from project.models.venue import Venue
from project.models.category import Category

API_BASE = "https://bel.cultreg.ru/api/1.0/places"
LIMIT = 100

# Map cultreg category sysName → our category_id
CATEGORY_MAP = {
    "teatry": 1,
    "kinoteatry": 2,
    "koncertnye-ploshchadki": 3,
    "muzei": 7,
    "dvorcy-kultury-i-kluby": 6,
    "sport": 5,
    "biblioteki": 9,
    "parki": 10,
    "zooparki": 10,
    "zapovedniki": 10,
    "katki": 5,
    "bazy-otdykha": 10,
}

# District mapping from city names
DISTRICT_MAP = {
    "Алексеевка": "Алексеевский",
    "Белгород": "Белгород",
    "Борисовка": "Борисовский",
    "Валуйки": "Валуйский",
    "Вейделевка": "Вейделевский",
    "Волоконовка": "Волоконовский",
    "Грайворон": "Грайворонский",
    "Губкин": "Губкинский",
    "Ивня": "Ивнянский",
    "Короча": "Корочанский",
    "Красное": "Красненский",
    "Бирюч": "Красногвардейский",
    "Красная Яруга": "Краснояружский",
    "Новый Оскол": "Новооскольский",
    "Прохоровка": "Прохоровский",
    "Ракитное": "Ракитянский",
    "Ровеньки": "Ровеньский",
    "Старый Оскол": "Старооскольский",
    "Чернянка": "Чернянский",
    "Шебекино": "Шебекинский",
    "Строитель": "Яковлевский",
}

def fmt_addr(addr):
    """Format address from API object."""
    parts = []
    city = addr.get("city", {}).get("name", "")
    street = addr.get("street", {}).get("name", "")
    stype = addr.get("street", {}).get("type", "")
    house = addr.get("house", {}).get("name", "")
    comment = addr.get("comment", "")
    if city:
        parts.append(f"г. {city}")
    if street and stype:
        type_map = {"ул": "ул.", "пр-кт": "просп.", "б-р": "бул.", "пер": "пер.", "пл": "пл."}
        parts.append(f"{type_map.get(stype, stype+'')} {street}")
    elif street:
        parts.append(f"ул. {street}")
    if house:
        parts.append(f", {house}")
    if comment:
        parts.append(f" ({comment})")
    return " ".join(parts)

def get_district(city_name):
    """Map city name to district."""
    for key, value in DISTRICT_MAP.items():
        if key.lower() in city_name.lower():
            return value
    return city_name

def fetch_all():
    app = create_app()
    with app.app_context():
        # Build category map from database
        cats = Category.query.all()
        our_cats = {c.id: c.name for c in cats}
        print(f"Found {Category.query.count()} categories in DB")
        for c in cats:
            print(f"  {c.id}: {c.name}")

        existing_names = {v.name for v in Venue.query.all()}
        print(f"Existing venues: {len(existing_names)}")

        offset = 0
        total_api = None
        added = 0
        skipped_dup = 0
        skipped_cat = 0
        errors = 0

        while True:
            url = f"{API_BASE}?offset={offset}&limit={LIMIT}"
            req = urllib.request.Request(url, headers={"User-Agent": "BelgorodMap/3.0"})
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode())
            except Exception as e:
                print(f"Error at offset {offset}: {e}")
                errors += 1
                if errors > 3:
                    break
                time.sleep(5)
                continue

            places = data.get("places", [])
            total_api = data.get("total", 0)
            if not places:
                break

            for p in places:
                name = p.get("name", "").strip()
                if not name or name in existing_names:
                    skipped_dup += 1
                    continue

                cat = p.get("category") or {}
                cat_sysname = cat.get("sysName", "")
                our_cat_id = CATEGORY_MAP.get(cat_sysname)
                if our_cat_id is None:
                    skipped_cat += 1
                    continue

                addr_obj = p.get("address", {})
                address = fmt_addr(addr_obj)
                city_name = addr_obj.get("city", {}).get("name", "")
                district = get_district(city_name)

                map_pos = p.get("mapPosition", {})
                coords = map_pos.get("coordinates", [])
                if len(coords) >= 2:
                    lat, lon = coords[0], coords[1]
                else:
                    lat, lon = 0, 0

                phone = ""
                contacts = p.get("contacts", [])
                for c in contacts:
                    if c.get("type") == "phone":
                        phone = "+7 " + c.get("phone", "")
                        break

                website = ""
                for c in contacts:
                    if c.get("type") == "website":
                        website = c.get("website", "")
                        break

                venue = Venue(
                    name=name,
                    address=address,
                    latitude=lat,
                    longitude=lon,
                    phone=phone,
                    website=website,
                    description=p.get("description", ""),
                    district=district,
                    category_id=our_cat_id,
                    source_url=f"https://bel.cultreg.ru/places/{p['_id']}",
                    image_url="",
                )
                db.session.add(venue)
                existing_names.add(name)
                added += 1

            db.session.commit()
            offset += LIMIT
            errors = 0
            print(f"  Fetched {offset}/{total_api}, added so far: {added}")

            if offset >= total_api:
                break
            time.sleep(0.3)

        db.session.commit()
        final_count = Venue.query.count()
        print(f"\nDone! Total venues in DB: {final_count}")
        print(f"  Added: {added}")
        print(f"  Skipped (dup name): {skipped_dup}")
        print(f"  Skipped (category): {skipped_cat}")

if __name__ == "__main__":
    fetch_all()
