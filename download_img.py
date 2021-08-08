# -*- coding: UTF-8 -*-


"""
下载 图片
"""
import os

import requests
from lxml import etree

from image_tools import reset_size

dir_name = '/Users/beer/beer/douyin/resource/img'


def main():
    for i in range(20):
        url = 'https://m.bcoderss.com/tag/%E7%BE%8E%E5%A5%B3/page/{}/'.format(str(i))
        resp = requests.get(url)
        for _ in etree.HTML(resp.text).xpath("//img[contains(@class, 'wp-post-image')]//@src"):
            image_url = str(_).replace('-260x534', '')
            print('download {}'.format(image_url))
            path = os.path.join(dir_name, image_url.split('/')[-1])
            _resp = requests.get(image_url)
            if _resp.status_code != 200:
                continue
            with open(path, 'wb') as f:
                f.write(_resp.content)
            reset_size(path)
            os.system('rm {}'.format(path))


if __name__ == '__main__':
    main()
