"""Fix missing/problematic venues with more precise queries."""
import json, time, requests

# Try more specific queries for the ones that failed or seem off
queries = [
    ("Белгородский государственный театр кукол", "Белгородский театр кукол Чумичова 100"),
    ("Культурный центр Октябрь", "культурный центр Октябрь Белгород"),
    ("Стадион Салют Белгород", "стадион Салют Белгород Победы 79"),
    ("Белгород Арена", "Белгород Арена Мичурина 39"),
    ("Кинотеатр Победа Белгород", "кинотеатр Победа Белгород Щорса 64"),
]

print(json.dumps({"results": []}))
results = []
for name, query in queries:
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": f"{query}, Россия", "format": "json", "limit": 1},
            headers={"User-Agent": "BelgorodMap/1.0"},
            timeout=10,
        )
        data = resp.json()
        if data:
            lat = round(float(data[0]["lat"]), 4)
            lon = round(float(data[0]["lon"]), 4)
            display = data[0].get("display_name", "")[:120]
            results.append({"name": name, "lat": lat, "lon": lon, "display": display})
        else:
            results.append({"name": name, "lat": None, "lon": None, "display": "NOT FOUND"})
    except Exception as e:
        results.append({"name": name, "lat": None, "lon": None, "display": str(e)})
    time.sleep(1)

print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
