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


def add_train_row(data):
    if len(data) != 5:
        print(data, '数据异常')
        return

    # train(id,type,trainNo,startStation,stopStation,tCode)
    sql = "insert into train values(null,'{0[type]}','{0[trainNo]}','{0[start]}','{0[stop]}','{0[code]}')".format(data)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print(data, '添加失败')


def main():
    file = '../train-list.json'
    date = '2018-07-05'
    data = {}
    pattern = r'[-()]'

    with open(file, 'r', encoding='utf-8') as load_file:
        count = 0
        load_dict = json.load(load_file).get(date)
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
