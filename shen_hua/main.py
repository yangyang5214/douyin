# -*- coding: UTF-8 -*-
import getopt
import json
import sys


# https://www.inapian.com/v/20382.html


def main(n):
    pass


flag = False

if __name__ == '__main__':
    with open('poet.tang.1000.json', 'r', encoding='utf8') as f:
        datas = json.load(f)

    args = sys.argv
    params = getopt.getopt(args[1:], 'n:d')
    m = {}
    for _ in params:
        if not _:
            continue
        m.update(dict(_))
    flag = '-d' in m
    main(m.get('-n'))
