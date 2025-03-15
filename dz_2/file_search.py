import os
import sys


def search_file(filename):
    current_dir = (
        os.getcwd()
    )  # Получаем текущий рабочий каталог, в котором запускается скрипт
    output = []  # Список для хранения результата поиска

    # Используем os.walk для рекурсивного обхода директорий
    for root, _, files in os.walk(current_dir):
        # Проверяем, есть ли файл с нужным именем в текущем каталоге
        if filename in files:
            # Формируем полный путь к файлу
            file_path = os.path.join(root, filename)
            try:
                # Открываем файл для чтения с указанием кодировки UTF-8
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = [] # Список для хранения строк файла
                    for _ in range(5):
                        line = f.readline() # Читаем одну строку из файла
                        if not line:  # Если строка пустая (достигнут конец файла)
                            break # Прерываем цикл, если файла больше нет
                        lines.append(line.strip())
                    # Формируем строку с выводом
                    output.append(f"\nФайл расположен в: {root}")
                    output.append("\nДанные файла (5 строк):")
                    output.append("\n".join(lines))
                    return "\n".join(output)  # Возвращаем результат как строку
            except Exception as e:
                output.append(f"\nФайл расположен: {root}")
                output.append(f"Ошибка при чтении: {str(e)}")
                return "\n".join(output)

    return f"Файл {filename} не найден"


if __name__ == "__main__":
    # Проверяем, что передано ровно два аргумента (имя скрипта и имя файла)
    if len(sys.argv) != 2:
        print("Использование: python file_search.py <имя_файла>", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1] # Извлекаем имя файла из аргумента командной строки
    result = search_file(filename)
    print(result)
