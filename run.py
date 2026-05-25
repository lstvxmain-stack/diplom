import sys
from project import create_app, db
from project.models.admin import AdminUser
from project.models.category import Category

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "AdminUser": AdminUser,
        "Category": Category,
    }


def init_db():
    """Initialize the database with default admin user and categories."""
    with app.app_context():
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
