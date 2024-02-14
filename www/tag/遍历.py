# 输出指定目录所有文件的名称
import os

def print_dir(path):
    for x in os.listdir(path):
        if os.path.isfile(x):
            print(x)
        else:
            print_dir(x)


print_dir('F:\OneDrive - Fornaxignis\Dev\sandberrypi\www\painting')
