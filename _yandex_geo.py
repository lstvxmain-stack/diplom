"""Use Yandex Maps geocoding for more accurate Russian addresses."""
import json, time, requests

# Yandex geocoder HTTP API (free, no key needed for limited use)
YANDEX_GEO = "https://geocode-maps.yandex.ru/1.x/"

addresses = [
    ("Драмтеатр Щепкина", "г Белгород, Соборная площадь, 1"),
    ("Театр кукол", "г Белгород, улица Н Чумичова, 100"),
    ("Кинотеатр Победа", "г Белгород, улица Щорса, 64"),
    ("Кинотеатр Радуга", "г Белгород, улица Шершнёва, 6"),
    ("Филармония", "г Белгород, улица Преображенская, 42"),
    ("Концертный зал БГИИК", "г Белгород, улица Королёва, 7"),
    ("Белгород Арена", "г Белгород, улица Мичурина, 39"),
    ("Стадион Салют", "г Белгород, улица Победы, 79"),
    ("ДК Энергомаш", "г Белгород, проспект Богдана Хмельницкого, 111"),
    ("КЦ Октябрь", "г Белгород, улица Н Чумичова, 124"),
    ("ДК Комсомольский", "г Губкин, улица Дзержинского, 15"),
    ("Старооскольский театр", "г Старый Оскол, улица Ленина, 18"),
    ("Кинотеатр Быль", "г Старый Оскол, микрорайон Ольминского, 6"),
    ("ДК Горняк", "г Шебекино, улица Ленина, 53"),
    ("Валуйский музей", "г Валуйки, улица Ленина, 10"),
    ("Алексеевский музей", "г Алексеевка, площадь Победы, 56"),
]

results = []
for name, addr in addresses:
    try:
        resp = requests.get(YANDEX_GEO, params={
            "format": "json",
            "geocode": addr,
            "results": 1,
        }, timeout=10)
        data = resp.json()
        geo_obj = data.get("response", {}).get("GeoObjectCollection", {}).get("featureMember", [])
        if geo_obj:
            pos = geo_obj[0].get("GeoObject", {}).get("Point", {}).get("pos", "")
            if pos:
                lon, lat = pos.split(" ")
                results.append({"name": name, "lat": round(float(lat), 4), "lon": round(float(lon), 4)})
            else:
                results.append({"name": name, "error": "no pos"})
        else:
            results.append({"name": name, "error": "not found"})
    except Exception as e:
        results.append({"name": name, "error": str(e)})
    time.sleep(0.5)

print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
