"""Final coordinate verification using geopy with Nominatim."""
import json, time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="BelgorodMap/1.0")

places = [
    ("Белгородский академический драматический театр им. Щепкина", "Соборная площадь, 1, Белгород"),
    ("Белгородский государственный театр кукол", "улица Н. Чумичова, 100, Белгород"),
    ("Кинотеатр Победа", "улица Щорса, 64, Белгород"),
    ("Кинотеатр Радуга", "улица Шершнёва, 6, Белгород"),
    ("Белгородская государственная филармония", "улица Преображенская, 42, Белгород"),
    ("Концертный зал БГИИК", "улица Королёва, 7, Белгород"),
    ("Белгород Арена", "улица Мичурина, 39, Белгород"),
    ("Стадион Салют", "улица Победы, 79, Белгород"),
    ("Дворец культуры Энергомаш", "проспект Богдана Хмельницкого, 111, Белгород"),
    ("Культурный центр Октябрь", "улица Н. Чумичова, 124, Белгород"),
    ("Дворец культуры Комсомольский", "улица Дзержинского, 15, Губкин"),
    ("Старооскольский театр для детей и молодёжи", "улица Ленина, 18, Старый Оскол"),
    ("Кинотеатр Быль", "микрорайон Ольминского, 6, Старый Оскол"),
    ("ДК Горняк", "улица Ленина, 53, Шебекино"),
    ("Валуйский историко-художественный музей", "улица Ленина, 10, Валуйки"),
    ("Алексеевский краеведческий музей", "площадь Победы, 56, Алексеевка"),
]

results = []
for name, address in places:
    full = f"{address}, Белгородская область, Россия"
    try:
        location = geolocator.geocode(full, timeout=10, language="ru")
        if location:
            lat = round(location.latitude, 4)
            lon = round(location.longitude, 4)
            addr = location.address[:100] if location.address else ""
            results.append({"name": name, "lat": lat, "lon": lon, "found": addr})
        else:
            results.append({"name": name, "lat": None, "lon": None, "found": "NOT FOUND"})
    except Exception as e:
        results.append({"name": name, "lat": None, "lon": None, "found": f"ERROR: {e}"})
    time.sleep(1.1)

print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
