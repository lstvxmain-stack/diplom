from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin as FlaskAdmin
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
flask_admin = FlaskAdmin(name="Культурная карта", template_mode="bootstrap4")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "admin.login_view"

    from project.models.admin import AdminUser

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(int(user_id))

    from project.admin.views import (
        MyAdminIndexView,
        CategoryAdminView,
        VenueAdminView,
        EventAdminView,
        ParserAdminView,
    )
    from project.models.category import Category
    from project.models.venue import Venue
    from project.models.event import Event

    flask_admin.init_app(app, index_view=MyAdminIndexView())
    flask_admin.add_view(CategoryAdminView(Category, db.session, name="Категории"))
    flask_admin.add_view(VenueAdminView(Venue, db.session, name="Объекты"))
    flask_admin.add_view(EventAdminView(Event, db.session, name="Мероприятия"))
    flask_admin.add_view(ParserAdminView(name="Парсеры", endpoint="parseradmin"))

    from project.routes.main import main_bp
    from project.routes.venue import venue_bp
    from project.routes.event import event_bp
    from project.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(venue_bp, url_prefix="/venues")
    app.register_blueprint(event_bp, url_prefix="/events")
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.context_processor
    def inject_categories():
        from project.models.category import Category
        return {"all_categories": Category.query.order_by(Category.sort_order).all()}

    return app
