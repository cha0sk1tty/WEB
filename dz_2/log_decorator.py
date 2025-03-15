from datetime import datetime
import time


def function_logger(file_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Время начала выполнения функции
            start_time = datetime.now()
            start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")

            # Логируем название функции и время вызова
            with open(file_name, "a") as file: # Открываем файл в режиме append
                file.write(f"Функция: {func.__name__}\n") # Записываем название функции
                file.write(f"Время вызова: {start_time_str}\n") # Записываем время вызова
                file.write(
                    f"Аргументы: позиционные аргументы={args}, ключевые аргументы={kwargs}\n"
                ) # Записываем аргументы функции

            # Выполняем функцию и получаем результат
            result = func(*args, **kwargs) # Вызов оригинальной функции с переданными аргументами

            # Время завершения выполнения функции
            end_time = datetime.now()
            end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

            # Время работы функции (в секундах)
            execution_time = (end_time - start_time).total_seconds()

            # Логируем результат, время завершения и время работы
            with open(file_name, "a") as file:
                file.write(
                    f"Возвращаемое значение: {result if result is not None else '-'}\n"
                )
                file.write(f"Время завершения работы функции: {end_time_str}\n")
                file.write(f"Время работы функции: {execution_time:.6f} seconds\n")
                file.write("-" * 40 + "\n")  # Разделитель для удобства чтения
            return result  # Возвращаем результат выполнения функции
        return wrapper  # Возвращаем обернутую функцию
    return decorator  # Возвращаем декоратор


@function_logger("test.log")
def greeting_format(name):
    return f"Hello, {name}!"

# Пример вызова функции
greeting_format("John")
greeting_format("Alice")
greeting_format("Bob")

# * перед аргументом (в данном случае args) позволяет функции принимать произвольное количество позиционных аргументов.
# ** перед аргументом (в данном случае kwargs) позволяет функции принимать произвольное количество именованных (ключевых) аргументов.