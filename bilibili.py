import requests
import sys,os
import re
import json
import shutil
import re
import subprocess
# import threading
# from multiprocessing import Pool
# from pprint import pprint

"""
curl -G 'http://api.bilibili.com/x/player/playurl' \
--data-urlencode 'bvid=BV1CF411b7g1' \
--data-urlencode 'cid=448981745' \
--data-urlencode 'qn=112' \
--data-urlencode 'fnval=0' \
--data-urlencode 'fnver=0' \
--data-urlencode 'fourk=1' \
-b 'SESSDATA=xxx' -v
"""
        
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
			'Accept': '*/*',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://www.bilibili.com',
            # "Cookie": 'SESSDATA=xxx'
          }
cookies = {
    'SESSDATA': 'xxx',
}
def get_play_url(bvid, cid):
    url = "http://api.bilibili.com/x/player/playurl"
    data = {
        "bvid": bvid,
        "cid": cid,
        "qn": "112",
        "fnval": "0",
        "fnver": "0",
        "fourk": "1"
    }
    res = requests.get(url, params=data, cookies=cookies)
    # print(res)
    # print(res.text)
    # print(res.json())
    durl = res.json()['data']['durl']
    return durl


def download_video(file_prefix, durl):
    for url_info in durl:
        order = url_info['order']
        url = url_info['url']
        # size = url_info['size']
        # length = url_info['length']
        cmd = "wget '{}' --referer 'https://www.bilibili.com' -O '{}_{}.flv'".format(url, file_prefix, order)
        out = subprocess.call(cmd, shell=True)
        # print(bvid, cmd)
        print(out)


def get_video_info(bvid):
    url = "http://api.bilibili.com/x/web-interface/view"
    data = {
        "bvid": bvid,
    }
    res = requests.get(url, params=data, cookies=cookies)
    # print(res)
    # print(res.text)
    # print(res.json())
    data = res.json()['data']
    return data

def download(bvid):
    video_info = get_video_info(bvid)
    title = video_info['title']
    video_dir = '/Users/xiangri/bi_video/{}'.format(title)
    if not os.path.exists(video_dir):
        os.mkdir(video_dir)

    for p in video_info['pages']:
        cid = p['cid']
        part = p['part']
        durl = get_play_url(bvid, cid)
        file_prefix = '{}/{}'.format(video_dir, part)
        # '/Users/xiangri/bi_video/{}_{}.flv'
        download_video(file_prefix, durl)



if __name__ == "__main__":
    # pass
    bvid = 'BV1CF411b7g1'
    # cid = '448981745'
    # durl = get_play_url(bvid, cid)
    # download_video(bvid, durl)
    # data = get_video_info(bvid)
    # print(data)
    download(bvid)
    