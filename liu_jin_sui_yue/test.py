# -*- coding: UTF-8 -*-

import os

if __name__ == '__main__':
    cmd = 'ffmpeg -i {} -vf "scale=1080:-1,pad=1080:1920:0:300" {}.mp4 -y'
    os.chdir('/Users/beer/beer/gif')
    for _ in os.listdir('/Users/beer/beer/gif'):
        _cmd = cmd.format(_, _.split('.')[0])
        print(_cmd)
        os.system(_cmd)
