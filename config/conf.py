# -*- coding: utf-8 -*-

'''
项目的配置文件
'''

# 指定某个日期,以便获取相应数据
date = '2018-12-14'

# my-database

# db = {
#     'host': '127.0.0.1',
#     'user': 'leng',
#     'pwd': 'root',
#     'database': 'ssm03'
# }
db = {
    'host': '127.0.0.1',
    'user': 'root',
    'pwd': 'root',
    'database': 'ssm03db'
}

# table:    train
# fields:   id, type, trainNo, startStation, stopStation, tCode
# format with dict
insert_train_sql = "insert into train values('{0[id]}','{0[type]}','{0[trainNo]}','{0[start]}','{0[stop]}','{0[code]}')"
select_train_sql = "select trainNo,startStation,stopStation,tCode from train where id={}"

select_train_id = "select id from train where trainNo='{}'"

query_train_id_num = "select count(*) from sch where trainId={}"


# table:    station
# fields:   id, simpleSpell, sName, sCode, spell, initial
# format with list
insert_station_sql = "insert into station values({0[5]},'{0[0]}','{0[1]}','{0[2]}','{0[3]}','{0[4]}')"
select_station_sql = "select sCode from station where sName='{}'"

# table:    sch(schedule)
# fields:   id, trainId, stationNo, station, arrive, start, stopover
insert_schedule_sql = "insert into sch values('{0[id]}','{0[trainId]}','{0[stationNo]}','{0[station]}'," \
                      "'{0[arrive]}','{0[start]}','{0[stopover]}')"


# table:    trainSearch
# fields:   id, trainId, stations, size
insert_search_sql = "insert into trainSearch values('{0[id]}','{0[trainId]}','{0[stations]}','{0[size]}')"
