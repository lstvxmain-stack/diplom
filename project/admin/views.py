from flask import redirect, url_for, request, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from wtforms import form, fields, validators
from project.models.admin import AdminUser


class LoginForm(form.Form):
    username = fields.StringField("Логин", validators=[validators.DataRequired()])
    password = fields.PasswordField("Пароль", validators=[validators.DataRequired()])


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    @login_required
    def index(self):
        return super().index()

    @expose("/login", methods=["GET", "POST"])
    def login_view(self):
        form = LoginForm(request.form)
        if request.method == "POST" and form.validate():
            user = AdminUser.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for("admin.index"))
        return self.render("admin/login.html", form=form)

    @expose("/logout")
    def logout_view(self):
        logout_user()
        return redirect(url_for("admin.login_view"))


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin.login_view"))


class CategoryAdminView(AdminModelView):
    column_list = ["name", "icon", "color", "sort_order"]
    form_columns = ["name", "icon", "color", "sort_order"]
    column_labels = {
        "name": "Название",
        "icon": "Иконка (FontAwesome)",
        "color": "Цвет маркера",
        "sort_order": "Порядок сортировки",
    }


class VenueAdminView(AdminModelView):
    column_list = ["name", "category", "address", "district", "latitude", "longitude"]
    form_columns = [
        "name", "address", "latitude", "longitude", "phone", "website",
        "description", "image_url", "district", "category", "source_url",
    ]
    column_labels = {
        "name": "Название",
        "category": "Категория",
        "address": "Адрес",
        "district": "Район",
        "latitude": "Широта",
        "longitude": "Долгота",
        "phone": "Телефон",
        "website": "Сайт",
        "description": "Описание",
        "image_url": "URL изображения",
        "source_url": "URL источника",
    }
    column_searchable_list = ["name", "address", "district"]
    column_filters = ["category", "district"]


class EventAdminView(AdminModelView):
    column_list = ["title", "venue", "category", "date_start", "time", "price", "age_rating"]
    form_columns = [
        "title", "description", "date_start", "date_end", "time",
        "price", "age_rating", "venue", "category", "source_url", "image_url",
    ]
    column_labels = {
        "title": "Название",
        "venue": "Объект",
        "category": "Категория",
        "date_start": "Дата начала",
        "date_end": "Дата окончания",
        "time": "Время",
        "price": "Цена",
        "age_rating": "Возрастной рейтинг",
        "description": "Описание",
        "source_url": "URL источника",
        "image_url": "URL изображения",
    }
    column_searchable_list = ["title"]
    column_filters = ["venue", "category", "date_start"]


class ParserAdminView(BaseView):
    @expose("/")
    @login_required
    def index(self):
        return self.render("admin/parsers.html")

    @expose("/run", methods=["POST"])
    @login_required
    def run(self):
        from flask import current_app
        from project.parsers import ParserManager, Afishka31Parser, CultureRFParser

        manager = ParserManager()
        manager.add_parser(Afishka31Parser())

        try:
            manager.run_all(current_app)
            flash("Парсеры успешно выполнили сбор данных", "success")
        except Exception as e:
            flash(f"Ошибка при выполнении парсеров: {e}", "error")

        return redirect(url_for("parseradmin.index"))
