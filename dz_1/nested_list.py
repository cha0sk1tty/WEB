n = int(input())
if 2 <= n <= 5:
    records = []
    for i in range(n):
        record = [0, 0]
        record[0] = input()
        record[1] = input()
        records.append(record)

    scores = []
    for i in range(len(records)):
        scores.append(records[i][1])

    set_scores = list(set(scores))
    set_scores.sort(reverse=True)

    second_score = []

    if len(set_scores) >= 2:
        for i in range(len(records)):
            if set_scores[1] == records[i][1]:
                second_score.append(records[i][0])
    else:
        print("Недостаточно данных.")

    second_score.sort()

    for j in range(len(second_score)):
        print(second_score[j])
else:
    print("Число должно быть в диапазоне от 2 до 5 включительно.")
