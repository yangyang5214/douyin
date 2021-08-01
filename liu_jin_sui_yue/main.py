# -*- coding: UTF-8 -*-

import argparse
import json
import logging
import os

import face_recognition

logging.basicConfig(
    format='',
    level=logging.INFO
)


def split_video(args):
    n = args.index
    logging.info("Number of index: {}".format(n))
    os.system('mkdir -p /tmp/liu_jin_sui_yue/images/{}'.format(n))
    cmd = 'ffmpeg -i /tmp/liu_jin_sui_yue/videos/result-{}.mp4 -r 1 /tmp/liu_jin_sui_yue/images/{}/%d.png'.format(n, n)
    os.system(cmd)


def glance_for_one(lss_encodings, path):
    if not os.path.exists(path):
        return False
    unknow = face_recognition.load_image_file(path)
    try:
        unknow_encoding = face_recognition.face_encodings(unknow)[0]
    except:
        return False

    results = face_recognition.compare_faces(lss_encodings, unknow_encoding, tolerance=0.3)
    if results[0]:
        return True
    else:
        return False


def glance(args):
    n = int(args.index)
    lss_encodings = []
    for _ in os.listdir('lss'):
        lss = face_recognition.load_image_file("lss/{}".format(_))
        lss_encoding = face_recognition.face_encodings(lss)[0]
        lss_encodings.append(lss_encoding)

    base_dir = '/tmp/liu_jin_sui_yue/images/{}'.format(n)
    result_list = []
    index = 0
    for _ in os.listdir(base_dir):
        index = index + 1
        logging.info("Current index {} -------".format(index))
        p = os.path.join(base_dir, _)
        flag = glance_for_one(lss_encodings, p)
        if flag:
            logging.info("Match success {}".format(p))
            result_list.append(p)

    with open('result/{}.json'.format(n), 'w') as f:
        json.dump(result_list, f)


def number_to_date(n):
    m = int(n / 60)
    diff = n - m * 60
    return '00:{}:{}'.format(str(m).zfill(2), diff)


def merge(args):
    n = int(args.index)
    with open('result/{}.json'.format(n), 'r') as f:
        d = json.load(f)
    indexs = []
    for _ in d:
        indexs.append(int(_.split('/')[-1].split('.')[0]))
    indexs = sorted(indexs)
    result = []
    arr = []
    for i in range(len(indexs) - 1):
        if indexs[i + 1] - 30 > indexs[i]:
            if arr and len(arr) != 1:
                result.append(arr)
            arr = []
            continue
        arr.append(indexs[i])
    index = 1
    os.chdir('/tmp/liu_jin_sui_yue/videos')
    for _ in result:
        ss = number_to_date(_[0] - 10)
        to = number_to_date(_[-1] + 10)
        tmp_name = '{}-{}.mp4'.format(n, index)
        cmd = 'ffmpeg -i result-{}.mp4 -ss {} -to {} -vcodec copy -acodec copy {} -y'.format(n, ss, to, tmp_name)
        index = index + 1
        os.system(cmd)
        add_subtitle(tmp_name)


all_mp4 = []


def add_subtitle(file_name):
    result_file = file_name.split('/')[-1]
    arr = result_file.split('-')
    parmas = [
        'crop="800:650"',
        'scale=1080:-1',
        'pad=1080:1920:0:550',
        "delogo=x=1000:y=580:w=79:h=50",
        'drawtext=text="流金岁月":fontfile=/Users/beer/beer/liu_jin_sui_yue/ttf/fan.ttf:x=210:y=230:fontsize=180:fontcolor=red',
        'drawtext=text="beer":fontfile=/Users/beer/beer/liu_jin_sui_yue/ttf/kai.ttf:x=900:y=500:fontsize=50:fontcolor=yellow',
    ]

    tang = datas[(int(arr[0]) - 1) * 5 + int(arr[1].split('.')[0])]
    paragraphs = tang.get('paragraphs')
    paragraphs = paragraphs[0:min(len(paragraphs), 6)]
    s = 'drawtext=text="{}":fontfile=/Users/beer/beer/liu_jin_sui_yue/ttf/kai.ttf:x=(w-text_w)/2:y={}:fontsize=50:fontcolor=white'
    y = 1480
    for _ in paragraphs:
        parmas.append(s.format(_, y))
        y = y + 80

    cmd = 'ffmpeg -i {} -vf "{}"  -preset superfast -acodec copy final_{} -y'.format(file_name, ','.join(parmas), result_file)
    print(cmd)
    os.system(cmd)


def main(args):
    if args.mode == 'split':
        split_video(args)
    elif args.mode == 'glance':
        glance(args)
    elif args.mode == 'merge':
        merge(args)
    else:
        pass


datas = []

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='god eye project')
    parser.add_argument('-m', '--mode', type=str, required=True, choices=['split', 'glance', 'merge'])
    parser.add_argument('-n', '--index', type=str, required=True, help='the number of index')
    args = parser.parse_args()

    with open('poet.song.0.json', 'r', encoding='utf8') as f:
        datas = json.load(f)

    main(args)
