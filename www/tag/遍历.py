# 输出指定目录所有文件的名称,只有文件名,不要路径,不包括子目录
import os


def print_dir(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            print(file)



print_dir('F:/OneDrive - Fornaxignis/Dev/sandberrypi/www/painting')
