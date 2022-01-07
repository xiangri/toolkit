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
import os
import shutil
import fire
from fire.core import Fire


def read_file(file_path):
    with open(file_path, 'r') as f:
        data = f.read().split("\n")
    # return list(filter(lambda x: x, data))
    return data


def classify_files(file_list_path, src_dir_path, result_dir_path):
    file_set = get_file_set(file_list_path, result_dir_path)
    print("file_set:")
    for f in file_set:
        print(f)
    print("\n\nstart classify:\n\n")
    count = 0
    for root, dirs, files in os.walk(src_dir_path):
        for f in files:
            if f in file_set:
                src_f = os.path.join(root, f)
                dst_f = os.path.join(file_set[f], f)
                print("copy {} to {}".format(src_f, dst_f))
                if not os.path.exists(file_set[f]):
                    os.mkdir(file_set[f])
                shutil.copy2(src_f, dst_f)
                count += 1
    print("classify finished, the number of successes was {}".format(count))


def get_file_set(file_list_path, result_dir_path):
    file_list = read_file(file_list_path)
    if not os.path.exists(result_dir_path):
        os.mkdir(result_dir_path)
    file_mapping = {}
    for f in file_list:
        if not f:
            continue
        file_name = f.strip()
        _dir = file_name.split('【')[0]
        file_mapping[file_name] = os.path.join(result_dir_path, _dir)

    return file_mapping


def creat_test(file_path, src_dir_path):
    file_list = read_file(file_path)
    if not os.path.exists(src_dir_path):
        os.mkdir(src_dir_path)
    for f in file_list:
        file_name = f.strip()

        if not file_name:
            continue
        _dir = file_name.split('【')[1].split('】')[0]
        _dir = os.path.join(src_dir_path, _dir)
        if not os.path.exists(_dir):
            os.mkdir(_dir)
        p = os.path.join(src_dir_path, _dir, file_name)
        with open(p, 'w') as f:
            f.write(file_name)

def print_all_file(dir_path='.', need_full_path=False):
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            name = f if not need_full_path else os.path.join(root, f)
            print(name)

class Main(object):
    @staticmethod
    def classify(file_set, src_dir, dst_dir):
        """
        遍历src_dir_path下的所有文件，
        如果文件名在file_list_path名单中，就将该文件复制到result_dir_path目录下，并且按照'【'前的名字创建文件夹分类放好
        """
        # file_list_path = '/Users/xiangri/Demo/z1.txt'
        # src_dir_path = '/Users/xiangri/Demo/src/'
        # dst_dir_path = '/Users/xiangri/Demo/result/'
        # creat_test(file_list_path, src_dir_path)
        # print(read_file(file_list_path))
        # classify_files(file_list_path, src_dir_path, dst_dir_path)
        classify_files(file_set, src_dir, dst_dir)
    
    @staticmethod
    def mv_files(target_file_set, src_dir, dst_dir):
        target_list = read_file(target_file_set)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        print("target_list:")
        for f in target_list:
            print(f)
        print(len(target_list))
        print("\n\nstart mv:\n\n")
        count = 0
        for root, dirs, files in os.walk(src_dir):
            for f in files:
                for target in target_list:
                    src_f = os.path.join(root, f)
                    # 如果src目录下包含dst_dir则跳过
                    if src_f.startswith(dst_dir):
                        continue
                    if target.strip() and target.strip() in f:
                        try:
                            shutil.copy2(src_f, dst_dir)
                            print("copy {} to {}".format(src_f, dst_dir))
                            count += 1
                            break
                        except:
                            print("failed copy file: ", src_f)

        print("mv finished, the number of successes was {}".format(count))

    

    @staticmethod
    def get_file_list(dst_dir='.', need_full_path=False):
        print_all_file(dst_dir, need_full_path)

    @staticmethod
    def help():
        text = """
        1.遍历src_dir下的所有文件，如果文件名在file_set名单中，就将该文件复制到dst_dir目录下，并且按照'【'前的名字创建文件夹分类放好
            useage : python file_tool.py classify --file_set='/Users/xiangri/Demo/z1.txt' --src_dir='/Users/xiangri/Demo/src/' --dst_dir='/Users/xiangri/Demo/result/'
        
        2.输出dst_dir目录下所有文件名, 可选参数：
            --dst_dir, 不写dst_dir就是当前目录
            --need_full_path, 是否打印全路径，默认是False,不打印
            
            2.1 打印当前目录下文件名
            useage : python file_tool.py get_file_list

            2.2 打印指定目录下所有文件名
            useage : python file_tool.py get_file_list --dst_dir='/Users/xiangri/Demo/result'

            2.3 打印指定目录下所有文件的全路径
            useage : python file_tool.py get_file_list --dst_dir='/Users/xiangri/Demo/result' --need_full_path=True
        
        3.遍历src_dir下的所有文件，如果文件名【包含】在target_file_set名单中，就将该文件复制到dst_dir目录下
            useage: python file_tool.py mv_files --target_file_set='target.txt' --src_dir='/Users/xiangri/github/toolkit' --dst_dir='/Users/xiangri/github/toolkit/test'

            easy useage:  python file_tool.py mv_files target.txt /Users/xiangri/github/toolkit /Users/xiangri/github/toolkit/test
        """
        print(text)


if __name__ == '__main__':
    # python file_tool.py help
    # fire.Fire(Main)
    target_file_set = r"target.txt"
    src_dir = r"c:\sss"
    dst_dir = r"C:\sss"
    Main.mv_files(target_file_set, src_dir, dst_dir)

