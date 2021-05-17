# -*- coding: UTF-8 -*-
import getopt
import json
import os
import sys

base_dir = '/Users/beer/Library/Containers/com.cntv.cboxmac/Data/Library/CBox/userdata/download'


def get_real_path(n):
    name_list = []
    with open(os.path.join(base_dir, 'list.wzd'), 'r') as f:
        s = f.read()
        for _ in s.split(" "):
            if len(_) > 10:
                name_list.append(_.strip()[-32:])
    return name_list[int(n) - 1]


def run_cmd(cmd):
    if flag:
        print(cmd)
    else:
        os.system(cmd)


def main(n: int):
    path = get_real_path(n)
    pwd_path = os.path.join(base_dir, path)
    list_files = {}
    for _ in os.listdir(pwd_path):
        if _.endswith(".mp4"):
            list_files[int(_.split('-')[-1].replace('.mp4', ''))] = _

    os.chdir(pwd_path)

    fianl_index = 1

    for i in range(1, len(list_files) - 1, 3):
        step = 3
        if i == 19 and n == 1:
            step = 4
        # 转为 ts
        tss = []
        for j in range(i, i + step):
            cmd = "ffmpeg -i {} -vcodec copy -acodec copy -vbsf h264_mp4toannexb {}.ts -y".format(list_files.get(j), j)
            run_cmd(cmd)
            tss.append('{}.ts'.format(j))
        concat = '|'.join(tss)
        cmd = 'ffmpeg -i "concat:{}" -acodec copy -vcodec copy -absf aac_adtstoasc {}.mp4 -y'.format(concat, fianl_index)
        run_cmd(cmd)
        fianl_index = fianl_index + 1

    for i in range(1, fianl_index):
        parmas = [
            'crop="850:650"',
            'scale=1080:-1',
            'pad=1080:1920:0:550',
            "delogo=x=1000:y=580:w=79:h=50",
            'drawtext=text="流金岁月":fontfile=/Users/beer/beer/douyin/ttf/fan.ttf:x=210:y=230:fontsize=180:fontcolor=red',
            'drawtext=text="beer":fontfile=/Users/beer/beer/douyin/ttf/kai.ttf:x=900:y=500:fontsize=50:fontcolor=yellow',
            'drawtext=text="{}-{}":fontfile=/Users/beer/beer/douyin/ttf/kai.ttf:x=430:y=430:fontsize=100:fontcolor=white'.format(n, i),
        ]
        tang = datas[(int(n) - 1) * fianl_index + i - 1]
        paragraphs = tang.get('paragraphs')
        paragraphs = paragraphs[0:min(len(paragraphs), 6)]
        s = 'drawtext=text="{}":fontfile=/Users/beer/beer/douyin/ttf/kai.ttf:x=(w-text_w)/2:y={}:fontsize=50:fontcolor=white'
        y = 1480
        for _ in paragraphs:
            parmas.append(s.format(_, y))
            y = y + 80
        result_name = '{}-{}'.format(n, (int(n) - 1) * fianl_index + i)
        cmd = '''ffmpeg -i {}.mp4 -i /Users/beer/beer/douyin/liu_jin_sui_yue/001.mp3 -vf "{}"  -preset superfast -acodec copy tmp{}.mp4 -y'''.format(i, ','.join(parmas), result_name)
        run_cmd(cmd)
        # add logo
        if i == 1:
            cmd = "ffmpeg -ss 00:01:34 -i tmp{}.mp4 -i /Users/beer/beer/douyin/liu_jin_sui_yue/teemo.png -filter_complex overlay=10:330 {}.mp4".format(result_name, result_name)
        elif i == 7:
            cmd = "ffmpeg -i tmp{}.mp4 -i /Users/beer/beer/douyin/liu_jin_sui_yue/teemo.png -filter_complex overlay=10:330 {}.mp4".format(result_name, result_name)
        else:
            cmd = "ffmpeg -to 00:06:58 -i tmp{}.mp4 -i /Users/beer/beer/douyin/liu_jin_sui_yue/teemo.png -filter_complex overlay=10:330 {}.mp4".format(result_name, result_name)
        run_cmd(cmd)


datas = []
flag = False

if __name__ == '__main__':
    with open('poet.song.0.json', 'r', encoding='utf8') as f:
        datas = json.load(f)

    args = sys.argv
    params = getopt.getopt(args[1:], 'n:d')
    m = {}
    for _ in params:
        if not _:
            continue
        m.update(dict(_))
    flag = '-d' in m
    main(m.get('-n'))
