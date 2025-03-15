n = int(input())
results = list(
    map(int, list(input().split(" ")))
)  # переносим баллы в список и делаем формат int

set_reslits = list(set(results))  # уникальные результаты
set_reslits.sort(reverse=True)  # сортировка по возрастанию

if len(set_reslits) >= 2:
    print(set_reslits[1])  # второе по величине число
else:
    print("Недостаточно данных")
