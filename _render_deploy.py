"""Create Render web service."""
import requests, json, sys

key = 'rnd_fweT4Q4OPOe0L8XEMk6dL12sEGK5'
headers = {'Authorization': 'Bearer ' + key, 'Accept': 'application/json', 'Content-Type': 'application/json'}
owner_id = 'tea-d8a6q9r7uimc73a5apbg'

# Check if service exists
r = requests.get('https://api.render.com/v1/services', headers=headers, timeout=15)
for s in r.json():
    if s.get('service', {}).get('name') == 'diplom':
        sid = s['service']['id']
        url = s['service'].get('serviceDetails', {}).get('url', '')
        print('Service already exists!')
        print('ID:', sid)
        print('URL:', url)
        sys.exit(0)

# Create service
payload = {
    'type': 'web_service',
    'name': 'diplom',
    'ownerId': owner_id,
    'repo': 'https://github.com/lstvxmain-stack/diplom',
    'autoDeploy': 'yes',
    'branch': 'main',
    'serviceDetails': {
        'runtime': 'python',
        'plan': 'free',
        'region': 'frankfurt',
        'envSpecificDetails': {
            'buildCommand': 'pip install -r requirements.txt',
            'startCommand': 'gunicorn wsgi:app',
        },
    },
}

r2 = requests.post('https://api.render.com/v1/services', headers=headers, json=payload, timeout=30)
print('Status:', r2.status_code)
if r2.status_code == 201:
    data = r2.json()
    sid = data.get('service', {}).get('id')
    print('Service ID:', sid)
    print('Deploy ID:', data.get('deployId'))
    # Get service URL
    r3 = requests.get(f'https://api.render.com/v1/services/{sid}', headers=headers, timeout=15)
    if r3.status_code == 200:
        url = r3.json().get('service', {}).get('serviceDetails', {}).get('url', '')
        print('URL:', url)
    print('\nBuilding and deploying...')
else:
    print('Error:', r2.status_code, r2.text[:500])
