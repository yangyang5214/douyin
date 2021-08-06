# -*- coding: UTF-8 -*-
import logging
import os
import sys

import requests
from lxml import etree

logging.basicConfig(
    level=logging.INFO,
    format=''
)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}

base_dir = '.'


def main(url: str):
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        logging.error("status_code is: {}".format(resp.status_code))
        exit()
    script_text = etree.HTML(resp.text).xpath("//script[contains(text(),'mp3')]")[0].text
    file_host, mp3_path, title = None, None, None
    for _ in script_text.split(';'):
        if 'var fileHost' in _:
            file_host = _.split('=')[1].strip().strip('\"')
        elif 'var mp3' in _:
            mp3_path = _.split('=')[1].strip().strip('\"')
        elif 'var bdText ' in _:
            title = _.split('=')[1].strip().strip('\"')
        else:
            pass
    target_url = file_host + mp3_path

    logging.info('start download {}: {}...'.format(title, target_url))

    mp3_resp = requests.get(target_url, headers=headers)
    with open(os.path.join(base_dir, title + '.mp3'), 'wb') as f:
        f.write(mp3_resp.content)


if __name__ == '__main__':
    argvs = sys.argv
    if len(argvs) == 1:
        logging.info("请添加需要下载的 url ...")
        exit()
    main(argvs[1])
