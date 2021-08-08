# -*- coding: UTF-8 -*-


import os
import random


def get_random(dir):
    return random.choice(os.listdir(dir))


img_dir = '../../resource/img'
mp3_dir = '../../resource/mp3'

if __name__ == '__main__':
    # parts = [
    #     '00:22:20', '00:25:50',
    #     '00:26:12', '00:26:34',
    #     '00:31:22', '00:33:10',
    #     '00:33:28', '00:34:00',
    # ]
    input_file = '/Users/beer/Downloads/shui_hu/新水浒传-04.mp4'

    text = '金翠莲，女，东京人，被恶霸欺凌，最终在酒楼卖唱。'
    #
    # # 开场白
    # say_file = 'out.aiff'
    # say_cmd = "say -o {} -v 'Ting-Ting' {} -r 230".format(say_file, text)
    # subprocess.run(say_cmd, shell=True)
    #
    # start_mp4_cmd = 'ffmpeg -loop 1 -i jin.jpg -i {} -t 5 -shortest -c:v libx264 -y start.mp4'.format(say_file)
    # subprocess.run(start_mp4_cmd, shell=True)
    # exit()
    #
    # # 中间部分
    title = '金翠莲身世'
    #
    # mp3_file = os.path.join(mp3_dir, get_random(mp3_dir))
    # bg_image = os.path.join(img_dir, get_random(img_dir))
    # main(input_file, parts, mp3_file, bg_image, title, 'red')
    #
    # # end
    # end_mp4_cmd = 'ffmpeg -loop 1 -i {} -t 2 -c:v libx264 -y end.mp4'.format(bg_image)
    # subprocess.run(end_mp4_cmd, shell=True)

    # merge
    text_name = 'title_file'
    # with open(text_name, 'w') as f:
    #     f.write("file '{}'\n".format('start.mp4'))
    #     f.write("file '{}'".format('{}.mp4').format(title))

    cmd = 'ffmpeg -f concat -i {} -c:v libx264 -y {}'.format(text_name, 'final_{}.mp4'.format(title))
    print(cmd)
    os.system(cmd)
