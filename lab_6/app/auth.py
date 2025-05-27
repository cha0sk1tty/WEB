# Импорт необходимых компонентов Flask и Flask-Login
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required
from models import db, User  # Импорт базы данных и модели пользователя

# Создание Blueprint-а для маршрутов, связанных с авторизацией
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Функция инициализации менеджера входа
def init_login_manager(app):
    login_manager = LoginManager()  # Создание экземпляра LoginManager
    login_manager.login_view = 'auth.login'  # Указание маршрута входа по умолчанию
    login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации.'  # Сообщение при попытке неавторизованного доступа
    login_manager.login_message_category = 'warning'  # Категория сообщения для flash-сообщений
    login_manager.user_loader(load_user)  # Функция для загрузки пользователя по ID
    login_manager.init_app(app)  # Инициализация с приложением Flask

# Функция загрузки пользователя по его ID (для Flask-Login)
def load_user(user_id):
    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()  # Получение пользователя по ID
    return user

# Маршрут авторизации (входа)
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Обработка отправки формы
        login = request.form.get('login')  # Получение логина из формы
        password = request.form.get('password')  # Получение пароля из формы
        if login and password:  # Проверка, что логин и пароль введены
            user = db.session.execute(db.select(User).filter_by(login=login)).scalar()  # Поиск пользователя по логину
            if user and user.check_password(password):  # Проверка пароля
                login_user(user)  # Вход пользователя в систему
                flash('Вы успешно аутентифицированы.', 'success')  # Flash-сообщение об успешной авторизации
                next = request.args.get('next')  # Получение URL-адреса для перенаправления после входа
                return redirect(next or url_for('index'))  # Перенаправление на следующую страницу или на главную
        flash('Введены неверные логин и/или пароль.', 'danger')  # Сообщение об ошибке входа
    return render_template('auth/login.html')  # Отображение шаблона страницы входа

# Маршрут выхода из системы
@bp.route('/logout')
@login_required  # Доступ только для авторизованных пользователей
def logout():
    logout_user()  # Выход пользователя из системы
    return redirect(url_for('index'))  # Перенаправление на главную страницу
