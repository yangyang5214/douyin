# -*- coding: UTF-8 -*-


import os
import random

from main_process import main


def get_random(dir):
    return random.choice(os.listdir(dir))


img_dir = 'resource/img'
mp3_dir = 'resource/mp3'

if __name__ == '__main__':
    input_file = '/home/pi/sda1/public/movies/shui_hu_zhuan/新水浒传-01.mp4'
    parts = ['00:00:00', '00:00:10']
    mp3_file = os.path.join(mp3_dir, get_random(mp3_dir))
    bg_image = os.path.join(img_dir, get_random(img_dir))
    title = '及时雨 —— 宋江'
    main(input_file, parts, mp3_file, bg_image, title, 'red')
