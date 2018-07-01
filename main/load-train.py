import re
import pymysql
import json
from config import conf

# 数据库连接
db = pymysql.connect(conf.db['host'], conf.db['user'], conf.db['pwd'], conf.db['database'], charset='utf8')
cursor = db.cursor()

# json数据文件
in_file = '../source/train_list_2018-07-05.json'


def add_train_row(row):
    if len(row) != 6:
        print(row, '数据异常')
        return

    try:
        cursor.execute(conf.insert_train_sql.format(row))
        db.commit()
    except:
        db.rollback()
        print(row, '添加失败')


def main():
    insert_data = {}
    # 数据分割的正则
    pattern = r'[-()]'

    with open(in_file, 'r', encoding='utf-8') as load_file:
        count = 0
        train_dict = json.load(load_file)
        for train_type in train_dict.keys():
            insert_data['type'] = train_type
            for row in train_dict[train_type]:
                count += 1
                insert_data['id'] = count
                insert_data['code'] = row['train_no']
                # 解析车次、出发、终点信息
                info = re.split(pattern, row['station_train_code'])
                insert_data['trainNo'] = info[0]
                insert_data['start'] = info[1]
                insert_data['stop'] = info[2]
                add_train_row(insert_data)

                if count % 100 == 0:
                    print(count)

        print(count)


if __name__ == '__main__':
    main()
    db.close()
