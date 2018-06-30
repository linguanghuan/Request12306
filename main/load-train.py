import re
import pymysql
import json

# 数据库连接
host = '127.0.0.1'
user = 'root'
pwd = 'root'
database = 'ssm03db'
db = pymysql.connect(host, user, pwd, database, charset='utf8')
cursor = db.cursor()

# 数据库表信息
# table: train
# fields: trainId, trainType, trainNo, startStation, stopStation, trainCode

# 车次日期
date = '2018-07-05'
# json数据文件
in_file = '../source/train_list_2018-07-05.json'


def add_train_row(data):
    if len(data) != 5:
        print(data, '数据异常')
        return

    sql = "insert into train values(null,'{0[type]}','{0[trainNo]}','{0[start]}','{0[stop]}','{0[code]}')".format(data)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print(data, '添加失败')


def main():
    data = {}
    # 数据分割的正则
    pattern = r'[-()]'

    with open(in_file, 'r', encoding='utf-8') as load_file:
        count = 0
        load_dict = json.load(load_file)
        for train_type in load_dict.keys():
            data['type'] = train_type
            for row in load_dict[train_type]:
                data['code'] = row['train_no']
                info = re.split(pattern, row['station_train_code'])
                data['trainNo'] = info[0]
                data['start'] = info[1]
                data['stop'] = info[2]
                add_train_row(data)
                count += 1

                if count % 100 == 0:
                    print(count)

        print(count)


if __name__ == '__main__':
    main()
    db.close()
