import operator

def person_lister(f):
    def inner(people):
        # Сортируем людей по возрасту (третий элемент в списке, индекс 2)
        people.sort(key=lambda x: int(x[2]))
        # Применяем функцию форматирования к каждому человеку
        return [f(person) for person in people]
    return inner

@person_lister
def name_format(person):
    return ("Mr. " if person[3] == "M" else "Ms. ") + person[0] + " " + person[1]

if __name__ == '__main__':
    n = int(input())
    people = [input().split() for i in range(n)]
    print(*name_format(people), sep='\n')
