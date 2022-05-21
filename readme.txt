######## 功能列表 ######
1. 对src文件夹中所有文件，如果名字【包含】target.txt里的项，就复制到dst文件夹里:
    cd "C:\Users\Tracy JT Zhang\Desktop\test" ; python file_tool.py "target.txt" "c:\src文件夹" "c:\dst文件夹"

2. 把src文件夹里所有工作簿里的所有同名的表合并到一个工作簿里: 
    cd "C:\Users\Tracy JT Zhang\Desktop\test" ; python merge_excel.py "c:\src文件夹" "合并结果.xlsx"

3. 列出来src文件夹下所有文件名:
    3.1 只打印文件名
        cd "C:\Users\Tracy JT Zhang\Desktop\test" ; python print_files.py "c:\src文件夹"
    3.2 打印文件的全路径
        cd "C:\Users\Tracy JT Zhang\Desktop\test" ; python print_files.py "c:\src文件夹" 1

####### powershell命令 ######
1. 解压zip包到dst文件夹下
    Expand-Archive -Path "E:\src.zip" -DestinationPath "F:\dst文件夹"
    1.1 批量解压src文件夹下的所有zip包
    cd "c:\src文件夹" ; ls | Expand-Archive -Path


######### Tips #########

1. 路径问题需要修改代码 file_path = r"c:\" 

2. 需要使用anaconda的cmd或者powershell运行代码

3. 切换到代码目录，使用 cd 命令
    cd "c:\代码目录"
4. 终端里字符乱码，设置编码
    CHCP 65001

5. 运行代码 python [脚本名].py
    python merge_excel.py


######## todo #######
1. fire模块用不了，怎么解决参数化使得不需要修改代码
2. 1问题还是算了，不想了，没必要，你说是吧
3. 1和2问题，反正也不复杂也不考虑复用代码就一个功能一个代码文件得了，done. 
