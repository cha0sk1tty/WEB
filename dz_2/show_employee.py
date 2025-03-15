def show_employee(name: str, salary: str = '100000') -> str:
    return f"{name}: {salary} ₽"


if __name__ == "__main__":
    print(show_employee("John Doe", '30000'))
