a = int(input())
b = int(input())

if 1 <= a <= 10**10 and 1 <= b <= 10**10:
    print(a + b)
    print(a - b)
    print(a * b)
else:
    print("Числа должны быть в диапазоне от 1 до 10^10")
