import sys, os, json
from datetime import datetime, timedelta
from project import create_app, db
from project.models.admin import AdminUser
from project.models.category import Category
from project.models.venue import Venue
from project.models.event import Event

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "AdminUser": AdminUser,
        "Category": Category,
        "Venue": Venue,
        "Event": Event,
    }


def init_db():
    """Initialize the database with all seed data."""
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
            db.session.flush()

        if not Venue.query.first():
            seed_path = os.path.join(app.root_path, '..', 'data', 'seed_venues.json')
            if os.path.exists(seed_path):
                with open(seed_path, 'r', encoding='utf-8') as f:
                    venues_data = json.load(f)
                for vd in venues_data:
                    db.session.add(Venue(**vd))
                db.session.flush()

        if not Event.query.first():
            events_data = [
                {"title": "Спектакль «Горе от ума»", "description": "Бессмертная комедия А.С. Грибоедова «Горе от ума» — одна из самых известных пьес русской классической драматургии, разобранная на цитаты ещё при жизни автора. На сцене Белгородского академического драматического театра им. М.С. Щепкина спектакль идёт в современной постановке, которая сохраняет остроту грибоедовского текста и добавляет новые сценические решения. Зрителей ждут яркие актёрские работы, узнаваемые персонажи — Чацкий, Фамусов, Молчалин, Софья — и вечная история о противостоянии ума и сердца, передовых взглядов и консервативного общества.", "date_start": datetime.now() + timedelta(days=7), "time": "18:30", "price": "400-1200 руб", "age_rating": "12+", "venue_name": "Белгородский академический драматический театр им. М.С. Щепкина", "category_id": 1, "source_url": "https://afishka31.ru/", "organizer_url": "https://beldramtheatre.ru/"},
                {"title": "Концерт симфонического оркестра", "description": "Симфонический оркестр Белгородской филармонии под управлением главного дирижёра представляет программу из шедевров русской классики. В концерте прозвучат Первый концерт для фортепиано с оркестром П.И. Чайковского, Второй концерт С.В. Рахманинова и «Мимолётности» С.С. Прокофьева. Это уникальная возможность услышать живую академическую музыку в исполнении одного из ведущих симфонических коллективов Черноземья. Концерт проходит в Большом зале филармонии, славившемся своей акустикой.", "date_start": datetime.now() + timedelta(days=3), "time": "19:00", "price": "500-1500 руб", "age_rating": "6+", "venue_name": "Белгородская государственная филармония", "category_id": 4, "source_url": "https://afishka31.ru/", "organizer_url": "https://belfilarm.ru/"},
                {"title": "Мюзикл «Принцесса на горошине»", "description": "Музыкальный спектакль по мотивам знаменитой сказки Ганса Христиана Андерсена в постановке Белгородского государственного театра кукол. Яркие куклы ручной работы, живое музыкальное сопровождение и профессиональная игра актёров-кукловодов создают на сцене настоящую сказочную атмосферу. История о том, как настоящая принцесса была обнаружена благодаря одной маленькой горошине, учит детей доброте, честности и чуткости. Спектакль рекомендован для семейного просмотра.", "date_start": datetime.now() + timedelta(days=5), "time": "11:00", "price": "300 руб", "age_rating": "0+", "venue_name": "Белгородский государственный театр кукол", "category_id": 1, "source_url": "https://afishka31.ru/", "organizer_url": "https://bgtk.org/"},
                {"title": "Фестиваль «Белгородское лето»", "description": "Ежегодный городской фестиваль «Белгородское лето» — одно из самых ожидаемых событий сезона, объединяющее музыку, театр, спорт и творчество. Три дня на открытых площадках Дворца культуры «Энергомаш» будут работать интерактивные зоны, проходить концерты местных и приглашённых коллективов, мастер-классы по живописи, гончарному делу и танцам. Для детей организована отдельная программа с аниматорами и настольными играми. Вход на все мероприятия свободный.", "date_start": datetime.now() + timedelta(days=14), "date_end": datetime.now() + timedelta(days=16), "time": "12:00", "price": "Бесплатно", "age_rating": "0+", "venue_name": "Дворец культуры «Энергомаш»", "category_id": 8, "source_url": "https://afishka31.ru/", "organizer_url": ""},
                {"title": "Матч по футболу. Салют — Металлург", "description": "Центральный матч тура в первенстве России по футболу среди команд Второй лиги встречают белгородский «Салют» и липецкий «Металлург». Принципиальное противостояние двух соседних регионов всегда собирает полный стадион. «Салют» — один из старейших клубов Черноземья, основанный в 1960 году, с богатой историей и преданными болельщиками. Матч обещает быть напряжённым: обе команды борются за место в верхней части турнирной таблицы.", "date_start": datetime.now() + timedelta(days=10), "time": "16:00", "price": "100-300 руб", "age_rating": "6+", "venue_name": "Стадион «Салют»", "category_id": 5, "source_url": "https://afishka31.ru/", "organizer_url": ""},
                {"title": "Премьера фильма", "description": "В кинотеатре «Победа» состоится премьерный показ нового российского фильма, который уже получил высокие оценки на национальных кинофестивалях. Современное цифровое оборудование кинозала, объёмный звук Dolby Atmos и удобные кресла с амфитеатральным расположением обеспечат максимальный комфорт просмотра. Кинотеатр «Победа» — старейший кинотеатр Белгорода, после реконструкции 2023 года оснащённый по последнему слову техники.", "date_start": datetime.now() + timedelta(days=2), "time": "10:00-23:00", "price": "200-400 руб", "age_rating": "12+", "venue_name": "Кинотеатр «Победа»", "category_id": 2, "source_url": "https://afishka31.ru/", "organizer_url": ""},
                {"title": "Концерт группы «Radio Tapok»", "description": "Radio Tapok — российский рок-проект, получивший широкую известность благодаря кавер-версиям и пародиям на мировые хиты, а также собственной оригинальной музыке в жанрах панк-рок и поп-рок. Основатель и бессменный лидер группы — музыкант Павел «Паша Техник» (настоящее имя Павел Ивлев), чьи провокационные тексты и энергичные выступления собирают многотысячные залы по всей стране. Концерт пройдёт на «Белгород Арене» — крупнейшей концертно-спортивной площадке области вместимостью до 5000 зрителей, оснащённой современным световым и звуковым оборудованием. В программе — как новые треки, так и проверенные хиты, которые зрители будут петь хором.", "date_start": datetime.now() + timedelta(days=20), "time": "20:00", "price": "800-2000 руб", "age_rating": "16+", "venue_name": "«Белгород Арена»", "category_id": 5, "source_url": "https://afishka31.ru/", "organizer_url": ""},
                {"title": "Выставка «Белгород в живописи»", "description": "В Валуйском историко-художественном музее открывается выставка «Белгород в живописи», представляющая более 50 работ белгородских художников XX–XXI веков. В экспозиции — пейзажи родного края, городские зарисовки, портреты известных земляков и тематические полотна, посвящённые истории Белгородчины. Особого внимания заслуживает раздел, посвящённый белгородской школе живописи, сформировавшейся в 1960–1970-х годах. Выставка будет работать в течение месяца.", "date_start": datetime.now() + timedelta(days=1), "date_end": datetime.now() + timedelta(days=30), "price": "100 руб", "age_rating": "0+", "venue_name": "Валуйский историко-художественный музей", "category_id": 7, "source_url": "https://afishka31.ru/", "organizer_url": ""},
                {"title": "Концерт органной музыки", "description": "Вечер органной музыки в Органном зале Белгородской филармонии — уникальная возможность услышать один из лучших органов Черноземья. В программе — сочинения И.С. Баха, В.А. Моцарта и С. Франка в исполнении титулярного органиста филармонии. Органный зал филармонии славится не только своим инструментом (производства немецкой фирмы «Hermann Eule», установленным в 2019 году), но и идеальной акустикой, созданной специально для органной музыки. Концерт сопровождается комментариями музыковеда об истории исполняемых произведений.", "date_start": datetime.now() + timedelta(days=8), "time": "18:00", "price": "400-800 руб", "age_rating": "6+", "venue_name": "Белгородская государственная филармония", "category_id": 4, "source_url": "https://afishka31.ru/", "organizer_url": "https://belfilarm.ru/"},
                {"title": "Спектакль «Золушка»", "description": "Музыкальный спектакль «Золушка» по мотивам одноимённой сказки Шарля Перро представляет Старооскольский театр для детей и молодёжи. В постановке органично сочетаются классический сюжет, современная хореография и живое вокальное исполнение. Театр, основанный в 1990 году, является одним из ведущих детских театров Белгородской области и неоднократно становился лауреатом региональных и всероссийских театральных фестивалей. Спектакль рекомендован для детей от 3 лет.", "date_start": datetime.now() + timedelta(days=12), "time": "11:00", "price": "250 руб", "age_rating": "0+", "venue_name": "Старооскольский театр для детей и молодёжи", "category_id": 1, "source_url": "https://afishka31.ru/", "organizer_url": ""},
            ]
            venue_map = {v.name: v for v in Venue.query.all()}
            for ed in events_data:
                venue = venue_map.get(ed.pop("venue_name"))
                if venue:
                    db.session.add(Event(venue_id=venue.id, **ed))

        db.session.commit()
        print("База данных инициализирована.")
        print("Администратор: admin / admin123")


def run_parsers():
    """Run all parsers to fetch data from external sources."""
    from project.parsers import ParserManager
    from project.parsers.culture_rf import CultureRFParser

    manager = ParserManager()
    manager.add_parser(CultureRFParser())

    manager.run_all(app)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "parse":
        run_parsers()
    elif len(sys.argv) > 1 and sys.argv[1] == "seed":
        import seed_data
        seed_data.seed()
    else:
        init_db()
        app.run(debug=True, host="0.0.0.0", port=5000)
