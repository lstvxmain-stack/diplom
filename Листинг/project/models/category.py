from project import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    icon = db.Column(db.String(50), default="fas fa-map-marker-alt")
    color = db.Column(db.String(7), default="#3388ff")
    sort_order = db.Column(db.Integer, default=0)

    venues = db.relationship("Venue", back_populates="category", lazy="dynamic")
    events = db.relationship("Event", back_populates="category", lazy="dynamic")

    def __repr__(self):
        return self.name
