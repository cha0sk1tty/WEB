cube = lambda x: x**3 # Безымянная функция возведения в куб


def fibonacci(n):
    fib = []
    a, b = 0, 1
    for _ in range(n):
        fib.append(a)
        a, b = b, a + b
    return fib


if __name__ == "__main__":
    n = int(input())
    if 1 <= n <= 15:
        result = list(map(cube, fibonacci(n)))
        print(result)
    else:
        print("n должно быть в диапазоне от 1 до 15.")
