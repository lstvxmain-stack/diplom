import os
from datetime import datetime, timedelta
from project import create_app, db
from project.models.admin import AdminUser
from project.models.category import Category
from project.models.venue import Venue
from project.models.event import Event

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
        db.session.flush()
    if not Event.query.first():
        events_data = [
            {"title": "Спектакль «Горе от ума»", "description": "Бессмертная комедия А.С. Грибоедова на сцене драмтеатра.", "date_start": datetime.now() + timedelta(days=7), "time": "18:30", "price": "400-1200 руб", "age_rating": "12+", "venue_name": "Белгородский академический драматический театр им. М.С. Щепкина", "category_id": 1, "source_url": "https://beltheatre.ru"},
            {"title": "Концерт симфонического оркестра", "description": "В программе: Чайковский, Рахманинов, Прокофьев.", "date_start": datetime.now() + timedelta(days=3), "time": "19:00", "price": "500-1500 руб", "age_rating": "6+", "venue_name": "Белгородская государственная филармония", "category_id": 4, "source_url": "https://belfilarm.ru"},
            {"title": "Мюзикл «Принцесса на горошине»", "description": "Кукольный спектакль для всей семьи.", "date_start": datetime.now() + timedelta(days=5), "time": "11:00", "price": "300 руб", "age_rating": "0+", "venue_name": "Белгородский государственный театр кукол", "category_id": 1, "source_url": "https://bgtk.org"},
            {"title": "Фестиваль «Белгородское лето»", "description": "Городской фестиваль с концертной программой и мастер-классами.", "date_start": datetime.now() + timedelta(days=14), "date_end": datetime.now() + timedelta(days=16), "time": "12:00", "price": "Бесплатно", "age_rating": "0+", "venue_name": "Дворец культуры «Энергомаш»", "category_id": 8},
            {"title": "Матч по футболу. Салют — Металлург", "description": "Футбольный матч в рамках первенства России.", "date_start": datetime.now() + timedelta(days=10), "time": "16:00", "price": "100-300 руб", "age_rating": "6+", "venue_name": "Стадион «Салют»", "category_id": 5},
            {"title": "Премьера фильма", "description": "Премьера нового российского фильма.", "date_start": datetime.now() + timedelta(days=2), "time": "10:00-23:00", "price": "200-400 руб", "age_rating": "12+", "venue_name": "Кинотеатр «Победа»", "category_id": 2},
            {"title": "Концерт группы «Radio Tapok»", "description": "Рок-концерт на Белгород Арене.", "date_start": datetime.now() + timedelta(days=20), "time": "20:00", "price": "800-2000 руб", "age_rating": "16+", "venue_name": "«Белгород Арена»", "category_id": 5},
            {"title": "Выставка «Белгород в живописи»", "description": "Выставка работ белгородских художников.", "date_start": datetime.now() + timedelta(days=1), "date_end": datetime.now() + timedelta(days=30), "price": "100 руб", "age_rating": "0+", "venue_name": "Валуйский историко-художественный музей", "category_id": 7},
            {"title": "Концерт органной музыки", "description": "Вечер органной музыки в Органном зале филармонии.", "date_start": datetime.now() + timedelta(days=8), "time": "18:00", "price": "400-800 руб", "age_rating": "6+", "venue_name": "Белгородская государственная филармония", "category_id": 4, "source_url": "https://belfilarm.ru"},
            {"title": "Спектакль «Золушка»", "description": "Детский спектакль в Старооскольском театре.", "date_start": datetime.now() + timedelta(days=12), "time": "11:00", "price": "250 руб", "age_rating": "0+", "venue_name": "Старооскольский театр для детей и молодёжи", "category_id": 1},
        ]
        venue_map = {v.name: v for v in Venue.query.all()}
        for ed in events_data:
            venue = venue_map.get(ed["venue_name"])
            if venue:
                event = Event(title=ed["title"], description=ed.get("description", ""), date_start=ed["date_start"], date_end=ed.get("date_end"), time=ed.get("time"), price=ed.get("price"), age_rating=ed.get("age_rating"), venue_id=venue.id, category_id=ed["category_id"], source_url=ed.get("source_url", ""))
                db.session.add(event)
    db.session.commit()

if __name__ == "__main__":
    app.run()
