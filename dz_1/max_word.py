import re

name = str(input().strip())
# Открываем файл и читаем его содержимое
with open(name, "r", encoding="utf-8") as file:
    text = file.read()

# Если нет слов, ничего не выводим
if not text:
    print("Файл пуст.")
    exit()

max_length = -1000000
for symbol in ",.-!?:":
    text = text.replace(symbol, " ")
words = text.split()

# Определяем максимальную длину слов
max_length = len(max(words, key=len))

# Собираем все слова максимальной длины
longest_words = [word for word in words if len(word) == max_length]
for _ in longest_words:
    print(_)
