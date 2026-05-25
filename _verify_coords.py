"""Verify and fix venue coordinates using Nominatim geocoding."""
import json
import time
import requests

venues_data = [
    {"name": "Белгородский академический драматический театр им. М.С. Щепкина", "address": "г. Белгород, Соборная пл., 1"},
    {"name": "Белгородский государственный театр кукол", "address": "г. Белгород, ул. Н. Чумичова, 100"},
    {"name": "Кинотеатр «Победа»", "address": "г. Белгород, ул. Щорса, 64"},
    {"name": "Кинотеатр «Радуга»", "address": "г. Белгород, ул. Шершнёва, 6"},
    {"name": "Белгородская государственная филармония", "address": "г. Белгород, ул. Преображенская, 42"},
    {"name": "Концертный зал Белгородского института искусств и культуры", "address": "г. Белгород, ул. Королёва, 7"},
    {"name": "«Белгород Арена»", "address": "г. Белгород, ул. Мичурина, 39"},
    {"name": "Стадион «Салют»", "address": "г. Белгород, ул. Победы, 79"},
    {"name": "Дворец культуры «Энергомаш»", "address": "г. Белгород, просп. Б. Хмельницкого, 111"},
    {"name": "Культурный центр «Октябрь»", "address": "г. Белгород, ул. Н. Чумичова, 124"},
    {"name": "Дворец культуры «Комсомольский»", "address": "г. Губкин, ул. Дзержинского, 15"},
    {"name": "Старооскольский театр для детей и молодёжи", "address": "г. Старый Оскол, ул. Ленина, 18"},
    {"name": "Кинотеатр «Быль»", "address": "г. Старый Оскол, микрорайон Ольминского, 6"},
    {"name": "ДК «Горняк»", "address": "г. Шебекино, ул. Ленина, 53"},
    {"name": "Валуйский историко-художественный музей", "address": "г. Валуйки, ул. Ленина, 10"},
    {"name": "Алексеевский краеведческий музей", "address": "г. Алексеевка, пл. Победы, 56"},
]

results = []
for v in venues_data:
    query = f"{v['address']}, Белгородская область, Россия"
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": query, "format": "json", "limit": 1, "accept-language": "ru"},
            headers={"User-Agent": "BelgorodCulturalMap/1.0"},
            timeout=10,
        )
        data = resp.json()
        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            display = data[0].get("display_name", "")[:100]
            results.append((v["name"], v["address"], lat, lon, "OK", display))
        else:
            results.append((v["name"], v["address"], None, None, "NOT FOUND", ""))
    except Exception as e:
        results.append((v["name"], v["address"], None, None, f"ERROR: {e}", ""))
    time.sleep(1)  # Respect Nominatim rate limit

print("\n=== VERIFIED COORDINATES ===\n")
for name, addr, lat, lon, status, display in results:
    print(f"{name}")
    print(f"  Адрес: {addr}")
    if lat:
        print(f"  Координаты: {lat:.4f}, {lon:.4f}")
    print(f"  Статус: {status}")
    if display:
        print(f"  Найдено: {display}")
    print()
