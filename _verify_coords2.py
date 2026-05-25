"""Verify coordinates using Nominatim with simple queries."""
import json, time, requests, sys

# Use direct venue names/cities for better geocoding
queries = [
    ("Белгородский академический драматический театр им. М.С. Щепкина", "Соборная площадь 1 Белгород"),
    ("Белгородский государственный театр кукол", "улица Н. Чумичова 100 Белгород"),
    ("Кинотеатр Победа", "улица Щорса 64 Белгород"),
    ("Кинотеатр Радуга", "улица Шершнёва 6 Белгород"),
    ("Белгородская государственная филармония", "улица Преображенская 42 Белгород"),
    ("Концертный зал БГИИК", "улица Королёва 7 Белгород"),
    ("Белгород Арена", "улица Мичурина 39 Белгород"),
    ("Стадион Салют", "улица Победы 79 Белгород"),
    ("Дворец культуры Энергомаш", "проспект Богдана Хмельницкого 111 Белгород"),
    ("Культурный центр Октябрь", "улица Н. Чумичова 124 Белгород"),
    ("Дворец культуры Комсомольский", "улица Дзержинского 15 Губкин"),
    ("Старооскольский театр для детей и молодёжи", "улица Ленина 18 Старый Оскол"),
    ("Кинотеатр Быль", "микрорайон Ольминского 6 Старый Оскол"),
    ("ДК Горняк", "улица Ленина 53 Шебекино"),
    ("Валуйский историко-художественный музей", "улица Ленина 10 Валуйки"),
    ("Алексеевский краеведческий музей", "площадь Победы 56 Алексеевка"),
]

print(json.dumps({"results": []}))
results = []
for name, query in queries:
    full_query = f"{query}, Белгородская область, Россия"
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": full_query, "format": "json", "limit": 1},
            headers={"User-Agent": "BelgorodMap/1.0"},
            timeout=10,
        )
        data = resp.json()
        if data:
            lat = round(float(data[0]["lat"]), 4)
            lon = round(float(data[0]["lon"]), 4)
            results.append({"name": name, "lat": lat, "lon": lon, "status": "ok"})
        else:
            results.append({"name": name, "lat": None, "lon": None, "status": "not_found"})
    except Exception as e:
        results.append({"name": name, "lat": None, "lon": None, "status": str(e)})
    time.sleep(1)

print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
