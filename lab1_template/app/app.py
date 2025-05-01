from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from faker import Faker
import re
import os

app = Flask(__name__)
application = app

# Генерация надежного секретного ключа
app.config['SECRET_KEY'] = os.urandom(24).hex()

# Инициализация Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
login_manager.login_message_category = 'warning'

# Модель пользователя
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

# База данных пользователей
users = {
    'user': {'password': 'qwerty'},
    'admin': {'password': 'admin123'}
}
# Загрузчик пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User(user_id) # Создание объекта пользователя

# Генерация тестовых постов
fake = Faker()
images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c', '2d2ab7df-cdbc-48a8-a936-35bba702def5', 
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7', 'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728', 
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

def generate_post(index):
    return {
        "title": fake.sentence(nb_words=7),
        "text": fake.paragraph(nb_sentences=100),
        "author": fake.name(),
        "date": fake.date_time_between(start_date="-2y", end_date="now"),
        "image_id": f"{images_ids[index]}.jpg"
    }

posts_list = sorted([generate_post(i) for i in range(5)], key=lambda p: p["date"], reverse=True)
    
# Маршруты
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visits')
def visits():
    session['visits'] = session.get('visits', 0) + 1
    return render_template('visits.html', visits=session['visits'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user, remember=remember)
            flash('Вы успешно вошли!', 'success')
            next_page = request.args.get('next') or url_for('secret')
            return redirect(next_page)
        flash('Неверные данные!', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

@login_manager.unauthorized_handler
def unauthorized():
    flash('Для доступа необходимо авторизоваться.', 'warning') 
    next_page = request.args.get('next') or request.full_path  
    return redirect(url_for('login', next=next_page))


if __name__ == '__main__':
    app.run()