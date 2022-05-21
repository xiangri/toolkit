# -*- coding: utf-8 -*-

import os
import sys
import shutil
from numpy.core.fromnumeric import transpose
import openpyxl
import pandas as pd
import xlrd
import xlwings as xw


def get_all_workbook_files_name(src_dir):
    workbook_files = []
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f.endswith('.xlsx') or f.endswith('.xls'):
                workbook_files.append(os.path.join(root, f))
                print("get ", f)
    return workbook_files


def test(file_path):
    wb = openpyxl.load


def merge(src_dir, result_file='all.xlsx', not_null_columns=None, ):
    """
    将src_dir下面的所有xlsx文件合并到一个xlsx文件中，同名的表竖着合并
    """
    workbook_files = get_all_workbook_files_name(src_dir)
    not_null_columns_dic = {}
    if not_null_columns is not None:
        for sheet_column in not_null_columns.split(','):
            sheet, column = sheet_column.split(':')
            if sheet and column:
                not_null_columns_dic[sheet] = int(column)

    new_wb = {}

    for f in workbook_files:
        # sheet_name=None表示读取所有sheet,否则默认只读第一个sheet
        # wb是一个dict，k是表名，v是表的值 DadaFrame类型
        # wb = pd.read_excel(f, sheet_name=None)
        print("load workbook ", f)
        wb = pd.read_excel(f, sheet_name=None, dtype=object)

        for sheet_name in wb.keys():
            if sheet_name not in new_wb:
                new_wb[sheet_name] = []
                print("find sheet ", sheet_name)
            new_wb[sheet_name].append(wb[sheet_name])

    print("load all workbook finished, start save result to ", result_file)
    with pd.ExcelWriter(result_file) as writer:
        for sheet_name, sheet_value_list in new_wb.items():
            # 将多个DadaFrame竖着合并。横着合并取axis=1
            df = pd.concat(sheet_value_list, axis=0)
            # 将合并后的dataframe当成一张sheet写入excle文件
            df.to_excel(writer, sheet_name=sheet_name)
    print("merge done , please check result_file: ", result_file)


def merge2(src_dir, result_file='all.xlsx', not_null_columns=None, ):
    """
    将src_dir下面的所有xlsx文件合并到一个xlsx文件中，同名的表竖着合并
    """
    workbook_files = get_all_workbook_files_name(src_dir)
    not_null_columns_dic = {}
    if not_null_columns is not None:
        for sheet_column in not_null_columns.split(','):
            sheet, column = sheet_column.split(':')
            if sheet and column:
                not_null_columns_dic[sheet] = int(column)

    new_wb = {}

    for f in workbook_files:
        # sheet_name=None表示读取所有sheet,否则默认只读第一个sheet
        # wb是一个dict，k是表名，v是表的值 DadaFrame类型
        # wb = pd.read_excel(f, sheet_name=None)
        print("load workbook ", f)
        # wb = pd.read_excel(f, sheet_name=None, dtype=object, engine='openpyxl', formatting_info=True)
        wb = pd.read_excel(f, sheet_name=None, dtype=object)

        for sheet_name in wb.keys():
            if sheet_name not in new_wb:
                new_wb[sheet_name] = []
                print("find sheet ", sheet_name)
            new_wb[sheet_name].append(wb[sheet_name])
    print("load all workbook finished, start save result to ", result_file)
    # wb = xlrd.open_workbook(workbook_files[0], formatting_info=True)
    app = xw.App(visible=False)
    # app = xw.App(spec='wpsoffice')

    app.display_alerts = False
    app.screen_updating = False
    # wb = xw.Book(workbook_files[0])
    # wb = app.books.open(workbook_files[0])
    wb = app.books(workbook_files[0])

    for sheet_name, sheet_value_list in new_wb.items():
        df = pd.concat(sheet_value_list, axis=0)
        wb.sheets[sheet_name].value = df
    wb.save(result_file)
    wb.close()
    app.quit()
    print("merge done , please check result_file: ", result_file)


if __name__ == '__main__':
    """
    python merge_excel.py "c:\ss\ss" "all.xlsx"

    cd "c:\代码目录" & python merge_excel.py "c:\ss\ss" "all.xlsx"
    """
    print(sys.argv)
    # src_dir = r'/Users/xiangri/github/toolkit/excel'
    # result_file = r'all—2.xlsx'
    src_dir = r'{}'.format(sys.argv[1])
    result_file = r'{}'.format(sys.argv[2])
    merge(src_dir, result_file)
    # merge2(src_dir, result_file)

a = r'/Users/xiangri/github/toolkit/批量更改源文件/test 1.xlsx'
