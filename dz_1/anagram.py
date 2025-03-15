def can_form_permutation(str1: str, str2: str) -> str:
    # Если длины строк не равны, они не могут быть анаграмами
    if len(str1) != len(str2):
        return "NO"

    char_count = {}

    # Подсчитываем количество символов в первой строке
    for char in str1:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    # Вычитаем количество символов, найденных во второй строке
    for char in str2:
        if char in char_count:
            char_count[char] -= 1
            if char_count[char] < 0:
                return "NO"
        else:
            return "NO"

    # Если все счетчики символов равны нулю, строки являются перестановками друг друга
    return "YES"


# Ввод строк
input_str1 = input().strip()
input_str2 = input().strip()

# Проверяем возможность перестановки
result = can_form_permutation(input_str1, input_str2)

# Вывод результата
print(result)
