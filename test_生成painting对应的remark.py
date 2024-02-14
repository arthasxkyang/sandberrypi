import os

import requests
from time import sleep

# 使用一言api去自动生成，便于测试

def generate_remark_file():
    for root, dirs, files in os.walk("./www/painting"):
        # 下面的for循环每次间隔1秒
        for file in files:
            if file.endswith('.png'):
                txt_file = file.replace('.png', '.txt')
                if not os.path.exists(f'./www/remark/{txt_file}'):
                    # 以UTF-8编码打开文件并写入内容
                    with open(f'./www/remark/{txt_file}', 'w', encoding='utf-8') as workingfile:
                        sleep(1)
                        response = requests.get('https://v1.hitokoto.cn/?c=d')
                        if response.status_code == 200:
                            hitokoto = response.json()
                        else:
                            hitokoto = {"hitokoto": "接口未返回内容", "from": "接口未返回内容"}
                        workingfile.write(f'{hitokoto["hitokoto"]}\n出自《{hitokoto["from"]}》')
                        print(f'Generated {txt_file}')
                else:
                    print(f'{txt_file} already exists')
    return "已生成所有沙画的备注"


generate_remark_file()
