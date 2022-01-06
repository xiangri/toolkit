# -*- coding: utf-8 -*-

import os
import shutil
import fire
from fire.core import Fire
import openpyxl
import pandas as pd
from copy import deepcopy


def get_all_sheets_name(src_dir):
    workbook_files = []
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f.endswith('.xlsx'):
                workbook_files.append(os.path.join(root, f))
                print("get ", f)
    return workbook_files


def check_row(row, not_null_columns):
    """
    全部not_null_columns列都不为空才返回True
    :param row:
    :param not_null_columns:
    :return:
    """
    for i in not_null_columns:
        if row[int(i)] is None:
            return False

    return True


def merge(src_dir, not_null_columns=None):
    result_file = 'all.xlsx'
    workbook_files = get_all_sheets_name(src_dir)

    if not_null_columns is None:
        not_null_columns = []
    else:
        not_null_columns = not_null_columns.split(',')

    wb_new = openpyxl.Workbook()

    for f in workbook_files:
        wb = openpyxl.load_workbook(f)
        for s in wb.worksheets:
            if s.title in wb_new.sheetnames:
                curr_sheet = wb_new[s.title]
            else:
                print("load sheet ", s.title)
                curr_sheet = wb_new.create_sheet(s.title)
            for row in s:
                new_row = [cell.value for cell in row]
                if check_row(new_row, not_null_columns):
                    curr_sheet.append(deepcopy(new_row))

    wb_new.save(result_file)
    print("merge done , result_file: ", result_file)


class Main(object):
    @staticmethod
    def merge2one(src_dir='.', not_null_columns=None):
        merge(src_dir, not_null_columns)


if __name__ == '__main__':
    # merge('/Users/xiangri/github/toolkit/test_data/', '2')
    fire.Fire(Main)
    # merge()