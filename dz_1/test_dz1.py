import subprocess
import pytest

INTERPRETER = "python"


def run_script(filename, input_data=None):
    filepath = f"./dz_1/{filename}"
    proc = subprocess.run(
        [INTERPRETER, filepath],
        input="\n".join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.stdout.strip()


test_data = {
    "python_if_else": [
        ("1", "Weird"),
        ("4", "Not Weird"),
        ("3", "Weird"),
        ("6", "Weird"),
        ("22", "Not Weird"),
    ],
    "arithmetic_operators": [
        (["1", "2"], ["3", "-1", "2"]),
        (["10", "5"], ["15", "5", "50"]),
        (["0", "5"], ["Числа должны быть в диапазоне от 1 до 10^10"]),
    ],
    "division": [
        (["4", "2"], ["2", "2.0"]),
        (["10", "6"], ["1", "1.6666666666666667"]),
        (["10", "0"], ["На ноль делить нельзя"]),
    ],
    "loops": [
        (["3"], ["0", "1", "4"]),
        (["5"], ["0", "1", "4", "9", "16"]),
        (["22"], ["Число должно быть в диапазоне от 1 до 20 включительно."]),
        (["-5"], ["Число должно быть в диапазоне от 1 до 20 включительно."]),
    ],
    "print_function": [
        (["5"], "12345"),
        (["10"], "12345678910"),
        (["0"], "Число должно быть в диапазоне от 1 до 20 включительно."),
    ],
    "second_score": [
        (["5", "10 10 10 10 10"], "Недостаточно данных"),
        (["7", "100 99 100 98 99 98 97"], "99"),
        (["3", "5 5 5"], "Недостаточно данных"),
    ],
    "nested_list": [
        (
            ["4", "Anna", "4", "Borya", "4", "Sergey", "4", "Ivan", "5"],
            "Anna\nBorya\nSergey",
        ),
        (
            ["7", "Anna", "6", "Borya", "3", "Sergey", "1", "Egor", "2"],
            "Число должно быть в диапазоне от 2 до 5 включительно.",
        ),
        (["2", "Ivan", "5", "Alexey", "4"], "Alexey"),
    ],
    "lists": [
        (["7", "insert 0 5", "insert 1 10", "print"], "[5, 10]"),
        (["4", "append 6", "pop", "print"], "[]"),
        (["6", "append 10", "append 20", "remove 10", "print"], "[20]"),
    ],
    "swap_case": [
        ("Hello World", "hELLO wORLD"),
        ("123abcDEF", "123ABCdef"),
        ("", ""),
        ("!@#$%^&*", "!@#$%^&*"),
    ],
    "split_and_join": [
        ("Hello World", "Hello-World"),
        (
            "   Hello   How   are you   ",
            "Hello-How-are-you",
        ),
        (
            "Hiii       What's a lovely day!   ",
            "Hiii-What's-a-lovely-day!",
        ),
        ("", ""),
        ("SingleWord", "SingleWord"),
    ],
    "max_word": [
        (["dz_1/example.txt"], "сосредоточенности"),
        (["dz_1/example_2.txt"], "распростился"),
        (["dz_1/example_3.txt"], "Файл пуст."),
    ],
    "price_sum": [
        (["dz_1/products.csv"], "6842.84 5891.06 0.00"),
    ],
    "anagram": [
        (["listen", "silent"], "YES"),
        (["apple", "papet"], "NO"),
        (["a", "a"], "YES"),
        (["a", "b"], "NO"),
        (["abcd", "ab"], "NO"),
    ],
    "metro": [
        (["5", "30 35", "15 26", "25 75", "30 59", "12 61", "35"], "4"),
        (["4", "15 20", "20 35", "41 56", "10 60", "21"], "2"),
    ],
    "minion_game": [
        (["Banana"], "Стюарт 12"),
        ([" "], "Строка должна содержать от 1 до 10^6 символов."),
        (["A"], "Кевин 1"),
    ],
    "is_leap": [
        (["1901"], "False"),
        (["202"], "Год должен быть в диапазоне от 1900 до 10^5."),
        (["2024"], "True"),
    ],
    "happiness": [
        (
            [
                "12 5",
                "16 41 52 37 89 41 25 67 12 23 45 65",
                "16 20 52 23 40",
                "17 41 65 47 12",
            ],
            "-1",
        ),
        (["4 2", "10 20 30 40", "10 30", "20 40"], "0"),
        (["3 3", "100 200 300", "100 200 300", "400 500 600"], "3"),
        (["3 3", "10 20 30", "40 50 60", "10 20 30"], "-3"),
        (["1 1", "100", "200", "300"], "0"),
    ],
    "pirate_ship": [
        (
            [
                "500 4",
                "giri 100 1500",
                "TV 70 20000",
                "bed 400 15000",
                "sofa 150 30000",
            ],
            "TV 70.00 20000.00\nsofa 150.00 30000.00\nbed 280.00 10500.00",
        ),
        (
            [
                "200 6",
                "стул 56 250",
                "стол 120 560",
                "принтер 30 1500",
                "ручка 1 5",
                "ноутбук 25 20000",
                "колонки 50 5000",
            ],
            "ноутбук 25.00 20000.00\nколонки 50.00 5000.00\nпринтер 30.00 1500.00\nручка 1.00 5.00\nстол 94.00 438.67",
        ),
    ],
    "matrix_mult": [
        (["2", "1 2", "3 4", "5 6", "7 8"], "19 22\n43 50"),
        (["1"], "Неверный размер матрицы (должен быть от 2 до 10)."),
        (["11"], "Неверный размер матрицы (должен быть от 2 до 10)."),
    ],
}


def test_hello_world():
    assert run_script("hello_world.py") == "Hello, world!"


@pytest.mark.parametrize("input_data, expected", test_data["python_if_else"])
def test_python_if_else(input_data, expected):
    assert run_script("python_if_else.py", [input_data]) == expected


@pytest.mark.parametrize("input_data, expected", test_data["arithmetic_operators"])
def test_arithmetic_operators(input_data, expected):
    assert run_script("arithmetic_operators.py", input_data).split("\n") == expected


@pytest.mark.parametrize("input_data, expected", test_data["division"])
def test_division(input_data, expected):
    assert run_script("division.py", input_data).split("\n") == expected


@pytest.mark.parametrize("input_data, expected", test_data["loops"])
def test_loops(input_data, expected):
    assert run_script("loops.py", input_data).split("\n") == expected


@pytest.mark.parametrize("input_data, expected", test_data["print_function"])
def test_print_function(input_data, expected):
    assert run_script("print_function.py", input_data).strip() == expected


@pytest.mark.parametrize("input_data, expected", test_data["second_score"])
def test_second_score(input_data, expected):
    assert run_script("second_score.py", input_data).strip() == expected


@pytest.mark.parametrize("input_data, expected", test_data["nested_list"])
def test_nested_list(input_data, expected):
    assert run_script("nested_list.py", input_data).strip() == expected


@pytest.mark.parametrize("input_data, expected", test_data["lists"])
def test_lists(input_data, expected):
    assert run_script("lists.py", input_data).strip() == expected


@pytest.mark.parametrize("input_data, expected", test_data["swap_case"])
def test_swap_case(input_data, expected):
    assert run_script("swap_case.py", [input_data]).strip() == expected


@pytest.mark.parametrize("input_data, expected", test_data["split_and_join"])
def test_split_and_join(input_data, expected):
    assert run_script("split_and_join.py", [input_data]).strip() == expected


@pytest.mark.parametrize("input_data, expected", test_data["max_word"])
def test_max_word(input_data, expected):
    assert run_script("max_word.py", input_data).strip() == expected


@pytest.mark.parametrize("input_data, expected", test_data["price_sum"])
def test_price_sum(input_data, expected):
    assert run_script("price_sum.py", input_data).strip() == expected


@pytest.mark.parametrize("input_data, expected", test_data["anagram"])
def test_anagram(input_data, expected):
    assert run_script("anagram.py", input_data).strip() == expected


@pytest.mark.parametrize("input_data, expected", test_data["metro"])
def test_metro(input_data, expected):
    assert run_script("metro.py", input_data).strip() == expected


@pytest.mark.parametrize("input_data, expected", test_data["minion_game"])
def test_minion_game(input_data, expected):
    assert run_script("minion_game.py", input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data["is_leap"])
def test_is_leap(input_data, expected):
    assert run_script("is_leap.py", input_data).strip() == expected


@pytest.mark.parametrize("input_data, expected", test_data["happiness"])
def test_happiness(input_data, expected):
    assert run_script("happiness.py", input_data).strip() == expected


@pytest.mark.parametrize("input_data, expected", test_data["pirate_ship"])
def test_pirate_ship(input_data, expected):
    assert run_script("pirate_ship.py", input_data).strip() == expected


@pytest.mark.parametrize("input_data, expected", test_data["matrix_mult"])
def test_matrix_mult(input_data, expected):
    assert run_script("matrix_mult.py", input_data).strip() == expected
