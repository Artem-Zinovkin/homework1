import json
from tkinter import messagebox
import tkinter as tk

def what_value_to_fill(max_conteyner_1, allowed_values):
    """
    створює словник з однаковими значеннями які вказав користувач, члючі дорівнюють послідовно перерахованим
    контейнерам від 1 до вказаного значення
    :param max_conteyner_1: кількість контенерів у чек-листі
    :return: словник з однаковими значеннями які вказав користувач
    """
    dict_1 = {}
    while True:
        val = input(f"яким значенням заповнити всі ячійки?\n допустмі значення{allowed_values}\n")
        if val.upper().lstrip().rstrip() in allowed_values:
            for i in range(1, max_conteyner_1 + 1):
                dict_1[i] = val
            return dict_1
        else:
            print("невірний ввод ")


def dictionary_1(dictionary: dict, a, allowed_values):
    """
    запрашивает у пользователя и при необходимости меняет значение на введеное если просто пробел оставляет старое
    если + можно ввести диапазон если остальное вводим поштучно
    :param dictionary: словарь с всеми одинаковыми значениями
    :return: новый словарь
    """

    while True:
        print("'Enter' - залишити як є, '+' - ввести діапазон, '-' - повернутися до контєйнеру, 'допустиме значенн'")
        for kay, value in list(dictionary.items())[a:]:
            value_1 = input(f"введіть нове значення   №{kay} = {value}  ")
            if len(value_1) == 0:
                pass
            elif value_1 == "+":
                while True:
                    value_2 = input("яке значення потрібно буде ввести? ")
                    if value_2 in allowed_values:
                        break
                    else:
                        print(f"не коректний ввід!!! допустимі значення {allowed_values}")
                        continue
                while True:
                    po_kay = input("по який номер? ")
                    try:
                        po_kay = int(po_kay)
                        break
                    except:
                        print("некоректний ввод!!! потрібна цифра")
                        continue
                if int(po_kay) < kay:
                    print("введенно значення менше можливого")
                    po_kay = kay
                if int(po_kay) >= max(dictionary):
                    if int(po_kay) == max(dictionary):
                        return dictionary, 200
                    print(f"перевищєн ліміт контйнерів максимальна кількість {max(dictionary)} шт")
                    po_kay = kay - 1
                for i in range(int(kay), int(po_kay) + 1):
                    dictionary[i] = value_2
                return dictionary, po_kay
            elif value_1 == "-":
                f = input("к какому контейнеру вернуться? ")
                return dictionary, int(f) - 1
            else:
                dictionary[kay] = value_1
            if kay >= max(dictionary):
                return dictionary, 200




def values_in_chek_list(minrow: int, maxrow, sheet_2, dictinary_last: dict, cell_number):
    """
    записує отриманий словник в ексель файл
    :param minrow: значення першого рядку з кого починаємо запис
    :param maxrow: значення останнього рядку яким закінчуємо запис
    :param sheet_2: сторінка ексель файлу
    :param dictinary_last: словник який переносимо в екель файл

    """

    for row in range(minrow, maxrow):
        for i in range(0, 30):
            if sheet_2[row][i].value is not None:
                if sheet_2[row][i].value in dictinary_last:
                    sheet_2[row][i + cell_number].value = dictinary_last[sheet_2[row][i].value]


def baza_in_json(predpr, vidpovidalniy, how_dk_1_2, how_dk_3):
    def save():
        with open("Baza.json", mode="w") as fp:
            file["Baza"].append({"pre dpr": predpr, "vidpovidalniy": vidpovidalniy, "how_dk_1_2": how_dk_1_2,
                                 "how_dk_3": how_dk_3})
            json.dump(file, fp, indent=2, ensure_ascii=False)

    try:
        file = json.load(open(f"Baza.json", mode="r"))
        v = []
        for i in file["Baza"]:
            v.append(i['pre dpr'])
        print(f'vvv= {v}')
        if predpr in v:
            print(f"file['Baza']={file['Baza']}")
            print(f'predpr = {predpr}')
            print(f"v.index(predpr)=={v.index(predpr)}")
            s_1 = messagebox.askokcancel("Увага!!!", "Підприємство вже є в базі перезаписати?")
            if s_1:
                file['Baza'].pop(v.index(predpr))
                save()
        else:
            save()
    except:
        with open(f"Baza.json", "a") as fp:
            file = {"Baza": [{"pre dpr": predpr, "vidpovidalniy": vidpovidalniy, "how_dk_1_2": how_dk_1_2,
                              "how_dk_3": how_dk_3}]}
            json.dump(file, fp, indent=2, ensure_ascii=False)


def in_json(predpr, month_1, number, baryer, diction, year, krisi_teritori, mishi_teritori):
    """
    записує данні в джейсон файл
    :param predpr: назва підпримства
    :param month_1: місяць обслуговування
    :param number: дата обслуговування
    :param baryer: барєр
    :param diction: введені користувачем данні
    :return:
    """

    try:
        file = json.load(open(f"test_file.json", mode="r"))
        with open("test_file.json", mode="w") as fp:
            file["DR"].append({"year": year, "pre dpr": predpr, "month": month_1,
                               "number": number, "barer": baryer,"krisi_teritori": krisi_teritori,
                               "mishi_teritori": mishi_teritori,"value": diction})
            # сделать проверку если значения словаря пустые не записывать
            json.dump(file, fp, indent=2, ensure_ascii=False)
    except:
        with open(f"test_file.json", "a") as fp:
            file = {"DR": [{"year": year, "pre dpr": predpr, "month": month_1,
                            "number": number, "barer": baryer,
                            "value": diction}]}
            json.dump(file, fp, indent=2, ensure_ascii=False)


def final_operation(number: str, max_day_1, sheet_1, month_date_1,
                    max_conteyner, allawed_values, predpr, month_1,
                    barer, minrow, maxrow, a1, a2, a3, a4, a5, a6, cell_number_1):
    """
    збирає в себе роботу всіх функцій
    :number: дата виходу вводиться користувачем
    :ell_number_1: значення яке вказує в яку ячейку записувати значення залежить від тоо який вихід
    :return:
    """
    while True:

        if len(number.rstrip().lstrip()) == 0:
            break
        try:
            number_1 = int(number)
        except:
            print("Потрібно бути тільки цира!!!")
            continue
        if int(number_1) in max_day_1:
            sheet_1[a1] = sheet_1[a2] = sheet_1[a3] = sheet_1[a4] = sheet_1[a5] = sheet_1[a6] \
                = f"{number}.{month_date_1}"

            d = what_value_to_fill(max_conteyner, allawed_values)
            pokey = 0
            while pokey != 200:
                dictionary_2, pokey = dictionary_1(dictionary=d, a=int(pokey), allowed_values=allawed_values)
                a = int(pokey)
            in_json(predpr, month_1, number_1, barer, dictionary_2)
            values_in_chek_list(minrow=minrow, maxrow=maxrow, sheet_2=sheet_1, dictinary_last=dictionary_2,
                                cell_number=cell_number_1)
            break
        else:
            print("некорректна дата!!!")
