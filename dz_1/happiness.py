def calculate_mood(array, set_a, set_b):
    mood = 0

    # Пройти по каждому числу в массиве
    for number in array:
        if number in set_a:
            mood += 1  # Увеличиваем настроение
        elif number in set_b:
            mood -= 1  # Уменьшаем настроение

    return mood


# Чтение входных данных
n, m = map(int, input().split())

# Проверка ограничения на n и m
if not (1 <= n <= 10**5) or not (1 <= m <= 10**5):
    print("n и m должны быть в диапазоне от 1 до 10^5.")

# Считываем основной массив
array = list(map(int, input().split()))

# Проверка на размер массива
if len(array) != n:
    print("Размер основного массива не соответствует n.")

# Считываем множества A и B
set_a = set(map(int, input().split()))
set_b = set(map(int, input().split()))

# Проверка размерности множеств A и B
if len(set_a) != m or len(set_b) != m:
    print("Размеры множеств A и B должны быть равны m.")

# Проверка ограничений на значения элементов
for num in array + list(set_a) + list(set_b):
    if not (1 <= num <= 10**9):
        print("Элементы должны быть в диапазоне от 1 до 10^9.")

# Вычисление и вывод конечного настроения
final_mood = calculate_mood(array, set_a, set_b)
print(final_mood)
