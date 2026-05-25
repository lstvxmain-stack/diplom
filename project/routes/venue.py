from flask import Blueprint, render_template, abort, request
from project.models.venue import Venue
from project.models.event import Event
from datetime import datetime

venue_bp = Blueprint("venues", __name__)


@venue_bp.route("/")
def list_venues():
    category_id = request.args.get("category_id", type=int)
    district = request.args.get("district")

    query = Venue.query

    if category_id:
        query = query.filter_by(category_id=category_id)
    if district:
        query = query.filter_by(district=district)

    venues = query.order_by(Venue.name).all()
    return render_template("venues_list.html", venues=venues)


@venue_bp.route("/<int:id>")
def detail(id):
    venue = Venue.query.get_or_404(id)
    events = (
        Event.query.filter_by(venue_id=id)
        .filter(Event.date_start >= datetime.now())
        .order_by(Event.date_start)
        .all()
    )
    return render_template("venue_detail.html", venue=venue, events=events)
