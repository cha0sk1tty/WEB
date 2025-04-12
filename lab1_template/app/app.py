import random
from flask import Flask, render_template, request, redirect, url_for
import random
from faker import Faker
import re

fake = Faker()

app = Flask(__name__)
application = app

images_ids = [
    "7d4e9175-95ea-4c5f-8be5-92a6b708bb3c",
    "2d2ab7df-cdbc-48a8-a936-35bba702def5",
    "6e12f3de-d5fd-4ebb-855b-8cbc485278b7",
    "afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728",
    "cab5b7f2-774e-4884-a200-0c0180fa777f",
]


def generate_comments(replies=True):
    comments = []
    for i in range(random.randint(1, 3)):
        comment = {"author": fake.name(), "text": fake.text()}
        if replies:
            comment["replies"] = generate_comments(replies=False)
        comments.append(comment)
    return comments


def generate_post(i):
    return {
        "title": fake.sentence(nb_words=7),
        "text": fake.paragraph(nb_sentences=100),
        "author": fake.name(),
        "date": fake.date_time_between(start_date="-2y", end_date="now"),
        "image_id": f"{images_ids[i]}.jpg",
        "comments": generate_comments(),
    }


posts_list = sorted(
    [generate_post(i) for i in range(5)], key=lambda p: p["date"], reverse=True
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/posts")
def posts():
    return render_template("posts.html", title="Посты", posts=posts_list)


@app.route("/posts/<int:index>")
def post(index):
    p = posts_list[index]
    return render_template("post.html", title=p["title"], post=p)


@app.route("/about")
def about():
    return render_template("about.html", title="Об авторе")


@app.route("/url_params")
def url_params():
    return render_template(
        "url_params.html", title="Параметры URL", params=request.args
    )


@app.route("/headers")
def headers():
    return render_template("headers.html", title="Заголовки", headers=request.headers)


@app.route("/cookies")
def cookies():
    return render_template("cookies.html", title="Cookies", cookies=request.cookies)


@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        return render_template(
            "auth_result.html",
            title="Результат авторизации",
            username=username,
            password=password,
        )
    return render_template("auth_form.html", title="Форма авторизации")


@app.route("/phone", methods=["GET", "POST"])
def phone():
    error = None
    phone_number = None
    formatted_phone = None

    if request.method == "POST":
        phone_number = request.form.get("phone_number")

        # Удаляем все разрешенные нецифровые символы
        cleaned_phone = re.sub(r"[\s\+\(\)\-\.]", "", phone_number)

        # Проверка на недопустимые символы
        if not cleaned_phone.isdigit():
            error = {
                "type": "invalid_chars",
                "message": "Недопустимый ввод. В номере телефона встречаются недопустимые символы.",
            }
        else:
            # Проверка длины номера
            if phone_number.startswith(("+7", "8")):
                required_length = 11
            else:
                required_length = 10

            if len(cleaned_phone) != required_length:
                error = {
                    "type": "invalid_length",
                    "message": "Недопустимый ввод. Неверное количество цифр.",
                }
            else:
                # Форматирование номера
                if phone_number.startswith("+7"):
                    cleaned_phone = "8" + cleaned_phone[1:]

                formatted_phone = f"8-{cleaned_phone[1:4]}-{cleaned_phone[4:7]}-{cleaned_phone[7:9]}-{cleaned_phone[9:]}"

    return render_template(
        "phone_form.html",
        title="Проверка номера телефона",
        phone_number=phone_number,
        formatted_phone=formatted_phone,
        error=error,
    )


if __name__ == "__main__":
    app.run()
