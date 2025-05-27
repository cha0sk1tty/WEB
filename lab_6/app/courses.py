# Импорт необходимых компонентов Flask, Flask-Login и SQLAlchemy
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from models import db, Course, Category, User, Review  # Импорт моделей базы данных
from tools import CoursesFilter, ImageSaver  # Импорт фильтра и обработчика изображений
from sqlalchemy import func  # Импорт агрегатных функций SQLAlchemy (не используется в коде, можно удалить)

# Создание Blueprint для маршрутов, связанных с курсами
bp = Blueprint('courses', __name__, url_prefix='/courses')

# Список параметров, используемых при создании курса
COURSE_PARAMS = [
    'author_id', 'name', 'category_id', 'short_desc', 'full_desc'
]

# Список параметров отзыва
REVIEW_PARAMS = ['rating', 'text']

# Функция для сбора параметров курса из формы
def params():
    return {p: request.form.get(p) or None for p in COURSE_PARAMS}

# Функция для сбора параметров отзыва из формы
def review_params():
    return {p: request.form.get(p) or None for p in REVIEW_PARAMS}

# Функция для сбора параметров поиска из строки запроса
def search_params():
    return {
        'name': request.args.get('name'),
        'category_ids': [x for x in request.args.getlist('category_ids') if x],
    }

# Маршрут списка курсов
@bp.route('/')
def index():
    courses = CoursesFilter(**search_params()).perform()  # Фильтрация курсов
    pagination = db.paginate(courses)  # Постраничная навигация
    courses = pagination.items  # Получение текущей страницы курсов
    categories = db.session.execute(db.select(Category)).scalars()  # Получение всех категорий
    return render_template('courses/index.html',
                           courses=courses,
                           categories=categories,
                           pagination=pagination,
                           search_params=search_params())  # Отображение шаблона с курсами

# Маршрут для отображения формы создания курса
@bp.route('/new')
@login_required
def new():
    course = Course()  # Пустой объект курса
    categories = db.session.execute(db.select(Category)).scalars()  # Все категории
    users = db.session.execute(db.select(User)).scalars()  # Все пользователи (для выбора автора)
    return render_template('courses/new.html',
                           categories=categories,
                           users=users,
                           course=course)  # Отображение шаблона формы

# Маршрут создания курса (обработка POST-запроса)
@bp.route('/create', methods=['POST'])
@login_required
def create():
    f = request.files.get('background_img')  # Получение изображения из формы
    img = None
    course = Course()  # Новый объект курса
    try:
        if f and f.filename:
            img = ImageSaver(f).save()  # Сохранение изображения

        image_id = img.id if img else None  # Получение ID изображения, если есть
        course = Course(**params(), background_image_id=image_id)  # Создание курса с параметрами
        db.session.add(course)
        db.session.commit()  # Сохранение в базе данных
    except IntegrityError as err:
        # Обработка ошибки при сохранении
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        db.session.rollback()
        categories = db.session.execute(db.select(Category)).scalars()
        users = db.session.execute(db.select(User)).scalars()
        return render_template('courses/new.html',
                            categories=categories,
                            users=users,
                            course=course)  # Повторный показ формы

    flash(f'Курс {course.name} был успешно добавлен!', 'success')  # Сообщение об успехе

    return redirect(url_for('courses.index'))  # Перенаправление на список курсов

# Маршрут отображения курса и добавления отзыва
@bp.route('/<int:course_id>', methods=['GET', 'POST'])
def show(course_id):
    course = db.get_or_404(Course, course_id)  # Получение курса или ошибка 404
    reviews = db.session.execute(
        db.select(Review).filter_by(course_id=course_id)
        .order_by(Review.created_at.desc()).limit(5)
    ).scalars()  # Получение последних 5 отзывов

    user_review = None
    if current_user.is_authenticated:
        # Поиск отзыва текущего пользователя, если авторизован
        user_review = db.session.execute(
            db.select(Review).filter_by(course_id=course_id, user_id=current_user.id)
        ).scalar()

    # Если отправлена форма и пользователь авторизован
    if request.method == 'POST' and current_user.is_authenticated:
        try:
            if not user_review:  # Если отзыв ещё не оставлен
                review = Review(course_id=course_id, user_id=current_user.id, **review_params())
                db.session.add(review)

                # Обновление рейтинга курса
                course.rating_sum += int(review.rating)
                course.rating_num += 1
                db.session.commit()
            else:
                flash('Вы уже оставили отзыв к этому курсу.', 'warning')  # Повторный отзыв не разрешён

        except IntegrityError as err:
            flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
            db.session.rollback()

        return redirect(url_for('courses.show', course_id=course_id))  # Перезагрузка страницы

    return render_template('courses/show.html', course=course, reviews=list(reviews), user_review=user_review)  # Отображение курса

# Маршрут отображения всех отзывов к курсу с сортировкой
@bp.route('/<int:course_id>/reviews', methods=['GET', 'POST'])
def reviews(course_id):
    course = db.get_or_404(Course, course_id)  # Получение курса

    sort_by = request.args.get('sort_by', 'newest')  # Получение параметра сортировки
    query = db.select(Review).filter_by(course_id=course_id)  # Базовый запрос отзывов

    # Применение сортировки
    if sort_by == 'positive':
        query = query.order_by(Review.rating.desc(), Review.created_at.desc())
    elif sort_by == 'negative':
        query = query.order_by(Review.rating.asc(), Review.created_at.desc())
    else:  # newest
        query = query.order_by(Review.created_at.desc())

    pagination = db.paginate(query, per_page=5)  # Постраничный вывод отзывов
    reviews = pagination.items

    user_review = None
    if current_user.is_authenticated:
        # Проверка, оставлял ли пользователь отзыв
        user_review = db.session.execute(
            db.select(Review).filter_by(course_id=course_id, user_id=current_user.id)
        ).scalar()

    if request.method == 'POST' and current_user.is_authenticated:
        try:
            if not user_review:  # Разрешено оставить только один отзыв
                review = Review(course_id=course_id, user_id=current_user.id, **review_params())
                db.session.add(review)

                # Обновление рейтинга курса
                course.rating_sum += int(review.rating)
                course.rating_num += 1
                db.session.commit()
            else:
                flash('Вы уже оставили отзыв к этому курсу.', 'warning')  # Если отзыв уже есть

        except IntegrityError as err:
            flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
            db.session.rollback()

        return redirect(url_for('courses.reviews', course_id=course_id, sort_by=sort_by))  # Перезагрузка с сортировкой

    return render_template(
        'courses/reviews.html',
        course=course,
        reviews=reviews,
        pagination=pagination,
        sort_by=sort_by,
        user_review=user_review
    )  # Отображение шаблона отзывов
