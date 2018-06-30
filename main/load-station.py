import re
import pymysql

# 数据库连接
host = '127.0.0.1'
user = 'root'
pwd = 'root'
database = 'ssm03db'
db = pymysql.connect(host, user, pwd, database, charset='utf8')
cursor = db.cursor()


def add_station_row(row):
    if len(row) != 6:
        print(row, '数据异常')
        return

    sql = "insert into station values({0[5]},'{0[0]}','{0[1]}','{0[2]}','{0[3]}','{0[4]}')".format(row)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print(row, '添加失败')


def main():
    file_path = '../station_name.js'
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
