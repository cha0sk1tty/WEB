import os
import sys

def list_files_by_extension(directory):
    items = os.listdir(directory) # Получаем список всех элементов в указанной директории
    files = [item for item in items if os.path.isfile(os.path.join(directory, item))] # Формируем список файлов, исключая подкаталоги
    files.sort(key=lambda x: (os.path.splitext(x)[1], x))  # Сортировка по расширению и имени
    return files # Возвращаем отсортированный список файлов

if __name__ == "__main__":
    # Проверяем, что передано ровно два аргумента (имя скрипта и директория)
    if len(sys.argv) != 2:
        print("Использование: python files_sort.py <директория>")
    else:
        directory = sys.argv[1] # Извлекаем директорию из аргумента командной строки
        if os.path.isdir(directory): # Проверяем, является ли указанный путь директорией
            sorted_files = list_files_by_extension(directory) # Получаем отсортированный список файлов
            # Печатаем каждый файл из отсортированного списка
            for file in sorted_files:
                print(file)
        else:
            print(f"Ошибка: '{directory}' не является директорией.")