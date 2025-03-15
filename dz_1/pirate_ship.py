class Cargo:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value
        self.value_per_weight = (
            value / weight
        )  # Считаем ценность на единицу веса для сортировки


def main():
    # Считывание ввода
    n, m = map(int, input().split())

    cargos = []

    for _ in range(m):
        data = input().split()
        name = data[0]
        weight = int(data[1])
        value = int(data[2])
        cargos.append(Cargo(name, weight, value))

    # Сортируем грузы по ценности на единицу веса в порядке убывания
    cargos.sort(key=lambda x: x.value_per_weight, reverse=True)

    total_weight = 0
    result = []

    for cargo in cargos:
        if total_weight < n:  # Пока есть место на судне
            if total_weight + cargo.weight <= n:
                # Если помещается целиком
                total_weight += cargo.weight
                result.append((cargo.name, cargo.weight, cargo.value))
            else:
                # Если помещается частично
                remaining_weight = n - total_weight  # оставшееся место на судне
                partial_value = (
                    remaining_weight / cargo.weight
                ) * cargo.value  # расчет стоимости части груза
                total_weight += remaining_weight
                result.append((cargo.name, remaining_weight, partial_value))

    # Вывод результата
    for name, weight, value in result:
        print(f"{name} {weight:.2f} {value:.2f}")


if __name__ == "__main__":
    main()
