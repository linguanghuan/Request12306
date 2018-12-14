# -*- coding: utf-8 -*-
import sys
sys.path.append("..")

import re
import pymysql

from config import conf

# 数据库连接
db = pymysql.connect(conf.db['host'], conf.db['user'], conf.db['pwd'], conf.db['database'], charset='utf8')
cursor = db.cursor()


def add_station_row(row):
    if len(row) != 6:
        print(row, '数据异常')
        return

    try:
        cursor.execute(conf.insert_station_sql.format(row))
        db.commit()
    except:
        db.rollback()
        print(row, '添加失败')


def main():
    file_path = '../source/station_name.js'
    count = 0

    file_pattern = re.compile(r"'(.*?)'")
    row_pattern = re.compile(r"@(.*?\d{1,5})")

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            re_line = file_pattern.findall(line)
            for row in re_line:
                re_row = row_pattern.findall(row)
                for data in re_row:
                    add_station_row(data.split('|'))
                    count += 1

                    if count % 100 == 0:
                        print(count)
        print(count)


if __name__ == '__main__':
    main()
    db.close()
