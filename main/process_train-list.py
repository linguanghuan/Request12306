import json

'''
    解析train_list.js文件，将其中一个日期的车次信息抓取出来，写入
'''

in_file = '../source/train_list.js'
date = '2018-07-05'


def get_start_letter_index(letter):
    index = -1
    with open(in_file, encoding='utf-8') as src:
        count = -1
        for char in src.read():
            count += 1
            if char == letter:
                # print(count)
                index = count
                break
    return index


def get_date_train_list(d):
    offset = get_start_letter_index('{')

    with open(in_file, 'r', encoding='utf-8') as fs:
        line = fs.read()
        train_data = json.loads(line[offset:])
        return train_data[d]


def main():
    data = get_date_train_list(date)
    out_file = '../source/train_list_{}.json'.format(date)
    with open(out_file, 'w', encoding='utf-8') as out:
        out.write(json.dumps(data))
        print('done')


if __name__ == '__main__':
    main()
