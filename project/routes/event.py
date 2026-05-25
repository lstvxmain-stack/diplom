from flask import Blueprint, render_template, request
from project.models.event import Event
from project.models.venue import Venue
from project.models.category import Category
from datetime import datetime, timedelta

event_bp = Blueprint("events", __name__)


@event_bp.route("/")
def list_events():
    category_id = request.args.get("category_id", type=int)
    venue_id = request.args.get("venue_id", type=int)
    district = request.args.get("district")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    query = Event.query.filter(Event.date_start >= datetime.now())

    if category_id:
        query = query.filter_by(category_id=category_id)
    if venue_id:
        query = query.filter_by(venue_id=venue_id)
    if district:
        query = query.join(Venue).filter(Venue.district == district)
    if date_from:
        try:
            query = query.filter(
                Event.date_start >= datetime.strptime(date_from, "%Y-%m-%d")
            )
        except ValueError:
            pass
    if date_to:
        try:
            query = query.filter(
                Event.date_start <= datetime.strptime(date_to, "%Y-%m-%d") + timedelta(days=1)
            )
        except ValueError:
            pass

    events = query.order_by(Event.date_start).all()
    return render_template("events_list.html", events=events)


@event_bp.route("/<int:id>")
def detail(id):
    event = Event.query.get_or_404(id)
    return render_template("event_detail.html", event=event)
