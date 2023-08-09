import MySQLdb
from datetime import datetime


# перевод даты в таймстам
def data_in_timestamp(_data):
    _timestamp = datetime.fromisoformat(_data).timestamp()
    return _timestamp 


# подключение и отключение к бд
def connection_bd():
    conn = MySQLdb.connect("dezeltor.mysql.tools",
                           "dezeltor_pestcontrol",
                           "lala280508",
                           "dezeltor_pestcontrol")

    return conn


# показать всех специалистов из бд
def show_specialists():
    conn = connection_bd()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM `spesialisti`""")
    row = cursor.fetchall()
    return row


# добавить специалиста
def add_spesialist(name, surnemes):
    conn = connection_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""INSERT INTO spesialisti (name, surnames) VALUES ('{name}','{surnemes}')""")
    except MySQLdb.IntegrityError:
        return False
    conn.commit()
    conn.close()


# удалить специалиста
def del_spesialist(_id):
    conn = connection_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""DELETE FROM `spesialisti` WHERE `spesialisti`.`idspesialisti` = {_id}""")
    except MySQLdb.ProgrammingError:
        return False
    conn.commit()
    conn.close()


# получаем id из таблицы предприятий
def receive_id(request):
    conn = connection_bd()
    cursor = conn.cursor()
    cursor.execute(request)
    return cursor.fetchall()[0][0]


# запись данных введенных в ручную в таблицу scan_dk и grizuni_na_territorii
def write_scan_dk(_predpr, _diction, _krisi_teritori, _mishi_teritori, _combo_month, _baryer):
    krisi_teritori = ("Криса", _krisi_teritori)
    mishi_teritori = ("Миша", _mishi_teritori)

    conn = connection_bd()
    cursor = conn.cursor()

    _idbaza_pidpriemstv = receive_id(f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
     "{_predpr}" """)

    # запись в табл грызуни на территории
    for i in [krisi_teritori, mishi_teritori]:
        cursor.execute(f"""INSERT INTO grizuni_na_territorii (vid_grizuna, kilkist, idbaza_pidpriemstv, time) 
                            VALUES ('{i[0]}','{i[1]}','{_idbaza_pidpriemstv}', STR_TO_DATE('{_combo_month}',
                             '%d-%m-%Y'))""")

    for number_dk, value_dk in _diction.items():
        if value_dk == "":
            pass
        else:
            _idbaza_obladnanya = receive_id(f"""SELECT  idbaza_obladnanya FROM baza_obladnanya
                        WHERE  number_obladnanya = '{number_dk}' AND idbaza_pidpriemstv ='{_idbaza_pidpriemstv}' 
                        AND barier ='{_baryer}' """)

            cursor.execute(f"""INSERT INTO scan_dk (time, value_dk, idbaza_obladnanya, idbaza_pidpriemstv, idspestalisti) 
                                        VALUES (STR_TO_DATE('{_combo_month}','%d-%m-%Y'),'{value_dk}','{_idbaza_obladnanya}',
                                        '{_idbaza_pidpriemstv}', '1')""")
    conn.commit()
    conn.close()


# получение данных из БД таблица skan_dk для формирования чек-листа
def value_from_db_for_cheklist(_month, _year, _barier, _predpr):
    conn = connection_bd()
    cursor = conn.cursor()

    _idbaza_pidpriemstv = receive_id(f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
         "{_predpr}" """)

    namber = []
    month_list = []
    value = []

    cursor.execute(f"""SELECT scan_dk.value_dk, DAY(time), MONTH(time),YEAR(time), baza_obladnanya.number_obladnanya
                     FROM scan_dk JOIN baza_obladnanya
                     ON scan_dk.idbaza_obladnanya = baza_obladnanya.idbaza_obladnanya 
                     WHERE MONTH(time) = '{_month}' AND YEAR(time) = '{_year}' AND baza_obladnanya.barier = '{_barier}' 
                     AND scan_dk.idbaza_pidpriemstv = {_idbaza_pidpriemstv}
                    """)

    row = cursor.fetchall()
    for value_dk, day, month, year, number in row:
        namber.append(str(day))
        month_list.append(str(month))

    namber = sorted(list(set(namber)))
    # month_list = list(set(month_list))

    for i in namber:
        value_test = []
        value_test.clear()
        test_dict = {}
        test_dict.clear()
        cursor.execute(f"""SELECT scan_dk.value_dk, DAY(time), MONTH(time),YEAR(time), baza_obladnanya.number_obladnanya
                     FROM scan_dk JOIN baza_obladnanya
                     ON scan_dk.idbaza_obladnanya = baza_obladnanya.idbaza_obladnanya 
                     WHERE MONTH(time) = '{_month}' AND YEAR(time) = '{_year}' AND DAY(time) = '{i}'
                      AND baza_obladnanya.barier = '{_barier}' 
                     AND scan_dk.idbaza_pidpriemstv = {_idbaza_pidpriemstv}
                    """)
        row = cursor.fetchall()

        for value_dk, *args, number_dk in row:
            value_test.append({str(number_dk): value_dk})

        for _ in value_test:
            test_dict.update(_)

        value.append({str(i): test_dict})

    conn.close()

    return namber, month_list, value


# получение данных из БД таблица грызуны на территории для формирования чек-листа и сразу считает обшее количество для
#  отчета

def value_from_db_grizuni_for_cheklist(_month, _year, _predpr):
    conn = connection_bd()
    cursor = conn.cursor()

    _idbaza_pidpriemstv = receive_id(f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
            "{_predpr}" """)
    date = []
    cursor.execute(f"""SELECT  DAY(time) FROM grizuni_na_territorii
                         WHERE MONTH(time) = '{_month}' AND YEAR(time) = '{_year}' 
                         AND idbaza_pidpriemstv = {_idbaza_pidpriemstv}""")
    row = cursor.fetchall()
    for i in row:
        date.append(i[0])

    date = (sorted(list(set(date))))
    value = []
    kris_za_mes = 0
    mish_za_mes = 0

    for i in date:
        krisa = 0
        misha = 0

        cursor.execute(f"""SELECT  vid_grizuna, kilkist FROM grizuni_na_territorii
                             WHERE MONTH(time) = '{_month}' AND YEAR(time) = '{_year}'  AND DAY(time) = '{i}'
                             AND idbaza_pidpriemstv = {_idbaza_pidpriemstv}""")
        row = cursor.fetchall()
        for j in row:
            if j[0] == 'Миша':
                misha += int(j[1])
            if j[0] == 'Криса':
                krisa += int(j[1])
        kris_za_mes += krisa
        mish_za_mes += misha
        value.append({str(i).zfill(2): f"K-{krisa},M-{misha}"})
    conn.close()
    vsego_grizunov_za_mes = [['M-', mish_za_mes], ['K-', kris_za_mes]]

    return value, vsego_grizunov_za_mes


# получение данных из БД таблица skan_dk для формирования отчета
def value_from_db_for_zvit(_month, _year, _predpr):
    conn = connection_bd()
    cursor = conn.cursor()

    _idbaza_pidpriemstv = receive_id(f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
         "{_predpr}" """)

    _bariers = ['I - II', 'III']
    date = []
    value_I_II = []
    value_III = []

    _month = [str(_month).zfill(2)]
    cursor.execute(f"""SELECT  DAY(time) FROM grizuni_na_territorii
                         WHERE MONTH(time) = '{_month[0]}' AND YEAR(time) = '{_year}'
                         AND idbaza_pidpriemstv = {_idbaza_pidpriemstv}""")
    row = cursor.fetchall()
    for i in row:
        date.append(str(i[0]).zfill(2))

    date = (sorted(list(set(date))))
    print(date)
    print(_month)
    for _barier in _bariers:
        for i in date:
            value_test = []
            value_test.clear()
            test_dict = {}
            test_dict.clear()
            cursor.execute(f"""SELECT scan_dk.value_dk, baza_obladnanya.number_obladnanya,
                    baza_obladnanya.barier, baza_obladnanya.idbaza_pidpriemstv
                    FROM scan_dk JOIN baza_obladnanya
                    ON scan_dk.idbaza_obladnanya = baza_obladnanya.idbaza_obladnanya
                    WHERE MONTH(time) = '{_month[0]}' AND YEAR(time) = '{_year}' AND DAY(time) = '{i}' 
                    AND baza_obladnanya.barier = '{_barier}' """)
            row = cursor.fetchall()
            for value_dk, number_dk, *args in row:
                value_test.append({str(number_dk): value_dk})

            for _ in value_test:
                test_dict.update(_)
            if _barier == 'I - II':
                value_I_II.append({str(i): test_dict})
            else:
                value_III.append({str(i): test_dict})
    conn.close()
    return date, _month, value_I_II, value_III


#достает из бд количество контейнеров по первому второму барьеру
def count_dk_1_2(_pidpr):
    conn = connection_bd()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT kilkist_dk_1_2 FROM baza_pidpriemstv WHERE nazva_pidriemstva = "{_pidpr}" """)

    row = cursor.fetchall()
    conn.close()
    return row[0][0]

#достает из бд количество контейнеров по третьему барьеру
def count_dk_3(_pidpr):
    conn = connection_bd()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT kilkist_dk_3 FROM baza_pidpriemstv WHERE nazva_pidriemstva = "{_pidpr}" """)

    row = cursor.fetchall()
    conn.close()
    return row[0][0]


if __name__ == '__main__':
    pass
