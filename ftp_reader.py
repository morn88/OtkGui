from configparser import ConfigParser
import sqlite3
import os
import shutil


def read_config(filename, section):
    """
    Чтение настроек из файла
    :param filename: Имя файла настроек
    :param section: Название секции
    :return: Папка программы и параметры
    """

    parser = ConfigParser()
    parser.read(filename)

    # Получаем секцию
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        print('Section not found...')
    return db


def parse_csv_file(file_csv, path):
    f = open(os.path.join(path, file_csv), 'r')
    list_of_request = []

    for line in f:
        list_line = line.split(sep=',')

        if list_line[0] != '"Date"':
            date, time, cass, form_number, cell_number, set_kn, kn1, kn2, kn3, kn4, rs1, rs2, rs3, rs4, mi, ma = list_line
            date = str(date[1:-1]).split(sep='/')
            date = '20' + date[0] + '-' + date[1] + '-' + date[2]
            time = time[1:-1]
            form_number = int(form_number[1:-1])
            cell_number = int(cell_number[1:-1])
            set_kn = float(set_kn[1:-1])
            kn1 = float(kn1[1:-1])
            kn2 = float(kn2[1:-1])
            kn3 = float(kn3[1:-1])
            kn4 = float(kn4[1:-1])

            list_of_request.append([date, time, form_number, cell_number, set_kn, kn1, kn2, kn3, kn4])
    if len(list_of_request) != 0:
        conn = sqlite3.connect('pkg_strings.db')
        curs = conn.cursor()

        for row in list_of_request:
            curs.execute('insert into Span6 values (?,?,?,?,?,?,?,?,?)', row)
            conn.commit()

        conn.close()
        print(len(list_of_request))

    f.close()
    shutil.move(os.path.join(path, file_csv), os.path.join('CSV_arch', file_csv))


def write_config(filename, section, option, param):
    config = ConfigParser()
    config.read(filename)
    config.set(section, option, param)
    with open(filename, 'w') as conf_file:
        config.write(conf_file)

def last_file():
    connection = sqlite3.connect('pkg_string.db')
    curs = connection.cursor()
    curs.execute("select * from (select * from Span6 where tens_date = (select max(tens_date) from Span6)) "
                 "where tens_time = (select max(tens_time) from (select * from Span6 "
                 "where tens_date = (select max(tens_date) from Span6)))")
    param = curs.fetchone()
    write_config('config.ini', 'lines', 'end_line', param)
    connection.close()

set_db = read_config('config.ini', 'database')
set_csv = read_config('config.ini', 'source')

for file in os.listdir(set_csv['csv_path']):
    parse_csv_file(file, set_csv['csv_path'])

#last_file()
