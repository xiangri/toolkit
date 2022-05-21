#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @FileName:  df
# @Function:  
# @Usage   :
# @Input   :  
# @Output  :
# @Notes   :  
# @Author  :  ri.xiang
# @Date    :  2022/4/10 12:48 上午
import requests


URL = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123039532775952146637_1649521902993&sortColumns=REPORT_DATE&sortTypes=-1&pageSize=50&pageNumber=1&columns=ALL&filter=(SECURITY_CODE%3D%22688169%22)&reportName=RPT_DMSK_FN_CASHFLOW"

def get_resp(url):

    resp = requests.get(url=url).text
    if resp.startswith("jQuery"):
        resp = resp.split('(')[-1]


if __name__ == '__main__':
    get_resp(URL)