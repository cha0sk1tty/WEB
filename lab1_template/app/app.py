from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re
import os

app = Flask(__name__)
application = app

# Конфигурация
app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config['DATABASE'] = 'users.db'

# Инициализация Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
login_manager.login_message_category = 'warning'

# Класс пользователя для Flask-Login
class User(UserMixin):
    def __init__(self, user_id, login, password_hash, first_name, last_name=None, middle_name=None, role_id=None, created_at=None):
        self.id = user_id
        self.login = login
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.role_id = role_id
        self.created_at = created_at

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Функции для работы с базой данных
def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        # Создаем таблицу ролей
        db.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
        ''')
        
        # Создаем таблицу пользователей
        db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            last_name TEXT,
            first_name TEXT NOT NULL,
            middle_name TEXT,
            role_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        )
        ''')
        
        # Проверяем, есть ли роли
        if not db.execute('SELECT 1 FROM roles LIMIT 1').fetchone():
            # Добавляем базовые роли
            roles = [
                ('Администратор', 'Полный доступ'),
                ('Модератор', 'Ограниченные права'),
                ('Пользователь', 'Базовые права')
            ]
            db.executemany('INSERT INTO roles (name, description) VALUES (?, ?)', roles)
            
            # Добавляем администратора, если нет пользователей
            if not db.execute('SELECT 1 FROM users LIMIT 1').fetchone():
                admin = User(
                    user_id=1,
                    login='admin',
                    password_hash=generate_password_hash('admin123'),
                    first_name='Администратор',
                    role_id=1
                )
                db.execute('''
                INSERT INTO users (login, password_hash, first_name, role_id)
                VALUES (?, ?, ?, ?)
                ''', (admin.login, admin.password_hash, admin.first_name, admin.role_id))
        
        db.commit()
        
@app.before_first_request
def init_db():
    db = get_db()
    # Создание таблиц
    db.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT,
        middle_name TEXT,
        role_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Добавление тестового администратора
    try:
        db.execute('''
        INSERT INTO users (login, password_hash, first_name, role_id)
        VALUES (?, ?, ?, ?)
        ''', ('admin', generate_password_hash('admin123'), 'Admin', 1))
        db.commit()
    except sqlite3.IntegrityError:
        db.rollback()

# Загрузчик пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user_data = db.execute('''
    SELECT id, login, password_hash, first_name, last_name, middle_name, role_id, created_at
    FROM users WHERE id = ?
    ''', (user_id,)).fetchone()
    
    if user_data:
        return User(
            user_id=user_data['id'],
            login=user_data['login'],
            password_hash=user_data['password_hash'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            middle_name=user_data['middle_name'],
            role_id=user_data['role_id'],
            created_at=user_data['created_at']
        )
    return None

# Валидация пароля
def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append("Пароль должен содержать не менее 8 символов")
    if len(password) > 128:
        errors.append("Пароль должен содержать не более 128 символов")
    if not re.search(r'[A-ZА-Я]', password):
        errors.append("Пароль должен содержать хотя бы одну заглавную букву")
    if not re.search(r'[a-zа-я]', password):
        errors.append("Пароль должен содержать хотя бы одну строчную букву")
    if not re.search(r'[0-9]', password):
        errors.append("Пароль должен содержать хотя бы одну цифру")
    if re.search(r'[^A-Za-zА-Яа-я0-9~!?@#$%^&*_\-+()\[\]{}><\/\\|"\'\.,:;]', password):
        errors.append("Пароль содержит недопустимые символы")
    if ' ' in password:
        errors.append("Пароль не должен содержать пробелов")
    return errors

# Валидация логина
def validate_login(login):
    errors = []
    if len(login) < 5:
        errors.append("Логин должен содержать не менее 5 символов")
    if not re.match(r'^[A-Za-z0-9]+$', login):
        errors.append("Логин должен содержать только латинские буквы и цифры")
    return errors

# Маршруты
@app.route('/')
def index():
    db = get_db()
    users = db.execute('''
    SELECT u.id, u.login, u.first_name, u.last_name, u.middle_name, u.created_at, r.name as role_name
    FROM users u
    LEFT JOIN roles r ON u.role_id = r.id
    ORDER BY u.created_at DESC
    ''').fetchall()
    return render_template('index.html', users=users)

@app.route('/users/<int:user_id>')
def view_user(user_id):
    db = get_db()
    user = db.execute('''
    SELECT u.id, u.login, u.first_name, u.last_name, u.middle_name, u.created_at, r.name as role_name
    FROM users u
    LEFT JOIN roles r ON u.role_id = r.id
    WHERE u.id = ?
    ''', (user_id,)).fetchone()
    
    if not user:
        flash('Пользователь не найден', 'danger')
        return redirect(url_for('index'))
    
    return render_template('view_user.html', user=user)

@app.route('/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    db = get_db()
    roles = db.execute('SELECT id, name FROM roles').fetchall()
    errors = {}
    
    if request.method == 'POST':
        print("\n[DEBUG] Получены данные формы:", request.form)
        
        login = request.form.get('login')
        password = request.form.get('password')
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        role_id = request.form.get('role_id')

        # Валидация данных
        if not login:
            errors['login'] = 'Логин обязателен'
        if not password:
            errors['password'] = 'Пароль обязателен'
        if not first_name:
            errors['first_name'] = 'Имя обязательно'

        if not errors:
            try:
                # Проверяем подключение к БД
                db.execute("SELECT 1").fetchone()
                print("[DEBUG] Подключение к БД работает")

                # Создаем хеш пароля
                password_hash = generate_password_hash(password)
                print("[DEBUG] Хеш пароля создан")

                # Вставляем пользователя
                db.execute('''
                INSERT INTO users (login, password_hash, last_name, first_name, middle_name, role_id)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (login, password_hash, last_name or None, first_name, middle_name or None, role_id or None))
                
                # Явно фиксируем транзакцию
                db.commit()
                print("[DEBUG] Запись добавлена в БД, транзакция зафиксирована")

                flash('Пользователь успешно создан', 'success')
                return redirect(url_for('index'))

            except sqlite3.IntegrityError as e:
                db.rollback()
                if "UNIQUE constraint failed: users.login" in str(e):
                    errors['login'] = 'Пользователь с таким логином уже существует'
                else:
                    errors['database'] = 'Ошибка базы данных'
                print("[ERROR] Ошибка БД:", str(e))

            except Exception as e:
                db.rollback()
                errors['database'] = 'Неизвестная ошибка'
                print("[ERROR] Неизвестная ошибка:", str(e))

        if errors:
            print("[DEBUG] Ошибки валидации:", errors)
            for field, message in errors.items():
                flash(f'{field}: {message}', 'danger')

    return render_template('create_user.html', roles=roles, errors=errors)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    roles = db.execute('SELECT id, name FROM roles').fetchall()
    errors = {}
    
    if not user:
        flash('Пользователь не найден', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        role_id = request.form.get('role_id')
        
        # Валидация
        if not first_name:
            errors['first_name'] = 'Имя не может быть пустым'
        
        if not errors:
            try:
                db.execute('''
                UPDATE users
                SET last_name = ?, first_name = ?, middle_name = ?, role_id = ?
                WHERE id = ?
                ''', (last_name or None, first_name, middle_name or None, role_id or None, user_id))
                db.commit()
                flash('Пользователь успешно обновлен', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.rollback()
                flash(f'Ошибка при обновлении пользователя: {str(e)}', 'danger')
    
    return render_template('edit_user.html', user=user, roles=roles, errors=errors)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    db = get_db()
    try:
        db.execute('DELETE FROM users WHERE id = ?', (user_id,))
        db.commit()
        flash('Пользователь успешно удален', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Ошибка при удалении пользователя: {str(e)}', 'danger')
    return redirect(url_for('index'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    errors = {}
    
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Валидация
        if not current_user.check_password(old_password):
            errors['old_password'] = 'Неверный текущий пароль'
        
        if not new_password:
            errors['new_password'] = 'Новый пароль не может быть пустым'
        else:
            password_errors = validate_password(new_password)
            if password_errors:
                errors['new_password'] = password_errors[0]
        
        if new_password != confirm_password:
            errors['confirm_password'] = 'Пароли не совпадают'
        
        if not errors:
            db = get_db()
            try:
                new_password_hash = generate_password_hash(new_password)
                db.execute('''
                UPDATE users
                SET password_hash = ?
                WHERE id = ?
                ''', (new_password_hash, current_user.id))
                db.commit()
                flash('Пароль успешно изменен', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.rollback()
                flash(f'Ошибка при изменении пароля: {str(e)}', 'danger')
    
    return render_template('change_password.html', errors=errors)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        db = get_db()
        user_data = db.execute('''
        SELECT id, login, password_hash, first_name, last_name, middle_name, role_id, created_at
        FROM users WHERE login = ?
        ''', (username,)).fetchone()
        
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(
                user_id=user_data['id'],
                login=user_data['login'],
                password_hash=user_data['password_hash'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                middle_name=user_data['middle_name'],
                role_id=user_data['role_id'],
                created_at=user_data['created_at']
            )
            login_user(user, remember=remember)
            flash('Вы успешно вошли!', 'success')
            next_page = request.args.get('next') or url_for('index')
            return redirect(next_page)
        flash('Неверные данные!', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

# Добавьте в конец app.py
if __name__ == '__main__':
    with app.app_context():
        db = get_db()
        print("Проверка целостности БД:")
        print(db.execute("PRAGMA integrity_check").fetchone())
    app.run(debug=True)