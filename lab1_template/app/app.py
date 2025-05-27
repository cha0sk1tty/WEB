from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    make_response,
)
import io
import csv
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re
import os
from functools import wraps
from flask import Blueprint

app = Flask(__name__)
application = app

# Конфигурация
app.config["SECRET_KEY"] = os.urandom(24).hex()
app.config["DATABASE"] = "users.db"
app.config["VISITS_PER_PAGE"] = 10

# Инициализация Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Пожалуйста, войдите для доступа к этой странице."
login_manager.login_message_category = "warning"

# Создаем Blueprint для отчетов
reports_bp = Blueprint("reports", __name__, template_folder="templates")


class User(UserMixin):
    def __init__(
        self,
        user_id,
        login,
        password_hash,
        first_name,
        last_name=None,
        middle_name=None,
        role_id=None,
        created_at=None,
    ):
        self.id = user_id
        self.login = login
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.role_id = role_id
        self.created_at = created_at
        self.role_name = self.get_role_name()

    def get_role_name(self):
        db = get_db()
        role = db.execute(
            "SELECT name FROM roles WHERE id = ?", (self.role_id,)
        ).fetchone()
        return role["name"] if role else None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Декоратор для проверки прав
def check_rights(required_rights):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Для доступа необходимо авторизоваться", "warning")
                return redirect(url_for("login"))

            user_role = current_user.role_name
            if user_role not in required_rights:
                flash("У вас недостаточно прав для доступа к данной странице", "danger")
                return redirect(url_for("index"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator


# Функции для работы с базой данных
def get_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with app.app_context():
        db = get_db()
        # Создаем таблицу ролей
        db.execute(
            """
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
        """
        )

        # Создаем таблицу пользователей
        db.execute(
            """
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
        """
        )

        # Создаем таблицу логов посещений
        db.execute(
            """
        CREATE TABLE IF NOT EXISTS visit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
        )

        # Проверяем, есть ли роли
        if not db.execute("SELECT 1 FROM roles LIMIT 1").fetchone():
            # Добавляем базовые роли
            roles = [
                ("Администратор", "Полный доступ"),
                ("Пользователь", "Базовые права"),
            ]
            db.executemany("INSERT INTO roles (name, description) VALUES (?, ?)", roles)

            # Добавляем администратора, если нет пользователей
            if not db.execute("SELECT 1 FROM users LIMIT 1").fetchone():
                admin = User(
                    user_id=1,
                    login="admin",
                    password_hash=generate_password_hash("admin123"),
                    first_name="Администратор",
                    role_id=1,
                )
                db.execute(
                    """
                INSERT INTO users (login, password_hash, first_name, role_id)
                VALUES (?, ?, ?, ?)
                """,
                    (admin.login, admin.password_hash, admin.first_name, admin.role_id),
                )

        db.commit()


# Валидация пароля
def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append("Пароль должен содержать не менее 8 символов")
    if len(password) > 128:
        errors.append("Пароль должен содержать не более 128 символов")
    if not re.search(r"[A-ZА-Я]", password):
        errors.append("Пароль должен содержать хотя бы одну заглавную букву")
    if not re.search(r"[a-zа-я]", password):
        errors.append("Пароль должен содержать хотя бы одну строчную букву")
    if not re.search(r"[0-9]", password):
        errors.append("Пароль должен содержать хотя бы одну цифру")
    if re.search(r'[^A-Za-zА-Яа-я0-9~!?@#$%^&*_\-+()\[\]{}><\/\\|"\'\.,:;]', password):
        errors.append("Пароль содержит недопустимые символы")
    if " " in password:
        errors.append("Пароль не должен содержать пробелов")
    return errors


# Валидация логина
def validate_login(login):
    errors = []
    if len(login) < 5:
        errors.append("Логин должен содержать не менее 5 символов")
    if not re.match(r"^[A-Za-z0-9]+$", login):
        errors.append("Логин должен содержать только латинские буквы и цифры")
    return errors


# Логирование посещений
@app.before_request
def log_visit():
    if request.path.startswith("/static/"):
        return

    db = get_db()
    user_id = current_user.id if current_user.is_authenticated else None
    db.execute(
        """
    INSERT INTO visit_logs (path, user_id)
    VALUES (?, ?)
    """,
        (request.path, user_id),
    )
    db.commit()


# Загрузчик пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user_data = db.execute(
        """
    SELECT id, login, password_hash, first_name, last_name, middle_name, role_id, created_at
    FROM users WHERE id = ?
    """,
        (user_id,),
    ).fetchone()

    if user_data:
        return User(
            user_id=user_data["id"],
            login=user_data["login"],
            password_hash=user_data["password_hash"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            middle_name=user_data["middle_name"],
            role_id=user_data["role_id"],
            created_at=user_data["created_at"],
        )
    return None


# Маршруты
@app.route("/")
def index():
    db = get_db()
    users = db.execute(
        """
    SELECT u.id, u.login, u.first_name, u.last_name, u.middle_name, u.created_at, r.name as role_name
    FROM users u
    LEFT JOIN roles r ON u.role_id = r.id
    ORDER BY u.created_at DESC
    """
    ).fetchall()
    return render_template("index.html", users=users)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = request.form.get("remember") == "on"

        db = get_db()
        user_data = db.execute(
            """
        SELECT id, login, password_hash, first_name, last_name, middle_name, role_id, created_at
        FROM users WHERE login = ?
        """,
            (username,),
        ).fetchone()

        if user_data and check_password_hash(user_data["password_hash"], password):
            user = User(
                user_id=user_data["id"],
                login=user_data["login"],
                password_hash=user_data["password_hash"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                middle_name=user_data["middle_name"],
                role_id=user_data["role_id"],
                created_at=user_data["created_at"],
            )
            login_user(user, remember=remember)
            flash("Вы успешно вошли!", "success")
            next_page = request.args.get("next") or url_for("index")
            return redirect(next_page)
        flash("Неверные данные!", "danger")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы", "info")
    return redirect(url_for("index"))


# Маршруты для отчетов
@reports_bp.route("/visits")
@login_required
def visits():
    page = request.args.get("page", 1, type=int)
    per_page = app.config["VISITS_PER_PAGE"]

    db = get_db()

    # Для администратора показываем все логи, для пользователя - только свои
    if current_user.role_name == "Администратор":
        logs = db.execute(
            """
        SELECT v.id, v.path, v.created_at, u.first_name, u.last_name, u.middle_name
        FROM visit_logs v
        LEFT JOIN users u ON v.user_id = u.id
        ORDER BY v.created_at DESC
        LIMIT ? OFFSET ?
        """,
            (per_page, (page - 1) * per_page),
        ).fetchall()

        total = db.execute("SELECT COUNT(*) FROM visit_logs").fetchone()[0]
    else:
        logs = db.execute(
            """
        SELECT v.id, v.path, v.created_at, u.first_name, u.last_name, u.middle_name
        FROM visit_logs v
        LEFT JOIN users u ON v.user_id = u.id
        WHERE v.user_id = ?
        ORDER BY v.created_at DESC
        LIMIT ? OFFSET ?
        """,
            (current_user.id, per_page, (page - 1) * per_page),
        ).fetchall()

        total = db.execute(
            "SELECT COUNT(*) FROM visit_logs WHERE user_id = ?", (current_user.id,)
        ).fetchone()[0]

    return render_template(
        "visits.html", logs=logs, page=page, per_page=per_page, total=total
    )


@reports_bp.route("/visits/by_page")
@login_required
@check_rights(["Администратор"])
def visits_by_page():
    db = get_db()
    stats = db.execute(
        """
    SELECT path, COUNT(*) as count
    FROM visit_logs
    GROUP BY path
    ORDER BY count DESC
    """
    ).fetchall()

    return render_template("visits_by_page.html", stats=stats)


@reports_bp.route("/visits/by_page/csv")
@login_required
@check_rights(["Администратор"])
def visits_by_page_csv():
    db = get_db()
    stats = db.execute(
        """
        SELECT path, COUNT(*) as count
        FROM visit_logs
        GROUP BY path
        ORDER BY count DESC
        """
    ).fetchall()


    output = io.StringIO()
    writer = csv.writer(output, delimiter=",")


    output.write("\ufeff")
    writer.writerow(["№", "Страница", "Количество посещений"])

    # Записываем данные
    for i, row in enumerate(stats, 1):
        writer.writerow([i, row["path"], row["count"]])

    # Создаем response 
    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8-sig"
    response.headers["Content-Disposition"] = "attachment; filename=visits_by_page.csv"
    return response


@reports_bp.route("/visits/by_user")
@login_required
@check_rights(["Администратор"])
def visits_by_user():
    db = get_db()
    stats = db.execute(
        """
    SELECT 
        CASE 
            WHEN u.id IS NULL THEN 'Неаутентифицированный пользователь'
            ELSE u.first_name || ' ' || COALESCE(u.last_name, '') || ' ' || COALESCE(u.middle_name, '')
        END as user_name,
        COUNT(*) as count
    FROM visit_logs v
    LEFT JOIN users u ON v.user_id = u.id
    GROUP BY user_name
    ORDER BY count DESC
    """
    ).fetchall()

    return render_template("visits_by_user.html", stats=stats)


@reports_bp.route("/visits/by_user/csv")
@login_required
@check_rights(["Администратор"])
def visits_by_user_csv():
    db = get_db()
    stats = db.execute(
        """
        SELECT 
            CASE 
                WHEN u.id IS NULL THEN 'Неаутентифицированный пользователь'
                ELSE u.first_name || ' ' || COALESCE(u.last_name, '') || ' ' || COALESCE(u.middle_name, '')
            END as user_name,
            COUNT(*) as count
        FROM visit_logs v
        LEFT JOIN users u ON v.user_id = u.id
        GROUP BY user_name
        ORDER BY count DESC
        """
    ).fetchall()

    # Создаем CSV
    output = io.StringIO()
    writer = csv.writer(output, delimiter=',')
    
    # Добавляем BOM 
    output.write('\ufeff')
    
    # Записываем заголовки
    writer.writerow(['№', 'Пользователь', 'Количество посещений'])
    
    # Записываем данные
    for i, row in enumerate(stats, 1):
        writer.writerow([i, row['user_name'], row['count']])

    # Создаем response
    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8-sig"
    response.headers["Content-Disposition"] = "attachment; filename=visits_by_user.csv"
    return response


# Регистрируем Blueprint с отчетами
app.register_blueprint(reports_bp, url_prefix="/reports")


@app.route("/users/<int:user_id>")
def view_user(user_id):
    db = get_db()
    user = db.execute(
        """
        SELECT u.id, u.login, u.first_name, u.last_name, u.middle_name, u.created_at, r.name as role_name
        FROM users u
        LEFT JOIN roles r ON u.role_id = r.id
        WHERE u.id = ?
    """,
        (user_id,),
    ).fetchone()

    if not user:
        flash("Пользователь не найден", "danger")
        return redirect(url_for("index"))

    return render_template("view_user.html", user=user)


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    errors = {}

    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        # Валидация
        if not current_user.check_password(old_password):
            errors["old_password"] = "Неверный текущий пароль"

        if not new_password:
            errors["new_password"] = "Новый пароль не может быть пустым"
        else:
            password_errors = validate_password(new_password)
            if password_errors:
                errors["new_password"] = password_errors[0]

        if new_password != confirm_password:
            errors["confirm_password"] = "Пароли не совпадают"

        if not errors:
            db = get_db()
            try:
                new_password_hash = generate_password_hash(new_password)
                db.execute(
                    """
                UPDATE users
                SET password_hash = ?
                WHERE id = ?
                """,
                    (new_password_hash, current_user.id),
                )
                db.commit()
                flash("Пароль успешно изменен", "success")
                return redirect(url_for("index"))
            except Exception as e:
                db.rollback()
                flash(f"Ошибка при изменении пароля: {str(e)}", "danger")

    return render_template("change_password.html", errors=errors)


@app.route("/users/create", methods=["GET", "POST"])
@login_required
def create_user():
    db = get_db()
    roles = db.execute("SELECT id, name FROM roles").fetchall()
    errors = {}

    if request.method == "POST":
        print("\n[DEBUG] Получены данные формы:", request.form)

        login = request.form.get("login")
        password = request.form.get("password")
        last_name = request.form.get("last_name")
        first_name = request.form.get("first_name")
        middle_name = request.form.get("middle_name")
        role_id = request.form.get("role_id")

        # Валидация данных
        if not login:
            errors["login"] = "Логин обязателен"
        if not password:
            errors["password"] = "Пароль обязателен"
        if not first_name:
            errors["first_name"] = "Имя обязательно"

        if not errors:
            try:
                # Проверяем подключение к БД
                db.execute("SELECT 1").fetchone()
                print("[DEBUG] Подключение к БД работает")

                # Создаем хеш пароля
                password_hash = generate_password_hash(password)
                print("[DEBUG] Хеш пароля создан")

                # Вставляем пользователя
                db.execute(
                    """
                INSERT INTO users (login, password_hash, last_name, first_name, middle_name, role_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        login,
                        password_hash,
                        last_name or None,
                        first_name,
                        middle_name or None,
                        role_id or None,
                    ),
                )

                # Явно фиксируем транзакцию
                db.commit()
                print("[DEBUG] Запись добавлена в БД, транзакция зафиксирована")

                flash("Пользователь успешно создан", "success")
                return redirect(url_for("index"))

            except sqlite3.IntegrityError as e:
                db.rollback()
                if "UNIQUE constraint failed: users.login" in str(e):
                    errors["login"] = "Пользователь с таким логином уже существует"
                else:
                    errors["database"] = "Ошибка базы данных"
                print("[ERROR] Ошибка БД:", str(e))

            except Exception as e:
                db.rollback()
                errors["database"] = "Неизвестная ошибка"
                print("[ERROR] Неизвестная ошибка:", str(e))

        if errors:
            print("[DEBUG] Ошибки валидации:", errors)
            for field, message in errors.items():
                flash(f"{field}: {message}", "danger")

    return render_template("create_user.html", roles=roles, errors=errors)


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    roles = db.execute("SELECT id, name FROM roles").fetchall()
    errors = {}

    if not user:
        flash("Пользователь не найден", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        last_name = request.form.get("last_name")
        first_name = request.form.get("first_name")
        middle_name = request.form.get("middle_name")
        role_id = request.form.get("role_id")

        # Валидация
        if not first_name:
            errors["first_name"] = "Имя не может быть пустым"

        # Если пользователь не администратор, сохраняем его текущую роль
        if current_user.role_name != "Администратор":
            role_id = user["role_id"]

        if not errors:
            try:
                db.execute(
                    """
                UPDATE users
                SET last_name = ?, first_name = ?, middle_name = ?, role_id = ?
                WHERE id = ?
                """,
                    (
                        last_name or None,
                        first_name,
                        middle_name or None,
                        role_id,
                        user_id,
                    ),
                )
                db.commit()
                flash("Пользователь успешно обновлен", "success")
                return redirect(url_for("index"))
            except Exception as e:
                db.rollback()
                flash(f"Ошибка при обновлении пользователя: {str(e)}", "danger")

    return render_template("edit_user.html", user=user, roles=roles, errors=errors)


@app.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    db = get_db()
    try:
        db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        db.commit()
        flash("Пользователь успешно удален", "success")
    except Exception as e:
        db.rollback()
        flash(f"Ошибка при удалении пользователя: {str(e)}", "danger")
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
