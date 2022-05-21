#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @FileName:  classify
# @Function:  
# @Usage   :
# @Input   :  
# @Output  :
# @Notes   :  
# @Author  :  ri.xiang
# @Date    :  2021/12/8 11:16 上午
import sys
import os


def print_all_file(dir_path='.', need_full_path=False):
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            name = f if not need_full_path else os.path.join(root, f)
            print(name)


if __name__ == '__main__':
    print(sys.argv)

    # dir_path = r"/Users/xiangri/github/toolkit"
    dir_path = r'{}'.format(sys.argv[1])
    need_full_path = False
    if len(sys.argv) >= 3 and sys.argv[2] == '1':
        need_full_path = True

    print_all_file(dir_path, need_full_path)

