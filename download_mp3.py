# -*- coding: UTF-8 -*-
import logging
import os
import time

import requests

logging.basicConfig(
    level=logging.INFO,
    format=''
)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}

dir_name = '/home/pi/sda1/public/douyin/music'


def main():
    for i in range(1, 999):
        target_url = 'http://f3.htqyy.com/play9/{}/mp3/5'.format(i)
        mp3_resp = requests.get(target_url, headers=headers)
        with open(os.path.join(dir_name, str(int(time.time_ns())) + '.mp3'), 'wb') as f:
            f.write(mp3_resp.content)


if __name__ == '__main__':
    main()
