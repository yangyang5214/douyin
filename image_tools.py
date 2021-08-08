# -*- coding: UTF-8 -*-
import logging
import os

from PIL import Image

logging.basicConfig(
    level=logging.INFO,
    format=''
)

"""
将图片转换为 676 / 1200 像素
"""


def get_width_index(height, width):
    for i in range(height):
        for j in range(1, width):
            ratio = round((height - i) / (width - j), 2)
            logging.info('ratio: {}'.format(ratio))
            if ratio == 1.78:
                return int(i / 2), int(j / 2),


def reset_size(path):
    """
    把图片剪裁或者放大
    :param path:
    :return:
    """
    try:
        img = Image.open(path)
        height = img.height
        width = img.width
        _width = int(9.0 / 16.0 * height)
        if height >= 1200 and width >= 675 and _width < width:
            new_img = img.crop(((width - _width) / 2, 0, _width + (width - _width) / 2, height))
        else:
            height_index, width_index = get_width_index(height, width)
            new_img = img.crop((width_index, height_index, width - width_index, height - height_index))
        new_img = new_img.resize((676, 1200), Image.ANTIALIAS)
        final_file = os.path.dirname(path) + '/result_' + os.path.basename(path)
        new_img.save(final_file)
    except:
        pass


if __name__ == '__main__':
    reset_size('/Users/beer/beer/douyin/14365_1627734405.jpg')
