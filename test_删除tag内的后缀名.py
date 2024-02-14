# 删除tag目录下的txt文件内每一行的后缀名

import os
import re


def delete_suffix(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                with open(file, 'r') as f:
                    lines = f.readlines()
                with open(file, 'w') as f:
                    for line in lines:
                        f.write(re.sub(r'\.\w+$', '', line))
                    print(f'{file} done')


delete_suffix('./www/tag')
