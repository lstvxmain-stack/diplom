"""Check deploys and logs."""
import requests, json

key = 'rnd_fweT4Q4OPOe0L8XEMk6dL12sEGK5'
headers = {'Authorization': 'Bearer ' + key, 'Accept': 'application/json'}
sid = 'srv-d8a6vreq1p3s73a8f2ag'

# List deploys
r = requests.get(f'https://api.render.com/v1/services/{sid}/deploys?limit=5', headers=headers, timeout=15)
print('Deploys status:', r.status_code)
if r.status_code == 200:
    deploys = r.json()
    for d in deploys:
        dep = d.get('deploy', {})
        did = dep.get('id', '')
        status = dep.get('status', '?')
        created = dep.get('createdAt', '?')[:19] if dep.get('createdAt') else '?'
        print(f'  Deploy {did}: status={status} created={created}')
    
    # Get the latest failed deploy events
    latest = deploys[0].get('deploy', {})
    latest_id = latest.get('id', '')
    if latest_id:
        r2 = requests.get(f'https://api.render.com/v1/services/{sid}/deploys/{latest_id}/events', headers=headers, timeout=15)
        print(f'\nEvents for {latest_id}: status={r2.status_code}')
        if r2.status_code == 200:
            for e in r2.json()[:30]:
                print(f'  {e.get("type")}: {json.dumps(e.get("text", ""), ensure_ascii=False)[:300]}')
                if e.get('type') == 'build_error' or e.get('type') == 'command_error':
                    print(f'  *** BUILD ERROR ***')
        else:
            print(f'  Response: {r2.text[:500]}')
