# -*- coding: UTF-8 -*-
import os
import sys

base_dir = '/Users/beer/Library/Containers/com.cntv.cboxmac/Data/Library/CBox/userdata/download/'

import logging

logging.basicConfig(
    level=logging.INFO,
    format=''
)


def get_index_name(n):
    n = n - 14
    with open(os.path.join(base_dir, 'list.wzd'), 'r') as f:
        s = f.read()
        for _ in s.split(" "):
            if len(_) > 10:
                name = _.strip()[-32:]
                n = n - 1
                if n == 0:
                    return name


def main(num, index_name):
    path = os.path.join(base_dir, index_name)
    os.chdir(path)
    m = {}
    for _ in os.listdir(path):
        if _.startswith(_) and _.endswith('mp4') and 'aac' in _:
            index = _.split('-')[-1].split('.')[0]
            m[index] = _
            os.system('ffmpeg -i {} -vcodec copy -acodec copy -vbsf h264_mp4toannexb {}.ts -y'.format(_, index))

    sorted_list = []
    for i in range(len(m)):
        sorted_list.append('{}.ts'.format(i + 1))

    final_file = 'result-{}.mp4'.format(num)
    cmd = 'ffmpeg -i "concat:{}" -acodec copy -vcodec copy -absf aac_adtstoasc {} -y'.format('|'.join(sorted_list), final_file)

    logging.info('---------------------------------')
    logging.info("cmd: {}".format(cmd))
    logging.info('---------------------------------')

    os.system(cmd)
    cmd = 'mv {} {}'.format(final_file, '/tmp/liu_jin_sui_yue/videos/')
    logging.info("mv cmd: {}".format(cmd))
    os.system(cmd)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit('Need set param "n"')
    main(sys.argv[1], sys.argv[2])
