from config import conf
import pymysql
import json

# 数据库连接
db = pymysql.connect(conf.db['host'], conf.db['user'], conf.db['pwd'], conf.db['database'], charset='utf8')
cursor = db.cursor()

load_file = '../source/detail_list.json'


def query_train_id(train_no):
    cursor.execute(conf.select_train_id.format(train_no))
    return cursor.fetchone()[0]


def add_schedule(data):
    cursor.execute(conf.insert_schedule_sql.format(data))
    db.commit()


def add_search(data):
    cursor.execute(conf.insert_search_sql.format(data))
    db.commit()


def format_station_info(format_dict, station_info):
    format_dict['stationNo'] = station_info['station_no']
    format_dict['station'] = station_info['station_name']
    format_dict['arrive'] = station_info['arrive_time']
    format_dict['start'] = station_info['start_time']
    format_dict['stopover'] = station_info['stopover_time'][:-2]

    # 处理特殊情况数据
    # 第一站，默认到达时间等于出发时间
    if station_info['station_no'] == '01':
        format_dict['trainId'] = query_train_id(station_info['station_train_code'])
        format_dict['arrive'] = station_info['start_time']

    if '-' in station_info['stopover_time']:
        format_dict['stopover'] = 0
        # 没有停留时间，又不是出发站，所以是终点站
        if station_info['station_no'] != '01':
            format_dict['start'] = station_info['arrive_time']


def main():
    with open(load_file, 'r', encoding='utf-8') as fs:
        schedule_count = 0
        train_count = 0

        # 每一趟列车
        for line in fs:
            # 写入数据，字典格式，方便索引
            schedule_row = {}
            search_row = {}
            # 站点列表
            station_list = []

            train_count += 1

            # str -> dict
            train_info = json.loads(line)
            for station in train_info['data']:
                schedule_count += 1
                schedule_row['id'] = schedule_count
                format_station_info(schedule_row, station)

                # 写入站点详情记录
                # print(schedule_row)
                add_schedule(schedule_row)

                # 站点名收集
                station_list.append(station['station_name'])

            # # 车次查询表数据收集
            # search_row['id'] = train_count
            # search_row['trainId'] = schedule_row['trainId']
            # search_row['stations'] = '-'.join(station_list)
            # search_row['size'] = len(station_list)
            # # 车次查找表数据写入
            # # print(search_row)
            # add_search(search_row)

            if train_count % 100 == 0:
                print(train_count)

        # 简单的信息统计
        print('车站时刻表记录数：', schedule_count)
        print('车次查询记录数：', train_count)


if __name__ == '__main__':
    main()
    db.close()
