# -*- coding: utf-8 -*-
import sys
import pandas as pd


def search_qcc(key):
    return 'key'


def get_wb(f=None):
    f = '/Users/xiangri/github/toolkit/test/test.xlsx'
    print("load workbook ", f)
    wb = pd.read_excel(f, dtype=object)
    wb['结果1'] = ''
    wb['结果2'] = ''
    wb['结果3'] = ''

    for i in range(len(wb['结果1'])):

        wb.loc[i][1],wb.loc[i][2],wb.loc[i][3] = [wb.loc[i], ]
        # print(wb.loc[i].values)


if __name__ == '__main__':
    """
    python merge_excel.py "c:\ss\ss" "all.xlsx"

    cd "c:\代码目录" & python qichacha.py "c:\ss\ss" "all.xlsx"
    """
    # print(sys.argv)
    # src_file = r'{}'.format(sys.argv[1])
    # result_file = r'{}'.format(sys.argv[2])
