def compute_average_scores(scores: list) -> list:
    # Проверка формата входных данных
    if isinstance(scores[0], str):
        # Если первый элемент — строка, пропускаем его ('n x') и преобразуем остальные строки в числа
        scores_list = [list(map(float, s.split())) for s in scores[1:]]
    else:
        # Если кортежи, преобразуем их в списки 
        scores_list = [list(score) for score in scores]
    
    # Количество предметов
    n = len(scores_list[0])
    
    # Суммирование оценок по каждому предмету
    scores_one_people = [0.0] * n  # Инициализация списка для накопления сумм
    for score in scores_list:
        for i in range(n):
            scores_one_people[i] += score[i]
    
    # Вычисление среднего и округление
    average_scores = [round(total / len(scores_list), 1) for total in scores_one_people]
    
    return average_scores


if __name__ == "__main__":
    # Чтение входных данных
    n, x = map(int, input().split())
    
    # Проверка допустимости значений n и x
    if 0 < n <= 100 and 0 < x <= 100:
        scores = []
        # Чтение оценок x студентов (каждый студент имеет n оценок)
        for _ in range(x):
            scores.append(tuple(map(float, input().split())))
        
        # Вычисление средних оценок
        average_scores = compute_average_scores(scores)
        
        # Вывод результата с одним знаком после запятой
        for avg in average_scores:
            print(f"{avg:.1f}")
    else:
        print("Значения x и n должны быть в диапазоне от 0 до 100 включительно.")