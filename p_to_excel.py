#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @FileName:  p_to_excel
# @Function:  
# @Usage   :
# @Input   :  
# @Output  :
# @Notes   :  
# @Author  :  ri.xiang
# @Date    :  2022/4/2 6:34 下午
import os

import cv2
import numpy as np
import pytesseract
from PIL import Image
import csv
import re
import json
import requests
import base64

'''
表格文字识别(同步接口)
'''


def get_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=T7IQ7dpukaiapppmfjWIbBW4&client_secret=6GWC8YHeHLALeAFfEIEzmu2aa9iod9w7'
    response = requests.get(host)
    if response:
        print(response.json())
    return response.json()['access_token']


def get_table(img_file_path):
    # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/form"
    request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request"
    # 二进制方式打开图片文件
    f = open(img_file_path, 'rb')
    img = base64.b64encode(f.read())
    f.close()
    params = {"image": img, "is_sync": "true", "request_type": "excel"}
    access_token = '24.acfcf1f768960fc1bb7633ebe0ed6185.2592000.1651489133.282335-25898425'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
    return response.json()


if __name__ == '__main__':
    img = "/Users/xiangri/github/toolkit/img.png"
    rs = get_table(img)
    print(rs)
