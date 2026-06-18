"""Parser for culture.ru Open API."""
import requests
from project.parsers.base import BaseParser, ParsedVenue, ParsedEvent


class CultureRFParser(BaseParser):
    name = "culture.ru"

    EVENTS_API = "https://www.culture.ru/api/events"
    BELGOROD_ORG_IDS = {
        24731,  # Белгородская филармония
        24732,  # Белгородский драмтеатр
        24733,  # Белгородский театр кукол
    }

    def parse_venues(self) -> list[ParsedVenue]:
        venues = []
        seen = set()
        try:
            events = self._fetch_events()
            for item in events:
                orgs = item.get("organizations", []) or []
                for org in orgs:
                    name = org.get("title", "").strip()
                    if not name or name in seen:
                        continue
                    seen.add(name)
                    venue = ParsedVenue(
                        name=name,
                        address=org.get("address"),
                        latitude=org.get("lat"),
                        longitude=org.get("lon"),
                        category_name="",
                    )
                    venues.append(venue)
        except Exception as e:
            print(f"[{self.name}] Error parsing venues: {e}")
        return venues

    def parse_events(self) -> list[ParsedEvent]:
        events = []
        try:
            data = self._fetch_events()
            for item in data:
                title = item.get("title", "").strip()
                if not title:
                    continue

                org_name = ""
                orgs = item.get("organizations", []) or []
                if orgs:
                    org_name = orgs[0].get("title", "")

                seance = None
                seances = item.get("seances", []) or []
                if seances:
                    seance = seances[0]

                event = ParsedEvent(
                    title=title,
                    description=item.get("shortText") or item.get("text", ""),
                    date_start=item.get("startDate") or (seance or {}).get("startDate"),
                    date_end=item.get("endDate"),
                    price=item.get("price") or item.get("priceMin"),
                    age_rating=item.get("ageRestriction", ""),
                    venue_name=org_name,
                    source_url=f"https://www.culture.ru/events/{item.get('_id', '')}",
                    image_url=f"https://www.culture.ru/{item.get('thumbnailFileId', '')}" if item.get("thumbnailFileId") else None,
                )
                events.append(event)
        except Exception as e:
            print(f"[{self.name}] Error parsing events: {e}")
        return events

    def _fetch_events(self) -> list[dict]:
        all_items = []
        page = 1
        while True:
            try:
                resp = requests.get(self.EVENTS_API, params={"page": page, "limit": 50}, timeout=15)
                if not resp.ok:
                    break
                data = resp.json()
                items = data.get("items", [])
                if not items:
                    break
                all_items.extend(items)
                total = data.get("total", 0)
                if len(all_items) >= total or len(items) < 50:
                    break
                page += 1
            except Exception as e:
                print(f"[{self.name}] Fetch error: {e}")
                break
        return all_items
