# Импорт необходимых модулей и компонентов Flask, SQLAlchemy и других
from flask import Flask, render_template, send_from_directory
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError
from models import db, Category, Image  # Импорт моделей базы данных
from auth import bp as auth_bp, init_login_manager  # Импорт Blueprint и инициализации логина
from courses import bp as courses_bp  # Импорт Blueprint для курсов

# Создание экземпляра приложения Flask
app = Flask(__name__)
application = app  # Для совместимости с WSGI (например, gunicorn ищет переменную "application")

# Загрузка конфигурации из файла config.py
app.config.from_pyfile('config.py')

# Инициализация базы данных с приложением Flask
db.init_app(app)
# Настройка миграций базы данных
migrate = Migrate(app, db)

# Инициализация менеджера входа
init_login_manager(app)

# Обработчик ошибок SQLAlchemy
@app.errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(err):
    # Сообщение об ошибке при работе с базой данных
    error_msg = ('Возникла ошибка при подключении к базе данных. '
                 'Повторите попытку позже.')
    return f'{error_msg} (Подробнее: {err})', 500  # Возвращает текст ошибки и HTTP статус 500

# Регистрация Blueprint-ов
app.register_blueprint(auth_bp)      # Регистрация маршрутов авторизации
app.register_blueprint(courses_bp)   # Регистрация маршрутов курсов

# Маршрут главной страницы
@app.route('/')
def index():
    # Получение всех категорий из базы данных
    categories = db.session.execute(db.select(Category)).scalars()
    # Отображение шаблона index.html с переданными категориями
    return render_template(
        'index.html',
        categories=categories,
    )

# Маршрут для отображения изображений
@app.route('/images/<image_id>')
def image(image_id):
    # Получение изображения по ID или возврат 404, если не найдено
    img = db.get_or_404(Image, image_id)
    
    # Отправка файла из директории UPLOAD_FOLDER по имени файла
    return send_from_directory(
                               app.config['UPLOAD_FOLDER'],  # Путь к папке с загруженными файлами
                               img.file_name                 # Имя запрашиваемого файла
                            )
