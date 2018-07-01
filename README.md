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