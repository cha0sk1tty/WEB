def wrapper(f):
    def fun(l):
        formatted_numbers = []
        for number in l:
            number = number.strip()
            if len(number) not in (10, 11) or not (number.startswith(('8', '7', '0', '+7', '9'))):
                return "Неверный формат номера телефона"  # Возвращаем ошибку как одну строку

            # Если номер длиной 10 символов, добавляем +7 в начало
            if len(number) == 10:
                number = "+7" + number

            # Форматируем номер
            if number.startswith('8') or number.startswith('0') or number.startswith('7'):
                formatted = f"+7 ({number[1:4]}) {number[4:7]}-{number[7:9]}-{number[9:]}"
            elif number.startswith('+7'):
                formatted = f"+7 ({number[2:5]}) {number[5:8]}-{number[8:10]}-{number[10:]}"
            formatted_numbers.append(formatted)
        return sorted(formatted_numbers)
    return fun


@wrapper
def sort_phone(l):
    return l


if __name__ == "__main__":
    n = int(input())
    l = [input() for _ in range(n)]
    result = sort_phone(l)
    if isinstance(result, str):  # Если результат — строка (ошибка)
        print(result)  # Выводим ошибку как одну строку
    else:
        print(*result, sep="\n")  # Иначе выводим отформатированные номера
        
"""3
07895462130
89875641230
9195969878"""