from flask import Blueprint, render_template, request
from project.models.venue import Venue
from project.models.category import Category
from project.models.event import Event
from datetime import datetime

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    categories = Category.query.order_by(Category.sort_order).all()
    districts = (
        db.session.query(Venue.district)
        .filter(Venue.district.isnot(None), Venue.district != "")
        .distinct()
        .order_by(Venue.district)
        .all()
    )
    return render_template(
        "index.html",
        categories=[{"id": c.id, "name": c.name, "color": c.color, "icon": c.icon} for c in categories],
        districts=[d[0] for d in districts],
    )


from project import db
