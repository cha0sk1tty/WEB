def count_passengers(time_data, T):
    count = 0
    for entry in time_data:
        entry_time, exit_time = map(int, entry.split())
        # Проверяем, находится ли пассажир в метро в момент T
        if entry_time <= T <= exit_time:
            count += 1
    return count


# Читаем количество пассажиров
N = int(input())

# Считываем данные о времени входа и выхода
time_data = []
for _ in range(N):
    time_data.append(input())

# Считываем время T
T = int(input())

# Получаем количество пассажиров в метро в момент времени T
result = count_passengers(time_data, T)

# Выводим результат
print(result)
