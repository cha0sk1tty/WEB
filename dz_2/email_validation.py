def fun(email: str) -> bool:
    valide_symbols_user = "1234567890qwertyuiopasdfghjklzxcvbnm-_"
    valide_symbols_domain = "qwertyuiopasdfghjklzxcvbnm1234567890"
    valide_symbols_extension = "qwertyuiopasdfghjklzxcvbnm"

    # Проверяем наличие одного символа '@' и одного символа '.'
    if email.count("@") != 1 or email.count(".") != 1:
        return False

    # Проверяем корректность username и website
    username, rest = email.split("@") # Разделяем до @ и проверяем если все символы подходят
    if not all(c in valide_symbols_user for c in username.lower()):
        return False

    website, extension = rest.split(".") # Раздеяем по точке и проверяем домен
    if not all(c in valide_symbols_domain for c in website):
        return False

    if not all(c in valide_symbols_extension for c in extension):
        return False

    if len(extension) > 3 or len(extension) == 0:
        return False

    return True

# Фильтрация по функции
def filter_mail(emails):
    return list(filter(fun, emails))


if __name__ == "__main__":
    n = int(input())
    emails = []
    for _ in range(n):
        emails.append(input().strip())

    if len(emails) == 0:
        print("Не введено ни одного адреса.")
    elif n == 0:
        print("должен быть хотя бы 1 адрес.")

    filtered_emails = filter_mail(emails)
    filtered_emails.sort()
    print(filtered_emails)