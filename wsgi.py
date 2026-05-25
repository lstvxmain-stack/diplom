import os
from project import create_app, db
from project.models.admin import AdminUser
from project.models.category import Category
from project.models.venue import Venue
from project.models.event import Event
from datetime import datetime, timedelta

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
        venues_data = [
            {"name": "Белгородский академический драматический театр им. М.С. Щепкина", "address": "г. Белгород, Соборная пл., 1", "latitude": 50.5943, "longitude": 36.5869, "phone": "+7 (4722) 27-01-22", "website": "https://beltheatre.ru", "description": "Один из старейших театров России. В репертуаре — классические и современные постановки.", "district": "Белгород", "category_id": 1, "source_url": "https://beltheatre.ru"},
            {"name": "Белгородский государственный театр кукол", "address": "г. Белгород, ул. Некрасова, 5Б/8", "latitude": 50.6158, "longitude": 36.5826, "phone": "+7 (4722) 26-17-67", "website": "https://bgtk.org", "description": "Кукольный театр для детей и взрослых с богатым репертуаром.", "district": "Белгород", "category_id": 1, "source_url": "https://bgtk.org"},
            {"name": "Кинотеатр «Победа»", "address": "г. Белгород, ул. 50-летия Белгородской области, 8Б", "latitude": 50.5987, "longitude": 36.5863, "phone": "+7 (4722) 32-70-27", "website": "", "description": "Городской кинотеатр с современным оборудованием.", "district": "Белгород", "category_id": 2, "source_url": "https://bel.cultreg.ru/places/3"},
            {"name": "Кинотеатр «Радуга»", "address": "г. Белгород, ул. Шершнёва, 6", "latitude": 50.6160, "longitude": 36.5835, "phone": "+7 (4722) 58-26-80", "website": "", "description": "Кинотеатр с кинозалом и сценой для проведения концертов.", "district": "Белгород", "category_id": 2},
            {"name": "Белгородская государственная филармония", "address": "г. Белгород, ул. Белгородского полка, 56А", "latitude": 50.5988, "longitude": 36.6038, "phone": "+7 (4722) 32-16-31", "website": "https://belfilarm.ru", "description": "Главная концертная площадка региона. Большой, Малый и Органный залы.", "district": "Белгород", "category_id": 4, "source_url": "https://belfilarm.ru"},
            {"name": "Концертный зал Белгородского института искусств и культуры", "address": "г. Белгород, ул. Королёва, 7", "latitude": 50.5750, "longitude": 36.5787, "phone": "", "website": "", "description": "Концертная площадка БГИИК.", "district": "Белгород", "category_id": 3},
            {"name": "«Белгород Арена»", "address": "г. Белгород, ул. Щорса, 14В", "latitude": 50.5735, "longitude": 36.5673, "phone": "", "website": "", "description": "Многофункциональный спортивный комплекс, концертная площадка.", "district": "Белгород", "category_id": 5},
            {"name": "Стадион «Салют»", "address": "г. Белгород, просп. Б. Хмельницкого, 107", "latitude": 50.6033, "longitude": 36.5796, "phone": "", "website": "", "description": "Центральный стадион Белгорода.", "district": "Белгород", "category_id": 5},
            {"name": "Дворец культуры «Энергомаш»", "address": "г. Белгород, просп. Б. Хмельницкого, 78Б", "latitude": 50.6104, "longitude": 36.5832, "phone": "+7 (4722) 31-85-82", "website": "", "description": "Центр культурной жизни. Концерты, спектакли, фестивали.", "district": "Белгород", "category_id": 6},
            {"name": "Культурный центр «Октябрь»", "address": "г. Белгород, ул. Н. Чумичова, 124", "latitude": 50.6142, "longitude": 36.5940, "phone": "", "website": "", "description": "Городской культурный центр с разнообразной программой.", "district": "Белгород", "category_id": 6},
            {"name": "Дворец культуры «Комсомольский»", "address": "г. Губкин, ул. Дзержинского, 15", "latitude": 51.2760, "longitude": 37.5363, "phone": "", "website": "", "description": "Центральный дворец культуры г. Губкин.", "district": "Губкинский", "category_id": 6},
            {"name": "Старооскольский театр для детей и молодёжи", "address": "г. Старый Оскол, ул. Ленина, 18", "latitude": 51.2943, "longitude": 37.8363, "phone": "+7 (4725) 22-43-77", "website": "", "description": "Театр в Старом Осколе.", "district": "Старооскольский", "category_id": 1},
            {"name": "Кинотеатр «Быль»", "address": "г. Старый Оскол, микрорайон Ольминского, 6", "latitude": 51.3130, "longitude": 37.8758, "phone": "", "website": "", "description": "Кинотеатр в Старом Осколе.", "district": "Старооскольский", "category_id": 2},
            {"name": "ДК «Горняк»", "address": "г. Шебекино, ул. Ленина, 53", "latitude": 50.3888, "longitude": 36.8776, "phone": "", "website": "", "description": "Центр культурной жизни Шебекино.", "district": "Шебекинский", "category_id": 6},
            {"name": "Валуйский историко-художественный музей", "address": "г. Валуйки, ул. Ленина, 10", "latitude": 50.2107, "longitude": 38.1101, "phone": "", "website": "", "description": "Музей истории и искусства.", "district": "Валуйский", "category_id": 7},
            {"name": "Алексеевский краеведческий музей", "address": "г. Алексеевка, пл. Победы, 56", "latitude": 50.6309, "longitude": 38.6866, "phone": "", "website": "", "description": "Краеведческий музей.", "district": "Алексеевский", "category_id": 7},
        ]
        venue_map = {}
        for vd in venues_data:
            venue = Venue(**vd)
            db.session.add(venue)
            db.session.flush()
            venue_map[vd["name"]] = venue
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
        for ed in events_data:
            event = Event(title=ed["title"], description=ed.get("description", ""), date_start=ed["date_start"], date_end=ed.get("date_end"), time=ed.get("time"), price=ed.get("price"), age_rating=ed.get("age_rating"), venue_id=venue_map[ed["venue_name"]].id, category_id=ed["category_id"], source_url=ed.get("source_url", ""))
            db.session.add(event)
    db.session.commit()

if __name__ == "__main__":
    app.run()
