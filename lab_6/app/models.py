# Импорт стандартных и сторонних библиотек
import os
from typing import Optional, Union, List
from datetime import datetime
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Text, Integer, MetaData

# Класс базы данных с соглашением об именовании ограничений
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',  # Индексы
        "uq": "uq_%(table_name)s_%(column_0_name)s",  # Уникальные ключи
        "ck": "ck_%(table_name)s_%(constraint_name)s",  # Ограничения
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # Внешние ключи
        "pk": "pk_%(table_name)s"  # Первичные ключи
    })

# Инициализация SQLAlchemy с использованием кастомной базовой модели
db = SQLAlchemy(model_class=Base)

# Модель категории
class Category(Base):
    __tablename__ = 'categories'  # Название таблицы в БД

    id = mapped_column(Integer, primary_key=True)  # Первичный ключ
    name: Mapped[str] = mapped_column(String(100))  # Название категории
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))  # Ссылка на родительскую категорию (если есть)

    def __repr__(self):
        return '<Category %r>' % self.name  # Представление объекта в консоли

# Модель пользователя
class User(Base, UserMixin):  # UserMixin добавляет поддержку Flask-Login
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)  # ID пользователя
    first_name: Mapped[str] = mapped_column(String(100))  # Имя
    last_name: Mapped[str] = mapped_column(String(100))  # Фамилия
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))  # Отчество (необязательное)
    login: Mapped[str] = mapped_column(String(100), unique=True)  # Уникальный логин
    password_hash: Mapped[str] = mapped_column(String(200))  # Хэш пароля
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)  # Дата регистрации
    #reviews: Mapped[List["Review"]] = relationship(back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  # Хэширует и сохраняет пароль

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  # Проверка пароля

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])  # Полное имя пользователя

    def __repr__(self):
        return '<User %r>' % self.login

# Модель курса
class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True)  # ID курса
    name: Mapped[str] = mapped_column(String(100))  # Название курса
    short_desc: Mapped[str] = mapped_column(Text)  # Краткое описание
    full_desc: Mapped[str] = mapped_column(Text)  # Полное описание
    rating_sum: Mapped[int] = mapped_column(default=0)  # Сумма всех оценок
    rating_num: Mapped[int] = mapped_column(default=0)  # Количество оценок
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))  # Категория курса
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # Автор курса
    background_image_id: Mapped[str] = mapped_column(ForeignKey("images.id"))  # Фоновое изображение
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)  # Дата создания курса

    author: Mapped["User"] = relationship()  # Отношение к пользователю-автору
    category: Mapped["Category"] = relationship(lazy=False)  # Категория (загружается сразу)
    bg_image: Mapped["Image"] = relationship()  # Отношение к изображению
    reviews: Mapped[List["Review"]] = relationship(back_populates="course")  # Отзывы о курсе

    def __repr__(self):
        return '<Course %r>' % self.name

    @property
    def rating(self):
        # Расчёт среднего рейтинга
        if self.rating_num > 0:
            return self.rating_sum / self.rating_num
        return 0

# Модель изображения
class Image(db.Model):
    __tablename__ = 'images'

    id: Mapped[str] = mapped_column(String(100), primary_key=True)  # Уникальный ID
    file_name: Mapped[str] = mapped_column(String(100))  # Имя файла
    mime_type: Mapped[str] = mapped_column(String(100))  # MIME-тип (например, image/png)
    md5_hash: Mapped[str] = mapped_column(String(100), unique=True)  # Уникальный хеш файла
    object_id: Mapped[Optional[int]]  # ID связанного объекта (если есть)
    object_type: Mapped[Optional[str]] = mapped_column(String(100))  # Тип связанного объекта
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)  # Дата загрузки

    def __repr__(self):
        return '<Image %r>' % self.file_name

    @property
    def storage_filename(self):
        # Генерация имени файла для хранения
        _, ext = os.path.splitext(self.file_name)
        return self.id + ext

    @property
    def url(self):
        # Генерация URL-адреса для доступа к изображению
        return url_for('image', image_id=self.id)

# Модель отзыва
class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)  # ID отзыва
    rating: Mapped[int] = mapped_column(Integer)  # Оценка (число)
    text: Mapped[str] = mapped_column(Text)  # Текст отзыва
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)  # Дата создания отзыва
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))  # ID курса
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # ID пользователя

    course: Mapped["Course"] = relationship(back_populates="reviews")  # Отношение к курсу (каждый отзыв принадлежит одному курсу)
    user: Mapped["User"] = relationship()  # Отношение к пользователю (каждый отзыв принадлежит одному пользователю)

    def __repr__(self):
        return f'<Review {self.id} for Course {self.course_id} by User {self.user_id}>'  # Представление отзыва
