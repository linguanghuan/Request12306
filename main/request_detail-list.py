import sys
sys.path.append("..")

import requests
import pymysql
import json
from config import conf

# 数据库连接
db = pymysql.connect(conf.db['host'], conf.db['user'], conf.db['pwd'], conf.db['database'], charset='utf8')
cursor = db.cursor()


def request_train_detail_info(req_info):
    '''
    使用12306的查询接口获取车次详细信息
    :param data: 请求接口需要的参数信息
    :return: 请求获取的数据
    '''

    # 返回信息，字典格式
    train_info = {}
    url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo'
    data = {
        'train_no': req_info['trainInfo'][-1],
        'from_station_telecode': req_info['start'][0],
        'to_station_telecode': req_info['stop'][0],
        'depart_date': conf.date
    }
    req = requests.get(url, data).json().get('data').get('data')
    train_info['data'] = req

    if not req:
        train_info['error'] = req_info

    return train_info


def query_request_info(train_id):
    '''
    根据车次id，从数据库查询对应车次的信息，以及车次起始站、终点站对应的电报码
    :param train_id: 数据库中，车次对应的id
    :return: 请求所需的车次相关信息
    '''

    req_info = {'id': train_id}

    # 车次信息查询
    cursor.execute(conf.select_train_sql.format(train_id))
    train_info = cursor.fetchone()
    req_info['trainInfo'] = train_info
    if not train_info or len(train_info) != 4:
        req_info['error'] = True
        # 如果车次查询结果异常，直接返回
        return req_info

    # 起始站编码查询
    cursor.execute(conf.select_station_sql.format(train_info[1]))
    start_code = cursor.fetchone()
    req_info['start'] = start_code
    if not start_code:
        req_info['error'] = True

    # 终点站编码查询
    cursor.execute(conf.select_station_sql.format(train_info[2]))
    stop_code = cursor.fetchone()
    req_info['stop'] = stop_code
    if not stop_code:
        req_info['error'] = True

    return req_info


def get_train_num():
    '''
    查询数据库，获取车次数量
    :return: 车次总数
    '''

    sql = "select count(*) from train"
    cursor.execute(sql)
    return cursor.fetchone()[0]


# 保存查询结果的文件
out_file = '../source/detail_list.json'
err_file = '../source/err_list.json'


def main():
    num = get_train_num() + 1
    with open(out_file, 'w', encoding='utf-8') as out, open(err_file, 'w', encoding='utf-8') as err:
        for i in range(1, num):
            req_info = query_request_info(i)
            if 'error' in req_info:
                err.write(json.dumps(req_info) + '\n')
                continue

            result = request_train_detail_info(req_info)
            if 'error' in result:
                err.write(json.dumps(result) + '\n')
            else:
                out.write(json.dumps(result) + '\n')

            if i % 100 == 0:
                print(i)
        print(num)


if __name__ == '__main__':
    main()
    db.close()
