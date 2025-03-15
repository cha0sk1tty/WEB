import math

# Определяем класс точек
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # Вычитание
    def __sub__(self, no):
        return Point(self.x - no.x, self.y - no.y, self.z - no.z)

    # Умножение
    def dot(self, no):
        return self.x * no.x + self.y * no.y + self.z * no.z

    # Скалярное произведение
    def cross(self, no):
        return Point(
            (self.y * no.z - self.z * no.y),
            (self.z * no.x - self.x * no.z),
            (self.x * no.y - self.y * no.x),
        )
        
    # Модуль точки
    def absolute(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)


def plane_angle(a: Point, b: Point, c: Point, d: Point):
    ab = b - a
    bc = b - c
    cd = c - d
    x = ab.cross(bc)
    y = bc.cross(cd)
    cos = x.dot(y) / (x.absolute() * y.absolute())
    return math.degrees(math.acos(cos))


if __name__ == "__main__":
    a = Point(*map(float, input().split()))
    b = Point(*map(float, input().split()))
    c = Point(*map(float, input().split()))
    d = Point(*map(float, input().split()))
    print(plane_angle(a, b, c, d))
