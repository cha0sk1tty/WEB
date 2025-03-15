def my_sum(*args):
    # Проверяем, все ли переданные значения являются числами (int или float)
    if all(isinstance(arg, (int, float)) for arg in args):
        return sum(args)
    else:
        raise ValueError("Все аргументы должны быть действительными числами.")

if __name__ == "__main__":
    print(my_sum(1, 2, 3))          # Вывод: 6
    print(my_sum(1.5, 2.5, 3.0))    # Вывод: 7.0
    print(my_sum(1, 2.2, 3.3, 4))   # Вывод: 10.5
