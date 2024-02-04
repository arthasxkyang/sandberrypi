# unicoding: utf-8
from flask import *

bp = Blueprint("indexpage", __name__, url_prefix="/indexpage")


@bp.route("/go")
def go():
    返回字符串 = []
    下一个def保留 = [0]
    # 将main.py中的所有url和对应的函数名称附加到返回字符串
    with open("www/main.py", "r", encoding="utf-8") as f:
        for line in f.readlines():
            if "@bp.route" in line:
                # 只提取引号内的,需要将<和>替换为字符实体
                提取的line = line.split('"')[1].replace("<", "&#60").replace(">", "&#62")
                加入了换行标签的line = f"<b>localhost:5000/main{提取的line}</b>" + "<br>"
                返回字符串.append(加入了换行标签的line)
                下一个def保留[0] = 1
                continue

            if "def " in line and 下一个def保留[0]:
                # 加入<br>换行标签
                加入了换行标签的line = line.strip() + "<br><br>"
                返回字符串.append(加入了换行标签的line)
                下一个def保留[0] = 0
                continue
            if 下一个def保留[0]:
                提取的line = line.strip().replace("<", "&#60").replace(">", "&#62")
                加入了换行标签的line = f"<i>{提取的line}</i>" + "<br>"
                返回字符串.append(加入了换行标签的line)
                continue
    return f"<html><head></head><body><div><p>开发者你好!<br>以下是main.py中的所有url和对应的函数名称<br><br>{''.join(返回字符串)}</p></div></body></html>"
