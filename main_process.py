# -*- coding: UTF-8 -*-
import argparse
import logging
import os
import time
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format=''
)


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
    base_dir = os.path.dirname(mp4_file)
    result_file_name = os.path.join(base_dir, '{}.mp4'.format(datetime.now().strftime('%Y%m%d_%H%M%S')))
    all_files = []
    for index in range(0, len(parts), 2):
        file_name = random_file_name(base_dir)
        # cmd = 'MP4Box -splitx {}:{} {} -out {}'.format(str_to_second(parts[index]), str_to_second(parts[index + 1]), mp4_file, file_name)
        cmd = 'ffmpeg -i {} -ss {} -to {} -y {}'.format(mp4_file, parts[index], parts[index + 1], file_name)
        os.system(cmd)
        all_files.append(file_name)
    cmd = 'MP4Box {} {}'.format("".join(["-cat {} ".format(_) for _ in all_files]), result_file_name)
    logging.info('merge cmd: {}'.format(cmd))
    os.system(cmd)

    return result_file_name


def random_file_name(dir_name, title=None):
    if not title:
        title = str(int(time.time_ns()))
    return os.path.join(dir_name, title + '.mp4')


def main(input_file: str, parts: list, mp3_file: str, bg_image: str, title: str, font_color: str):
    """
    :param input_file: 需要剪辑的文件
    :param parts: 剪辑的片段 00:01:09 00:02:09
    :param mp3_file: 背景音乐
    :param bg_image: 背景图片
    :param title: title
    :return:
    """
    dir_name = os.path.dirname(input_file)
    merged_mp4 = cut_video(input_file, parts)

    add_mp3_mp4 = random_file_name(dir_name, 'add_mp3_{}'.format(title))
    add_mp3_cmd = 'ffmpeg -i {} -i {} -filter_complex "[0:a][1:a]amerge=inputs=2[a]" -map 0:v -map "[a]" -c:v copy -c:a libvorbis -ac 2 -shortest {}'.format(merged_mp4, mp3_file, add_mp3_mp4)
    logging.info("add_mp3_cmd: {}".format(add_mp3_cmd))
    os.system(add_mp3_cmd)

    result_file = random_file_name(dir_name, title)

    # add bg and sub-title
    final_cmd = '''ffmpeg -loop 1 -i {} -i {} -filter_complex "[1:v]scale=1080:-1[fg];[0:v][fg]overlay=(W-w)/2:(H-h)/2:shortest=1,drawtext=text='{}':fontfile=/opt/kai.ttf:x=(
    w-text_w)/2:y=180:fontsize=60:fontcolor={},drawtext=text=beer:x=20:y=300:fontsize=30:fontcolor=white" -c:v libx264 -y {}'''.format(bg_image, add_mp3_mp4, title, font_color, result_file)
    logging.info("final_cmd: {}".format(final_cmd))
    os.system(final_cmd)

    logging.info("final mp4 file: {}".format(os.path.join(dir_name, result_file)))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--target_file', type=str, help='目标 mp4 文件', required=True)
    ap.add_argument('-l', '--part_list', nargs="+", help='需要剪辑的片段. 00:10:00 00:16:00 00:20:00 00:21:00', required=True)
    ap.add_argument('-m', '--mp3', type=str, help='mp3 文件路径。做背景音乐', required=True)
    ap.add_argument('-i', '--img', type=str, help='背景图片', required=True)
    ap.add_argument('-t', '--title', type=str, help='title', required=True)
    ap.add_argument('-c', '--color', type=str, help='title color', required=True)
    args = ap.parse_args()

    if len(args.part_list) % 2 != 0:
        logging.error("--part_list 参数，应该是成对的")
        exit()
    if not os.path.exists(args.mp3):
        logging.error("mp3:{} 不存在".format(args.mp3))
        exit()

    if not os.path.exists(args.img):
        logging.error("img:{} 不存在".format(args.img))
        exit()

    main(args.target_file, args.part_list, args.mp3, args.img, args.title, args.color)
