import timeit


# Обычная функция: 0.00000125 сек за вызов
def process_list(arr):
    if 1 <= len(arr) <= 10**3:
        result = []
        for i in arr:
            if i % 2 == 0:
                result.append(i**2)
            else:
                result.append(i**3)
        return result
    else:
        return "Длина списка должна быть в диапазоне от 1 до 10^3 включительно."


# Функция-генератор: 0.00000110 сек за вызов
def process_list_gen(arr):
    if 1 <= len(arr) <= 10**3:
        results = [i**2 if i % 2 == 0 else i**3 for i in arr]
        return results
    else:
        return "Длина списка должна быть в диапазоне от 1 до 10^3 включительно."


if __name__ == "__main__":
    arr = [4, 13, 52, 47, 89, 45, 61]
    arr1 = [4, 2, 13, 56, 98]
    arr2 = [4, 2, 13, 56, 98, 52, 47, 89, 45, 61]
    arr3 = [4, 2, 13, 56, 102, 123, 65, 84, 96]
    arr4 = [4, 2, 45, 63, 12, 32, 10, 94]
    iterations = 10000

    rec_time = timeit.timeit(lambda: process_list(arr), number=iterations)
    it_time = timeit.timeit(lambda: process_list_gen(arr), number=iterations)

    print(f"Обычная функция: {rec_time/iterations:.8f} сек за вызов")
    print(f"Функция-генератор: {it_time/iterations:.8f} сек за вызов")
    print(process_list(arr))
    print(process_list(arr1))
    print(process_list(arr2))
    print(process_list(arr3))
    print(process_list(arr4))
