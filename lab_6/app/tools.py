# Импорт библиотек
import hashlib  # Для создания хэша файлов
import uuid  # Для генерации уникальных ID
import os  # Для работы с файловой системой
from werkzeug.utils import secure_filename  # Для безопасного имени файла
from flask import current_app  # Доступ к текущему приложению Flask
from models import db, Course, Image  # Импорт моделей и базы данных

# Класс фильтрации курсов по имени и категориям
class CoursesFilter:
    def __init__(self, name, category_ids):
        self.name = name  # Имя курса для фильтрации (поиск по названию)
        self.category_ids = category_ids  # Список ID категорий
        self.query = db.select(Course)  # Начальный запрос без фильтров

    def perform(self):
        self.__filter_by_name()  # Фильтрация по названию (если задано)
        self.__filter_by_category_ids()  # Фильтрация по категориям
        return self.query.order_by(Course.created_at.desc())  # Сортировка по дате создания, от новых к старым

    def __filter_by_name(self):
        if self.name:
            # Добавляем фильтр по имени с использованием ILIKE (регистронезависимый поиск)
            self.query = self.query.filter(
                Course.name.ilike('%' + self.name + '%'))

    def __filter_by_category_ids(self):
        if self.category_ids:
            # Фильтр по списку категорий (если указаны)
            self.query = self.query.filter(
                Course.category_id.in_(self.category_ids))

# Класс для сохранения изображения и предотвращения дублирования
class ImageSaver:
    def __init__(self, file):
        self.file = file  # Полученный файл (например, из формы)

    def save(self):
        self.img = self.__find_by_md5_hash()  # Проверка: уже существует ли такой файл (по хэшу)
        if self.img is not None:
            return self.img  # Если уже есть — возвращаем его (не сохраняем заново)

        # Безопасное имя файла
        file_name = secure_filename(self.file.filename)
        
        # Создание новой записи изображения
        self.img = Image(
            id=str(uuid.uuid4()),  # Уникальный ID
            file_name=file_name,
            mime_type=self.file.mimetype,  # MIME-тип (например, image/jpeg)
            md5_hash=self.md5_hash  # Хэш содержимого файла
        )

        # Сохраняем файл в файловую систему
        self.file.save(
            os.path.join(current_app.config['UPLOAD_FOLDER'],  # Путь загрузки из конфигурации
                         self.img.storage_filename))  # Уникальное имя файла

        # Добавляем запись в базу данных
        db.session.add(self.img)
        db.session.commit()
        return self.img  # Возвращаем объект изображения

    def __find_by_md5_hash(self):
        # Считаем MD5-хэш содержимого файла
        self.md5_hash = hashlib.md5(self.file.read()).hexdigest()
        self.file.seek(0)  # Возвращаем "курсор" файла в начало (чтобы позже его можно было сохранить)
        # Ищем изображение с таким же хэшем
        return db.session.execute(
            db.select(Image).filter(Image.md5_hash == self.md5_hash)
        ).scalar()
