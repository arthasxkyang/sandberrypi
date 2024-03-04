# coding=utf-8
# 将目录下所有gcode的后缀名前的空格替换为下划线
import os


def rename_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.gcode'):
                new_file = file.replace(' ', '_')
                if file != new_file:
                    os.rename(os.path.join(root, file), os.path.join(root, new_file))
                    print('Renamed:', file, '->', new_file)
                else:
                    print('No need to rename:', file)


# rename_files('./www/gcode')

# 将目录下所有gcode的文件名小括号和其中内容移除
def remove_brackets(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.gcode'):
                new_file = file.split('(')[0] + '.gcode'
                if file != new_file:
                    os.rename(os.path.join(root, file), os.path.join(root, new_file))
                    print('Renamed:', file, '->', new_file)
                else:
                    print('No need to rename:', file)

remove_brackets('./www/gcode')
