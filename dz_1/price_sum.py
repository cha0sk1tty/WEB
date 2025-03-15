import csv

def aggregate_expenses(filename: str):
    # Инициализация сумм для каждой категории
    totals = {"Взрослый": 0.0, "Пенсионер": 0.0, "Ребёнок": 0.0}

    # Открываем CSV файл и читаем его содержимое
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Обрабатываем каждую строку в файле
        for row in reader:
            # Суммируем затраты по категориям, заменяя запятые на точки
            for category in totals.keys():
                if category in row:  # Проверяем, есть ли категория в строке
                    totals[category] += float(row[category].replace(",", "."))

    # Вывод суммы для каждой категории, округляя до двух десятичных знаков
    print(f"{totals['Взрослый']:.2f} {totals['Пенсионер']:.2f} {totals['Ребёнок']:.2f}")


if __name__ == "__main__":
    filename = input().strip()
    aggregate_expenses(filename)
