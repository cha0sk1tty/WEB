import subprocess
import pytest

# Для Windows
INTERPRETER = "python"
# Для MAC
INTERPRETER = "python"


def run_script(filename, input_data=None):
    # Преобразуем все элементы input_data в строки
    input_str = "\n".join(map(str, input_data)) if input_data else ""
    proc = subprocess.run(
        [INTERPRETER, filename],
        input=input_str,  # Используем преобразованные данные
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.stdout.strip()


test_data = {
    "fact": [(["5"], "120"), (["3"], "6"), (["6"], "720")],
    "show_employee": [
        (["John Doe", "30000"], "John Doe: 30000 ₽"),
        (["John Doe", "20000"], "John Doe: 20000 ₽"),
        (["John Doe"], "John Doe: 100000 ₽"),
    ],
    "sum_and_sub": [
        ([1, 2], (3, -1)),
        ([2, 3], (5, -1)),
        ([5, 3], (8, 2)),
        ([6, 10], (16, -4)),
        ([51, 3], (54, 48)),
        ([11, 22], (33, -11)),
    ],
    "process_list": [
        ([4, 13, 52, 47, 89, 45, 61], [16, 2197, 2704, 103823, 704969, 91125, 226981]),
        ([4, 2, 13, 56, 98], [16, 4, 2197, 3136, 9604]),
        (
            [4, 2, 13, 56, 98, 52, 47, 89, 45, 61],
            [16, 4, 2197, 3136, 9604, 2704, 103823, 704969, 91125, 226981],
        ),
        (
            [4, 2, 13, 56, 102, 123, 65, 84, 96],
            [16, 4, 2197, 3136, 10404, 1860867, 274625, 7056, 9216],
        ),
        (
            [4, 2, 45, 63, 12, 32, 10, 94],
            [16, 4, 91125, 250047, 144, 1024, 100, 8836],
        ),
    ],
    "my_sum": [
        ([1, 2, 3], 6),
        ([1, 2, 4], 7),
        ([1, 2, 3, 4], 10),
    ],
    "my_sum_argv": [
        ([1, 2, 5, 4, 7, 8, 7, 6], 40),
        ([1, 2, 5, 4, 7, 8, 7], 34),
        ([1, 2, 5, 4], 12),
        ([1, 2, 5, 4, 12], 24),
        ([1, 2, 3, 4, 9, 10], 29),
        ([1, 5, 10, 15, 20], 51),
    ],
    "files_sort": [
        (
            "C:\\WEB\\dz_2\\tests_files_sort",
            ["1.txt", "2.txt", "3.txt", "a.txt", "b.txt", "c.txt", "d.txt", "z.txt"],
        )
    ],
    "file_search": [
        (
            "1.txt",
            [
                "Файл расположен в: C:\\WEB\\dz_2\\tests_files_sort",
                "",
                "Данные файла (5 строк):",
                "Старый солдат шёл на побывку. Притомился в пути, есть хочется. Дошёл до деревни, постучал в крайнюю избу:",
                "– Пустите отдохнуть дорожного человека! Дверь отворила старуха.",
                "– Заходи, служивый.",
                "– А нет ли у тебя, хозяюшка, перекусить чего? У старухи всего вдоволь, а солдата поскупилась накормить, прикинулась сиротой.",
                "– Ох, добрый человек, и сама сегодня ещё ничего не ела: нечего.",
            ],
        )
    ],
    "email_validation": [
        (
            [
                "4",
                "svetikjfj.fkfkdk@mail.ruuuu",
                "kirisa@gmail.com",
                "ghfjdjddlfmdkfk",
                "12345@sxdcfvg12345.ru",
            ],
            ["12345@sxdcfvg12345.ru", "kirisa@gmail.com"],
        ),
        (
            [
                "4",
                "user.name@domain.com",
                "user@domain.co.uk",
                "invalid@domain",
                "12345@domain123.ru",
            ],
            ["12345@domain123.ru"],
        ),
        (
            [
                "3",
                "lara@mospolytech.ru",
                "brian-23@mospolytech.ru",
                "britts_54@mospolytech.ru",
            ],
            [
                "brian-23@mospolytech.ru",
                "britts_54@mospolytech.ru",
                "lara@mospolytech.ru",
            ],
        ),
    ],
    "fibonacci": [
        (1, "[0]"),
        (2, "[0, 1]"),
        (3, "[0, 1, 1]"),
        (4, "[0, 1, 1, 8]"),
        (5, "[0, 1, 1, 8, 27]"),
        (6, "[0, 1, 1, 8, 27, 125]"),
        (7, "[0, 1, 1, 8, 27, 125, 512]"),
        (8, "[0, 1, 1, 8, 27, 125, 512, 2197]"),
        (9, "[0, 1, 1, 8, 27, 125, 512, 2197, 9261]"),
        (10, "[0, 1, 1, 8, 27, 125, 512, 2197, 9261, 39304]"),
        (11, "[0, 1, 1, 8, 27, 125, 512, 2197, 9261, 39304, 166375]"),
        (12, "[0, 1, 1, 8, 27, 125, 512, 2197, 9261, 39304, 166375, 704969]"),
        (13, "[0, 1, 1, 8, 27, 125, 512, 2197, 9261, 39304, 166375, 704969, 2985984]"),
        (
            14,
            "[0, 1, 1, 8, 27, 125, 512, 2197, 9261, 39304, 166375, 704969, 2985984, 12649337]",
        ),
        (
            15,
            "[0, 1, 1, 8, 27, 125, 512, 2197, 9261, 39304, 166375, 704969, 2985984, 12649337, 53582633]",
        ),
    ],
    "average_scores": [
        (
            ["5 3", "80 95 65 75 89", "52 54 68 78 59", "91 83 69 81 78"],
            [74.3, 77.3, 67.3, 78.0, 75.3],
        ),
        (
            ["3 4", "56 54 32", "90 89 78", "65 45 85", "91 87 81"],
            [75.5, 68.8, 69.0],
        ),
        (
            ["6 3", "56 89 78 94 56 87", "56 89 91 93 100 97", "56 89 78 69 98 71"],
            [56.0, 89.0, 82.3, 85.3, 84.7, 85.0],
        ),
    ],
    "plane_angle": [
        (["0 0 0", "1 0 0", "1 1 0", "1 1 1"], "90.0"),
        (["-1 0 0", "1 0 0", "-1 1 0", "1 1 1"], "48.18968510422141"),
        (["4 5 6", "1 2 3", "1 4 8", "2 2 8"], "89.18162803003673"),
        (["0 -1 0", "-1 0 0", "0 0 -1", "0 0 0"], "125.26438968275468"),
        (["0.5 21 3", "-1 6 8", "-123 3 2", "10 123 -9"], "169.82863266233858"),
    ],
    "phone_number": [
        (
            ["3", "07895462130", "89875641230", "9195969878"],
            ["+7 (789) 546-21-30", "+7 (919) 596-98-78", "+7 (987) 564-12-30"],
        ),
        (
            ["3", "07985632146", "89657321504", "52369874"],
            ["Неверный формат номера телефона"],
        ),
        (
            ["3", "07986", "89647896", "523785112"],
            ["Неверный формат номера телефона"],
        ),
        (
            ["2", "89652145698", "07892152315"],
            ["+7 (789) 215-23-15", "+7 (965) 214-56-98"],
        ),
    ],
    "people_sort": [
        (
            ["3", "Mike Thomson 20 M", "Robert Bustle 32 M", "Andria Bustle 30 F"],
            ["Mr. Mike Thomson", "Ms. Andria Bustle", "Mr. Robert Bustle"],
        ),
        (
            ["3", "Mikki Mouse 14 M", "Donald Duck 15 M", "Minni Nouse 13 F"],
            ["Ms. Minni Nouse", "Mr. Mikki Mouse", "Mr. Donald Duck"],
        ),
    ],
    "complex_numbers": [
        (
            ["2 1", "5 6"],
            [
                "7.00+7.00i",
                "-3.00-5.00i",
                "4.00+17.00i",
                "0.26-0.11i",
                "2.24+0.00i",
                "7.81+0.00i",
            ],
        ),
        (
            ["3 1", "5 9"],
            [
                "8.00+10.00i",
                "-2.00-8.00i",
                "6.00+32.00i",
                "0.23-0.21i",
                "3.16+0.00i",
                "10.30+0.00i",
            ],
        ),
        (
            ["1 6", "5 8"],
            [
                "6.00+14.00i",
                "-4.00-2.00i",
                "-43.00+38.00i",
                "0.60+0.25i",
                "6.08+0.00i",
                "9.43+0.00i",
            ],
        ),
    ],
}

from show_employee import show_employee
from sum_and_sub import sum_and_sub
from process_list import process_list
from my_sum import my_sum
from my_sum_argv import my_sum_argv
from files_sort import list_files_by_extension
from file_search import search_file
from email_validation import filter_mail
from average_scores import compute_average_scores


@pytest.mark.parametrize("input_data, expected", test_data["fact"])
def test_fact_it(input_data, expected):
    assert run_script("fact.py", input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data["show_employee"])
def test_show_employee(input_data, expected):
    assert show_employee(*input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data["sum_and_sub"])
def test_sum_and_sub(input_data, expected):
    assert sum_and_sub(*input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data["process_list"])
def test_process_list(input_data, expected):
    assert process_list(input_data) == expected


@pytest.mark.parametrize("input_args, expected", test_data["my_sum"])
def test_my_sum_function(input_args, expected):
    assert my_sum(*input_args) == expected


@pytest.mark.parametrize("input_args, expected", test_data["my_sum_argv"])
def test_my_sum_argv_function(input_args, expected):
    assert my_sum_argv(*input_args) == expected


@pytest.mark.parametrize("input_data, expected", test_data["files_sort"])
def test_files_sort(input_data, expected):
    assert list_files_by_extension(input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data["file_search"])
def test_file_search(input_data, expected):
    assert search_file(input_data).strip().split("\n") == expected


@pytest.mark.parametrize("input_args, expected", test_data["email_validation"])
def test_emails_validation_function(input_args, expected):
    assert sorted(filter_mail(input_args)) == sorted(expected)


@pytest.mark.parametrize("input_args, expected", test_data["fibonacci"])
def test_fibonacci(input_args, expected):
    assert run_script("fibonacci.py", [input_args]) == expected


@pytest.mark.parametrize("input_args, expected", test_data["average_scores"])
def test_average_scores(input_args, expected):
    assert compute_average_scores(input_args) == expected


@pytest.mark.parametrize("input_data, expected", test_data["plane_angle"])
def test_plane_angle(input_data, expected):
    assert run_script("plane_angle.py", input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data["phone_number"])
def test_phone_number(input_data, expected):
    assert run_script("phone_number.py", input_data).split("\n") == expected


@pytest.mark.parametrize("input_data, expected", test_data["people_sort"])
def test_people_sort(input_data, expected):
    assert run_script("people_sort.py", input_data).split("\n") == expected


@pytest.mark.parametrize("input_data, expected", test_data["complex_numbers"])
def test_complex_numbers(input_data, expected):
    assert run_script("complex_numbers.py", input_data).split("\n") == expected
