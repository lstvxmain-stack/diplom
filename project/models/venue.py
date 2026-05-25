from project import db


class Venue(db.Model):
    __tablename__ = "venues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(50))
    website = db.Column(db.String(300))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    district = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    source_url = db.Column(db.String(500))

    category = db.relationship("Category", back_populates="venues", lazy="joined")
    events = db.relationship("Event", back_populates="venue", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "phone": self.phone,
            "website": self.website,
            "description": self.description,
            "image_url": self.image_url,
            "district": self.district,
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else "",
            "category_color": self.category.color if self.category else "#3388ff",
            "source_url": self.source_url,
            "events_count": self.events.count(),
        }
