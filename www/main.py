# coding=utf-8

from flask import *

import pygame
import os

import serial

bp = Blueprint("main", __name__, url_prefix="/main")
每毫米步数 = 100
b暂停 = [0]
当前G代码列表 = []
当前播放列表 = []
当前播放列表位置 = [0]
当前播放的沙画名称 = [""]
初始化沙画名称 = '龙年大吉'


@bp.route("/media/play/<filename>")
# 沙画的结构由:沙画名称/缩略图/音乐/备注组成
# 分别以沙画名称为文件名保存在painting/media/remark目录下
# list目录是自定义播放集,以播放集名称为文件名保存
# 开机直接播放init沙画
# 播放音乐
# 返回值:"正在播放+filename" 或者是 "不支持的文件格式"
def 播放音乐(filename):
    # 系统开始播放音乐，文件位置在media文件夹下
    # 判断结尾是否是MP3
    if filename:
        pygame.mixer.init()
        pygame.mixer.music.set_volume(10)
        # 如果这个mp3文件存在，则播放，不存在就播放默认音乐init.mp3
        if not os.path.exists(f"www/media/{filename}.mp3"):
            filename = "init"
        pygame.mixer.music.load(f"www/media/{filename}.mp3")
        pygame.mixer.music.play()
        return f"正在播放{filename}"
    else:
        return "不支持的文件格式"


@bp.route("/media/stop")
# 返回值:"已停止播放"
def 停止播放音乐():
    # 系统停止播放
    pygame.mixer.init()
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    return "已停止播放"


@bp.route("/media/pause")
# 返回值:"已暂停播放"
def 暂停播放音乐():
    # 系统暂停播放
    pygame.mixer.music.pause()
    return "已暂停播放"


@bp.route("/media/resume")
# 返回值:"已继续播放"
def 继续播放音乐():
    # 系统继续播放
    pygame.mixer.music.unpause()
    return "已继续播放"


# 播放沙画
@bp.route("/sc/start/<name>")
# 实际上会依次执行以下函数:
# 停止播放沙画()
# 读取gcode文件加载到列表(name)
# 将事前清理gcode加入到G代码()
# 当前播放的沙画名称[0] = name
# 播放音乐(name)
# b暂停[0] = 0
# 执行G代码列表()
# 返回值:"已开始播放"
def 播放沙画(name):
    停止播放沙画()
    读取gcode文件加载到列表(name)
    将事前清理gcode加入到G代码()
    当前播放的沙画名称[0] = name
    播放音乐(name)
    b暂停[0] = 0
    执行G代码列表()
    return "已开始播放"


# 停止播放沙画
@bp.route("/sc/stop")
# b暂停[0] = 1
# 停止播放音乐()
# 当前播放的沙画名称[0] = ""
# 返回值:"已停止播放"
def 停止播放沙画():
    # 暂停播放沙画
    b暂停[0] = 1
    # 停止播放音乐
    停止播放音乐()
    当前播放的沙画名称[0] = ""
    return "已停止播放"


# 暂停播放沙画
@bp.route("/sc/pause")
# b暂停[0] = 1
# 返回值:"已暂停播放"
def 暂停播放沙画():
    # 暂停播放沙画
    b暂停[0] = 1
    # 暂停播放音乐
    暂停播放音乐()
    return "已暂停播放"


# 继续播放沙画
@bp.route("/sc/resume")
# b暂停[0] = 0
# 执行G代码列表()
# 继续播放音乐()
# 返回值:"已继续播放"
def 继续播放沙画():
    # 继续播放沙画
    b暂停[0] = 0
    执行G代码列表()
    # 继续播放音乐
    继续播放音乐()
    return "已继续播放"


# 播放初始化沙画
@bp.route("/sc/init")
# 返回值:"已播放初始化沙画"
def 播放初始化沙画():
    播放沙画(f"{初始化沙画名称}")
    return "已播放初始化沙画"


# 创建一个播放集
@bp.route("/list/create/<name>")
# 返回值:"已创建播放集" 或者是 "播放集已存在"
def 创建一个播放集(name):
    # 判断list文件夹里是否有同名文件
    if os.path.exists(f"www/list/{name}.txt"):
        return "播放集已存在"
    else:
        # 创建一个同名文件
        with open(f"www/list/{name}.txt", "w") as f:
            f.write("")
    return "已创建播放集"


# 添加沙画到播放集
@bp.route("/list/add/<listname>/<sandpaintingname>")
# 返回值:"已添加沙画到播放集" 或者是 "播放集不存在"
def 添加沙画到播放集(listname, sandpaintingname):
    # 判断list文件夹里是否有同名文件
    if os.path.exists(f"www/list/{listname}.txt"):
        # 打开文件
        with open(f"www/list/{listname}.txt", "a") as f:
            # 写入沙画名
            f.write(f"{sandpaintingname}\n")
        return "已添加沙画到播放集"
    else:
        return "播放集不存在"


# 从播放集删除沙画
@bp.route("/list/delete/<listname>/<sandpaintingname>")
# 返回值:"已从播放集删除沙画" 或者是 "播放集不存在"
def 从播放集删除沙画(listname, sandpaintingname):
    # 判断list文件夹里是否有同名文件
    if os.path.exists(f"www/list/{listname}.txt"):
        # 打开文件
        with open(f"www/list/{listname}.txt", "r") as f:
            # 读取文件
            lines = f.readlines()
            # 遍历文件
            for line in lines:
                # 去除换行符
                line = line.strip()
                # 判断是否是注释
                if line.startswith(";"):
                    # 跳过
                    continue
                # 判断是否是要删除的沙画
                if line == sandpaintingname:
                    # 删除
                    lines.remove(line)
        return "已从播放集删除沙画"
    else:
        return "播放集不存在"


# 播放集顺序播放
@bp.route("/list/play/<listname>")
# 返回值:"已开始顺序播放播放集" 或者是 "播放集不存在"
def 播放集顺序播放(listname):
    # 判断list文件夹里是否有同名文件
    if os.path.exists(f"www/list/{listname}.txt"):
        # 清空当前播放列表,重置播放位置
        当前播放列表.clear()
        当前播放列表位置[0] = 0
        # 打开文件
        with open(f"www/list/{listname}.txt", "r") as f:
            # 读取文件
            lines = f.readlines()
            # 遍历文件
            for line in lines:
                # 去除换行符
                line = line.strip()
                # 判断是否是注释
                if line.startswith(";"):
                    # 跳过
                    continue
                # 将沙画添加到播放列表
                当前播放列表.append(line)
        # 开始播放
        播放沙画(当前播放列表[0])
        当前播放列表位置[0] = 0
        return "已开始顺序播放播放集"
    else:
        return "播放集不存在"


# 读取播放集,返回播放集列表用于前端显示
@bp.route("/list/read/<listname>")
# 返回值:正在读取的播放集的变量值 或者是 "播放集不存在"
def 读取播放集(listname):
    # 判断list文件夹里是否有同名文件
    if os.path.exists(f"www/list/{listname}.txt"):
        正在读取的播放集 = []
        # 打开文件
        with open(f"www/list/{listname}.txt", "r") as f:
            # 读取文件
            lines = f.readlines()
            # 遍历文件
            for line in lines:
                # 去除换行符
                line = line.strip()
                # 判断是否是注释
                if line.startswith(";"):
                    # 跳过
                    continue
                # 将沙画添加到播放列表
                正在读取的播放集.append(line)
        return 正在读取的播放集
    else:
        return "播放集不存在"


# 遍历list目录下所有存在文件的名称用于前端显示
@bp.route("/list/readall")
# 返回值:播放集名称列表得变量值
def 遍历list目录下所有文件的名称():
    # 遍历list目录下的txt文件的名称
    播放集名称列表 = []
    for filename in os.listdir("www/list"):
        # 判断是否是txt文件
        if filename.endswith(".txt"):
            # 去除后缀
            filename = filename.split(".")[0]
            # 添加到列表
            播放集名称列表.append(filename)
    return 播放集名称列表


# 遍历painting目录下所有存在文件的名称用于前端显示
@bp.route("/painting/readall")
# 遍历painting目录下的txt文件的名称
# 文件名组成为:沙画名称.txt
# 返回值:沙画名称列表的变量值
def 遍历painting目录下所有文件的名称():
    沙画名称列表 = []
    for filename in os.listdir("www/painting"):
        # 判断是否是png文件
        if filename.endswith(".png"):
            # 去除后缀
            filename = filename.split(".")[0]
            # 添加到列表
            沙画名称列表.append(filename)
    return 沙画名称列表


# 读取沙画类别,返回沙画类别列表用于前端显示
@bp.route("/tag/readall")
# 返回值:沙画类别列表的变量值
def 读取沙画类别():
    # 遍历tag目录下的txt文件的名称
    沙画类别列表 = []
    for filename in os.listdir("www/tag"):
        # 判断是否是txt文件
        if filename.endswith(".txt"):
            # 去除后缀
            filename = filename.split(".")[0]
            # 添加到列表
            沙画类别列表.append(filename)
    return 沙画类别列表


# 读取类别文件,按类别返回沙画名称列表
@bp.route("/tag/read/<tagname>")
# 返回值:沙画名称列表的变量值
def 按类别返回沙画名称列表(tagname):
    沙画名称列表 = []
    # 打开文件
    with open(f"www/tag/{tagname}.txt", "r") as f:
        # 读取文件
        lines = f.readlines()
        # 遍历文件
        for line in lines:
            # 去除换行符
            line = line.strip()
            # 判断是否是注释
            if line.startswith(";"):
                # 跳过
                continue
            # 添加到列表
            沙画名称列表.append(line)
    return 沙画名称列表


# 返回单个沙画的信息
@bp.route("/painting/read/<name>")
# 返回值:沙画的结构
def 返回单个沙画的信息(name):
    # noinspection PyDictCreation
    沙画结构 = {}
    # 添加沙画名称(无类别)
    沙画结构["name"] = name
    # 添加沙画缩略图路径
    沙画结构["thumbnail"] = f"www/painting/{name}.png"
    # 添加沙画音乐
    沙画结构["music"] = f"www/media/{name}.mp3"
    # 添加沙画备注
    沙画结构["remark"] = f"www/remark/{name}.txt"
    # 如果当前播放的沙画名称是当前沙画,则添加播放状态为正在播放.
    if 当前播放的沙画名称[0] == name:
        沙画结构["status"] = "playing"
    else:
        沙画结构["status"] = "stop"
    return 沙画结构


# 播放集随机播放（可选）

# 播放集循环播放（可选）


# 将清理gcode加入到G代码
@bp.route("/gcode/add_clear_gcode")
# 返回值:"已将清理gcode加入到G代码" 或者是 "文件不存在"
def 将事前清理gcode加入到G代码():
    清理G代码列表 = []
    # 打开文件
    try:
        with open(f"www/gcode/clear.gcode", "r") as f:
            # 读取文件
            lines = f.readlines()
            # 遍历文件
            for line in lines:
                # 去除换行符
                line = line.strip()
                # 判断是否是注释
                if line.startswith(";"):
                    # 跳过
                    continue
                # 添加到列表
                清理G代码列表.append(line)
        # "清理G代码列表"的全部内容按顺序插入到到"当前G代码列表"的最前面
        当前G代码列表[:0] = 清理G代码列表
        return "已将清理gcode加入到G代码"
    except:
        return "文件不存在"


# 读取gcode文件加载到列表
def 读取gcode文件加载到列表(filename):
    # 清空当前列表
    当前G代码列表.clear()
    # 打开文件
    try:
        with open(f"www/gcode/{filename}.gcode", "r") as f:
            # 读取文件
            lines = f.readlines()
            # 遍历文件
            for line in lines:
                # 去除换行符
                line = line.strip()
                # 判断是否是注释
                if line.startswith(";"):
                    # 跳过
                    continue
                # 添加到列表
                当前G代码列表.append(line)
            return 当前G代码列表
    except:
        return "文件不存在"


# 从'G代码列表'执行
def 执行G代码列表():
    # 遍历列表,从第一行开始,执行一行然后移除
    # 如果播放完,则播放列表里的下一个沙画
    while len(当前G代码列表) > 0:
        # 如果暂停,则跳出循环
        if b暂停[0] == 1:
            return "检测到暂停为真"
        # 执行一行
        执行一行(当前G代码列表[0])
        # 移除一行
        当前G代码列表.pop(0)
    # 如果播放完,则播放列表里的下一个沙画
    if len(当前G代码列表) == 0:
        当前沙画已完成()
        return "当前沙画已完成"


def 当前沙画已完成():
    # 判断是否是最后一个沙画
    if 当前播放列表位置[0] == len(当前播放列表) - 1:

        # 播放完毕
        return "播放完毕"

    elif len(当前播放列表) == 0:
        return "播放完毕"
    else:
        # 播放下一个沙画
        当前播放列表位置[0] = 当前播放列表位置[0] + 1
        播放沙画(当前播放列表[当前播放列表位置[0]])


# 使用香橙派CM4的GPIO,控制4988步进电机,驱动电机,执行命令
# TODO: 电机控制代码
port = 'COM8'
brt = 115200
b前端开发测试 = 1


@bp.route("/execute/<line>")
# 如果b前端开发测试为真,执行特殊返回
# return {"前端开发测试传递的参数为": line, "report": "已执行一行"}
def 执行一行(line):
    # 如果b前端开发测试为真,则不执行
    if b前端开发测试 == 1:
        # 以json格式返回{前端开发测试传递的参数为：line,report:已执行一行}
        return {"前端开发测试传递的参数为": line, "report": "已执行一行"}
    # 通过serial通讯发送line,波特率115200
    ser = serial.Serial(port, brt, timeout=1)
    ser.write(b'[ESP500] line\n')
    ser.close()
    return "已执行一行"


@bp.route("/status")
# 返回文件中所有变量和对应的值,输出到前端,以json格式
# {
#     "b暂停": 0,
#     "初始化沙画名称": "龙年大吉",
#     "当前G代码列表": [],
#     "当前播放列表": [],
#     "当前播放列表位置": 0,
#     "当前播放的沙画名称": "龙年大吉",
#     "每毫米步数": 100
# }
def 查看状态():
    # 返回文件中所有变量和对应的值,输出到前端,以json格式
    return {"每毫米步数": 每毫米步数, "b暂停": b暂停[0], "当前G代码列表": 当前G代码列表, "当前播放列表": 当前播放列表,
            "当前播放列表位置": 当前播放列表位置[0], "当前播放的沙画名称": 当前播放的沙画名称[0],
            "初始化沙画名称": 初始化沙画名称}


播放初始化沙画()
