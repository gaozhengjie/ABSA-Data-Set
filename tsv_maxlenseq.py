# coding: utf-8
# author: gaozhengjie
# e-mail: gaozhengj@foxmail.com
# description: 统计数据集中每一条记录，最长的长度是多少 max_length


def trans2tsv(filename, filename2tsv):
    # 将以前的txt文本转换成tsv的格式
    fp = open(filename, 'r', encoding='utf-8').readlines()

    text = ''
    for i in range(len(fp)):
        text = text + fp[i][0] + '\t' + fp[i][2:]

    with open(filename2tsv, 'w', encoding='utf-8') as outer:
        outer.write(text)


def find_max_len_seq(filename):
    with open(filename, 'r', encoding='utf-8') as fp1:
        for i in range(len(fp1)):
            if i==0:
                max_len = 0
                continue
            else:
                tmp = len(fp1[i].split(' '))
                if tmp > max_len:
                    max_len = tmp
        print(max_len)


if __name__ == '__main__':
    filename = 'dev.txt'
    filename2tsv = 'dev.tsv'
    trans2tsv(filename, filename2tsv)
    find_max_len_seq(filename)