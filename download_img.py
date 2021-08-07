# -*- coding: UTF-8 -*-


"""
下载 图片
"""
import os
import time

import requests
from PIL import Image
from lxml import etree

dir_name = '/home/pi/sda1/public/douyin/img'


def reset_size(path):
    try:
        img = Image.open(path)
        img = img.convert('RGB')
        width = 670
        height = 1200
        new_img = img.resize((width, height), Image.BILINEAR)
        new_img.save(os.path.join(dir_name, str(int(time.time_ns())) + '.jpg'))
    except:
        pass
    finally:
        os.system('rm {}'.format(path))


def main():
    for i in range(20):
        url = 'https://m.bcoderss.com/tag/%E7%BE%8E%E5%A5%B3/page/{}/'.format(str(i))
        resp = requests.get(url)
        for _ in etree.HTML(resp.text).xpath("//img[contains(@class, 'wp-post-image')]//@src"):
            image_url = str(_)
            print('download {}'.format(image_url))

            path = os.path.join(dir_name, str(int(time.time_ns())) + '.jpg')
            with open(path, 'wb') as f:
                f.write(requests.get(image_url).content)
            reset_size(path)


if __name__ == '__main__':
    main()
