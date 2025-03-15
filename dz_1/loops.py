n = int(input())
if 1 <= n <= 20:
    for i in range(0, n):
        print(i * i)
else:
    print("Число должно быть в диапазоне от 1 до 20 включительно.")
