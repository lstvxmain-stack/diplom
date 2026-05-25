from flask import Blueprint, jsonify, request
from project.models.venue import Venue
from project.models.event import Event
from project.models.category import Category
from datetime import datetime
from project import db

api_bp = Blueprint("api", __name__)


@api_bp.route("/map-data")
def map_data():
    category_id = request.args.get("category_id", type=int)
    district = request.args.get("district")
    search = request.args.get("search")

    venue_query = Venue.query

    if category_id:
        venue_query = venue_query.filter_by(category_id=category_id)
    if district:
        venue_query = venue_query.filter_by(district=district)
    if search:
        venue_query = venue_query.filter(Venue.name.ilike(f"%{search}%"))

    venues = venue_query.all()

    now = datetime.now()
    result = []
    for venue in venues:
        upcoming = (
            Event.query.filter_by(venue_id=venue.id)
            .filter(Event.date_start >= now)
            .order_by(Event.date_start)
            .limit(5)
            .all()
        )
        venue_dict = venue.to_dict()
        venue_dict["upcoming_events"] = [e.to_dict() for e in upcoming]
        result.append(venue_dict)

    return jsonify(result)


@api_bp.route("/categories")
def categories():
    cats = Category.query.order_by(Category.sort_order).all()
    return jsonify([{"id": c.id, "name": c.name, "color": c.color, "icon": c.icon} for c in cats])


@api_bp.route("/districts")
def districts():
    result = (
        db.session.query(Venue.district)
        .filter(Venue.district.isnot(None))
        .distinct()
        .order_by(Venue.district)
        .all()
    )
    return jsonify([d[0] for d in result if d[0]])
