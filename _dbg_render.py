"""Debug Render API responses."""
import requests, json

key = 'rnd_fweT4Q4OPOe0L8XEMk6dL12sEGK5'
headers = {'Authorization': 'Bearer ' + key, 'Accept': 'application/json'}

r = requests.get('https://api.render.com/v1/owners', headers=headers)
print('Status:', r.status_code)
print('Response:', json.dumps(r.json(), indent=2, ensure_ascii=False)[:2000])
