def matrix_multiply(A, B, n):
    # Инициализируем результирующую матрицу C нулями
    C = [[0] * n for _ in range(n)]

    # Выполняем умножение матриц строка на столбец
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]

    return C


def main():
    # Считываем размерность матриц
    n = int(input())
    if 2 <= n <= 10:
        # Считываем первую матрицу A и заполняем строки
        A = []
        for _ in range(n):
            row = list(map(int, input().strip().split()))
            A.append(row)

        # Считываем вторую матрицу B и заполняем строки
        B = []
        for _ in range(n):
            row = list(map(int, input().strip().split()))
            B.append(row)

        # Получаем результат умножения матриц
        C = matrix_multiply(A, B, n)

        # Выводим результирующую матрицу
        for row in C:
            print(" ".join(map(str, row)))
    else:
        print("Неверный размер матрицы (должен быть от 2 до 10).")


if __name__ == "__main__":
    main()
