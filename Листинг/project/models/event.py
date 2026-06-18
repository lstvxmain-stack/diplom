from datetime import datetime
from project import db


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime)
    time = db.Column(db.String(50))
    price = db.Column(db.String(100))
    age_rating = db.Column(db.String(10))
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    source_url = db.Column(db.String(500))
    organizer_url = db.Column(db.String(500))
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    venue = db.relationship("Venue", back_populates="events", lazy="joined")
    category = db.relationship("Category", back_populates="events", lazy="joined")

    def __repr__(self):
        return self.title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date_start": self.date_start.isoformat() if self.date_start else None,
            "date_end": self.date_end.isoformat() if self.date_end else None,
            "time": self.time,
            "price": self.price,
            "age_rating": self.age_rating,
            "venue_id": self.venue_id,
            "venue_name": self.venue.name if self.venue else "",
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else "",
            "category_color": self.category.color if self.category else "#3388ff",
            "source_url": self.source_url,
            "organizer_url": self.organizer_url,
            "image_url": self.image_url,
        }
