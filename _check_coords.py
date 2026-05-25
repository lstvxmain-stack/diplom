import requests
r = requests.get('https://diplom-sfq0.onrender.com/api/map-data', timeout=30)
data = r.json()
print('Total:', len(data))
for v in data[:5]:
    print(f'  name={v["name"][:30]:30s} lat={v["latitude"]} lng={v["longitude"]}')
null_coords = [v for v in data if not v.get('latitude') or not v.get('longitude')]
print(f'Null coords: {len(null_coords)}')
