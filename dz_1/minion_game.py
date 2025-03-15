def minion_game(string):
    vowels = "AEIOU"  # гласные буквы
    kevin_score = 0
    stuart_score = 0
    length = len(string)

    for i in range(length):
        if string[i] in vowels:
            kevin_score += length - i  # Подсчет очков Кевина
        else:
            stuart_score += length - i  # Подсчет очков Стюарта

    if kevin_score > stuart_score:
        print(f"Кевин {kevin_score}")
    elif stuart_score > kevin_score:
        print(f"Стюарт {stuart_score}")
    else:
        print("Ничья")


S = input().strip().upper()

if 0 < len(S) <= 10**6:
    minion_game(S)
else:
    print("Строка должна содержать от 1 до 10^6 символов.")
