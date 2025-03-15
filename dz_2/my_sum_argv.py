import sys


def my_sum_argv(*args):
    return sum(args)


if __name__ == '__main__':
    # Проверяем, переданы ли аргументы командной строки
    if len(sys.argv) > 1:
        numbers = map(int, sys.argv[1:]) # Преобразуем все аргументы командной строки (кроме первого) в целые числа 
        result = my_sum_argv(*numbers) # Вызываем функцию my_sum с распакованными аргументами и сохраняем результат
        print(result)
    else:
        # Если аргументы не переданы, запрашиваем ввод чисел у пользователя
        number = [int(num) for num in input('Введите числа через пробел: ').split()]
        result = my_sum_argv(*number)
        print(result)
