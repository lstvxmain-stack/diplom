import os
from project import create_app, db
from project.models.admin import AdminUser
from project.models.category import Category
from project.models.venue import Venue

app = create_app()

with app.app_context():
    os.makedirs(os.path.join(app.root_path, '..', 'data'), exist_ok=True)
    db.create_all()
    if not AdminUser.query.first():
        admin = AdminUser(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)
    if not Category.query.first():
        categories = [
            Category(name="Театры", icon="fas fa-theater-masks", color="#e74c3c", sort_order=1),
            Category(name="Кинотеатры", icon="fas fa-film", color="#3498db", sort_order=2),
            Category(name="Концертные залы", icon="fas fa-music", color="#2ecc71", sort_order=3),
            Category(name="Филармонии", icon="fas fa-violin", color="#9b59b6", sort_order=4),
            Category(name="Стадионы и спорткомплексы", icon="fas fa-futbol", color="#f39c12", sort_order=5),
            Category(name="Дворцы культуры и клубы", icon="fas fa-landmark", color="#1abc9c", sort_order=6),
            Category(name="Музеи и выставки", icon="fas fa-palette", color="#e67e22", sort_order=7),
            Category(name="Фестивали и городские мероприятия", icon="fas fa-star", color="#e91e63", sort_order=8),
            Category(name="Библиотеки", icon="fas fa-book", color="#795548", sort_order=9),
            Category(name="Парки и зоны отдыха", icon="fas fa-tree", color="#4caf50", sort_order=10),
        ]
        db.session.add_all(categories)
    if not Venue.query.first():
        import json
        seed_path = os.path.join(app.root_path, '..', 'data', 'seed_venues.json')
        with open(seed_path, 'r', encoding='utf-8') as f:
            venues_data = json.load(f)
        for vd in venues_data:
            venue = Venue(**vd)
            db.session.add(venue)
    db.session.commit()

if __name__ == "__main__":
    app.run()
