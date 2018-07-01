'''
项目的配置文件
'''

# 指定某个日期,以便获取相应数据
date = '2018-07-05'

# my-database

db = {
    'host': '127.0.0.1',
    'user': 'leng',
    'pwd': 'root',
    'database': 'ssm03'
}

# table:    train
# fields:   id, type, trainNo, startStation, stopStation, tCode
# format with dict
insert_train_sql = "insert into train values('{0[id]}','{0[type]}','{0[trainNo]}','{0[start]}','{0[stop]}','{0[code]}')"
select_train_sql = "select trainNo,startStation,stopStation,tCode from train where id={}"

# table:    station
# fields:   id, simpleSpell, sName, sCode, spell, initial
# format with list
insert_station_sql = "insert into station values({0[5]},'{0[0]}','{0[1]}','{0[2]}','{0[3]}','{0[4]}')"
select_station_sql = "select sCode from station where sName='{}'"

