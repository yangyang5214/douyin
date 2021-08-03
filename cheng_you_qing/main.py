# -*- coding: UTF-8 -*-
import argparse
import logging
import os
import subprocess
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format=''
)

"""
https://www.zhihu.com/question/34343360/answer/384884215
"""


def str_to_second(str_date: str):
    """
    时间转化为 s
    :param str_date: 00:00:10
    :return:
    """
    r = 0
    strs = str_date.split(":")
    r += int(strs[0]) * 3600
    r += int(strs[1]) * 60
    r += int(strs[2])
    return r


def cut_video(mp4_file: str, parts: list):
    """
    MP4Box: MP4Box -splitz 10:15 1.mp4
    ffmpeg: ffmpeg -i 1.mp4 -ss 00:00:10 -to 00:00:15 2.mp4

    MP4Box 比 ffmpeg 快好多
    :param mp4_file:
    :param parts:
    :return:
    """
    result_file_name = '{}.mp4'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))
    for index in range(0, len(parts), 2):
        cmd = 'MP4Box -splitz {}:{} {}'.format(str_to_second(parts[index]), str_to_second(parts[index + 1]), mp4_file)
        os.system(cmd)
    os.chdir(os.path.dirname(mp4_file))
    r, _ = subprocess.Popen('ls -t | grep "{}"'.format(os.path.basename(mp4_file).replace('.mp4', '_')), stdout=subprocess.PIPE, shell=True).communicate()
    need_merge_mp4s = r.decode('utf-8').strip().split("\n")
    cmd = 'MP4Box {} {}'.format("".join(reversed(["-cat {} ".format(_) for _ in need_merge_mp4s])), result_file_name)
    os.system(cmd)

    os.system('rm {}'.format(' '.join(need_merge_mp4s)))
    return result_file_name


def main(input_file: str, parts: list):
    merged_mp4 = cut_video(input_file, parts)

    dir_name = os.path.dirname(input_file)
    os.chdir(dir_name)
    result_file = 'result_{}'.format(merged_mp4)
    final_cmd = '''ffmpeg -loop 1 -i /Users/beer/beer/douyin/cheng_you_qing/bg.png -i {} -filter_complex "[1:v]scale=1080:-1[fg];[0:v][fg]overlay=(W-w)/2:(H-h)/2:shortest=1,drawtext=text='我可能不会爱你':fontfile=/Users/beer/beer/douyin/cheng_you_qing/kai.ttf:x=(
    w-text_w)/2:y=130:fontsize=60:fontcolor=red" -y {}'''.format(merged_mp4, result_file)
    os.system(final_cmd)

    logging.info("final mp4 file: {}".format(os.path.join(dir_name, result_file)))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--target_file', type=str, help='目标 mp4 文件', required=True)
    ap.add_argument('-l', '--part_list', nargs="+", help='需要剪辑的片段. 00:10:00 00:16:00 00:20:00 00:21:00', required=True)
    args = ap.parse_args()

    if len(args.part_list) % 2 != 0:
        logging.error("--part_list 参数，应该是成对的")
        exit()
    main(args.target_file, args.part_list)
