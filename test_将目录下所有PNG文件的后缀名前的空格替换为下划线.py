# 将目录下所有PNG文件的后缀名前的空格替换为下划线

import os


def rename_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.png'):
                new_file = file.replace(' ', '_')
                os.rename(os.path.join(root, file), os.path.join(root, new_file))
                print('Renamed:', file, '->', new_file)


rename_files('F:/OneDrive - Fornaxignis/Dev/sandberrypi/www/painting')
