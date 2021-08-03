# -*- coding: UTF-8 -*-
from PIL import Image

"""
剪切为指定像素
"""


def main():
    img = Image.open("./lover.png")  # 1200 * 1200
    cropped = img.crop((262.5, 0, 262.5 + 675.0, 1200))  # (left, upper, right, lower)
    cropped.save("./bg.png")


if __name__ == '__main__':
    main()
