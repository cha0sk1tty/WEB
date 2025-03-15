n = int(input())

if 1 <= n <= 100:
    if n % 2 != 0:
        print("Weird")
    else:
        if n >= 2 and n <= 5:
            print("Not Weird")
        elif n >= 6 and n <= 20:
            print("Weird")
        else:
            print("Not Weird")
else:
    print("Введите число от 1 до 100")
