"""Get full service details and try to debug deployment."""
import requests, json

key = 'rnd_fweT4Q4OPOe0L8XEMk6dL12sEGK5'
headers = {'Authorization': 'Bearer ' + key, 'Accept': 'application/json'}
sid = 'srv-d8a6vreq1p3s73a8f2ag'

# Full service details
r = requests.get(f'https://api.render.com/v1/services/{sid}', headers=headers, timeout=15)
print('Service details:')
print(json.dumps(r.json(), indent=2, ensure_ascii=False)[:3000])
