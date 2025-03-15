n = int(input())
res = ""
if 1 <= n <= 20:
    for i in range(1, n + 1):
        res += str(i)
else:
    print("Число должно быть в диапазоне от 1 до 20 включительно.")
print(res)
