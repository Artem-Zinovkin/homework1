# конвертация градусов в радианы
import math


def degrees(a):
    a = int(a)
    return round((a * math.pi) / 180, 6)


b = degrees(a=float(input("Введите число в градусах ")))
print(F"число в радианах = {b} ")
