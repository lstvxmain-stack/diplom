"""Parser manager - orchestrates all parsers and saves to database."""
from datetime import datetime
from project import db
from project.models.category import Category
from project.models.venue import Venue
from project.models.event import Event


class ParserManager:
    def __init__(self, parsers=None):
        self.parsers = parsers or []

    def add_parser(self, parser):
        self.parsers.append(parser)

    def run_all(self, app):
        """Run all parsers and save results to database."""
        total_venues = 0
        total_events = 0

        with app.app_context():
            category_map = {c.name.lower(): c for c in Category.query.all()}
            default_cat = Category.query.first()
            existing_venue_names = {v.name: v for v in Venue.query.all()}
            existing_event_titles = {(e.title, e.venue_id): e for e in Event.query.all()}

            for parser in self.parsers:
                print(f"[{parser.name}] Starting...")

                try:
                    parsed_venues = parser.parse_venues()
                    for pv in parsed_venues:
                        if not pv.name or pv.name in existing_venue_names:
                            continue
                        cat = None
                        if pv.category_name and pv.category_name.lower() in category_map:
                            cat = category_map[pv.category_name.lower()]
                        elif default_cat:
                            cat = default_cat

                        venue = Venue(
                            name=pv.name,
                            address=pv.address,
                            latitude=pv.latitude or 0,
                            longitude=pv.longitude or 0,
                            phone=pv.phone,
                            website=pv.website,
                            description=pv.description,
                            image_url=pv.image_url,
                            district=pv.district,
                            category_id=cat.id if cat else default_cat.id,
                            source_url=pv.source_url,
                        )
                        db.session.add(venue)
                        db.session.flush()
                        existing_venue_names[pv.name] = venue
                        total_venues += 1
                except Exception as e:
                    print(f"[{parser.name}] Error in venues: {e}")

                try:
                    parsed_events = parser.parse_events()
                    for pe in parsed_events:
                        venue = existing_venue_names.get(pe.venue_name or "")
                        if not venue:
                            continue

                        key = (pe.title, venue.id)
                        if key in existing_event_titles:
                            continue

                        cat = None
                        if pe.category_name and pe.category_name.lower() in category_map:
                            cat = category_map[pe.category_name.lower()]
                        elif default_cat:
                            cat = default_cat

                        date_start = None
                        if pe.date_start:
                            try:
                                date_start = datetime.fromisoformat(pe.date_start)
                            except (ValueError, TypeError):
                                pass

                        date_end = None
                        if pe.date_end:
                            try:
                                date_end = datetime.fromisoformat(pe.date_end)
                            except (ValueError, TypeError):
                                pass

                        event = Event(
                            title=pe.title,
                            description=pe.description,
                            date_start=date_start or datetime.now(),
                            date_end=date_end,
                            time=pe.time,
                            price=pe.price,
                            age_rating=pe.age_rating,
                            venue_id=venue.id,
                            category_id=cat.id if cat else default_cat.id,
                            source_url=pe.source_url,
                            image_url=pe.image_url,
                        )
                        db.session.add(event)
                        existing_event_titles[key] = event
                        total_events += 1
                except Exception as e:
                    print(f"[{parser.name}] Error in events: {e}")

                print(f"[{parser.name}] Done. {len(parsed_venues)} venues, {len(parsed_events)} events")

            db.session.commit()
            print(f"Parser manager: saved {total_venues} venues, {total_events} events")
