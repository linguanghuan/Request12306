# Request12306
从12306网站请求获取列车时刻信息

## 车站信息
从该地址可以下载到一个全国车站信息的js文件

    https://kyfw.12306.cn/otn/resources/js/framework/station_name.js

其中的每一条车站信息的格式如下

    @拼音简写|车站名|编码|拼音|首字母|编号
    @bjb|北京北|VAP|beijingbei|bjb|0

## 车次信息
车次信息文件下载地址

    https://kyfw.12306.cn/otn/resources/js/query/train_list.js

车次信息文件也是一个js文件,其中将一个超长的json对象赋值给一个变量,处理起来相对麻烦点

通过分析12306网站查询查票的行为,可以得到其获取信息的请求地址,结合前面两个文件的内容,就能获取到大部分车次的列车时刻表

请求地址

    https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=列车编号&from_station_telecode=出发车站电报码&to_station_telecode=到达车站电报码&depart_date=出发日期



## 步骤

### 下载python

https://repo.anaconda.com/archive/Anaconda3-5.3.1-Windows-x86_64.exe

安装pymysql

pip install pymysql

用python2.7运行会报错，我测试的环境是用python3.7，环境就是用上述地址下载的anaconda



### 建库 建表

```sql
CREATE TABLE `station` (
  `id` int(11) DEFAULT NULL,
  `simpleSpell` varchar(255) DEFAULT NULL,
  `sName` varchar(255) DEFAULT NULL,
  `sCode` varchar(255) DEFAULT NULL,
  `spell` varchar(255) DEFAULT NULL,
  `initial` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `train` (
  `id` int(11) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `trainNo` varchar(255) DEFAULT NULL,
  `startStation` varchar(255) DEFAULT NULL,
  `stopStation` varchar(255) DEFAULT NULL,
  `tCode` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `trainsearch` (
  `id` int(11) NOT NULL,
  `trainId` varchar(255) DEFAULT NULL,
  `stations` varchar(255) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `sch` (
  `id` int(11) DEFAULT NULL,
  `trainId` int(11) DEFAULT NULL,
  `stationNo` varchar(255) DEFAULT NULL,
  `station` varchar(255) DEFAULT NULL,
  `arrive` varchar(255) DEFAULT NULL,
  `start` varchar(255) DEFAULT NULL,
  `stopover` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

```

### 执行脚本

用anaconda的命令提示符进入到代码目录，

按顺序执行以下脚本



python load-station.py

python load-train.py

python process_train-list.py

python request_detail-list.py



运行示例：

(base) C:\Users\gh\Desktop\huoche\Request12306\main>python load_schedule.py



## 结果

1. [source/20181214.zip](source\/20181214.zip)目录下保存了2018-12-14运行下载的数据以及得到的中间结果，还有报错信息（报错目前只是先记录到err文件还未排查原因和处理）
2. [sqlresult/20181214.sql.zip](sqlresult\/20181214.sql.zip) 是导入的mysql数据库结果数据，直接用这个表的数据即可

### TODO

排查处理source目录中err_list.json以及sch_err.json的错误





