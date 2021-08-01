# -*- coding: UTF-8 -*-
import os
import sys

if __name__ == '__main__':
    path = sys.argv[1]
    text = sys.argv[2]
    result_file = path.split('/')[-1]
    parmas = [
        'crop="800:650"',
        'scale=1080:-1',
        'pad=1080:1920:0:550',
        "delogo=x=1000:y=580:w=79:h=50",
        'drawtext=text="流金岁月":fontfile=ttf/fan.ttf:x=210:y=230:fontsize=180:fontcolor=red',
        'drawtext=text="beer":fontfile=ttf/kai.ttf:x=900:y=500:fontsize=50:fontcolor=yellow',
        'drawtext=text={}:fontfile=ttf/kai.ttf:x=w/2-text_w/2:y=1600:fontsize=80:fontcolor=yellow'.format(text),
    ]
    cmd = 'ffmpeg -i {} -vf {}  -preset superfast -acodec copy final_{} -y'.format(path, ','.join(parmas), result_file)
    print(cmd)
    os.system(cmd)
