import json
with open('data/seed_venues.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
bad = []
for v in data:
    name = v.get('name', '')
    for ch in ['$', '`', '<', '>', '&']:
        if ch in name:
            bad.append(name)
            break
print(f'Checked {len(data)} venues')
print(f'Bad names: {len(bad)}')
for b in bad[:10]:
    print(repr(b))
