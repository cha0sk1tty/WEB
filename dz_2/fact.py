import timeit

#Рекурсивная версия: 0.00000123 сек за вызов
def fact_rec(n):
    if n == 1:
        return 1
    return n * fact_rec(n - 1)

#Итеративная версия: 0.00000062 сек за вызов
def fact_it(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


if __name__ == '__main__':
    n = int(input())
    iterations = 10000
    print(fact_it(n))
    
    # lambda используется для обертки вызова функции без аргументов
    # number=iterations означает выполнение функции указанное количество раз
    #rec_time = timeit.timeit(lambda: fact_rec(n), number=iterations)
    
    #it_time = timeit.timeit(lambda: fact_it(n), number=iterations)

    # Время за 1 вызов = общее время / количество итераций
    #print(f'Рекурсивная версия: {rec_time/iterations:.8f} сек за вызов')
    #print(f'Итеративная версия: {it_time/iterations:.8f} сек за вызов')
