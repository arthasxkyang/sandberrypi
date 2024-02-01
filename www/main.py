from flask import *
from .db import *
import pygame
from .sandpainting import *
import os
import time

bp = Blueprint("main", __name__, url_prefix="/main")
每毫米步数 = 100
b暂停 = []
b暂停.append(0)
当前G代码列表 = []
当前播放列表 = []
当前播放列表位置 = []
当前播放列表位置.append(0)
当前播放的沙画名称 = []
当前播放的沙画名称.append("")


@bp.route("/media/play/<filename>")

# 沙画的结构由:沙画名称/缩略图/音乐/备注组成
# 分别以沙画名称为文件名保存在painting/media/remark目录下
# list目录是自定义播放集,以播放集名称为文件名保存
# 开机直接播放init沙画


def 播放音乐(filename):
    # 系统开始播放音乐，文件位置在media文件夹下
    # 判断结尾是否是MP3
    if filename:
        pygame.mixer.init()
        pygame.mixer.music.set_volume(10)
        pygame.mixer.music.load(f"www/media/{filename}.mp3")
        pygame.mixer.music.play()
        return f"正在播放{filename}"
    else:
        return "不支持的文件格式"


@bp.route("/media/stop")
def 停止播放音乐():
    # 系统停止播放
    pygame.mixer.init()
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    return "已停止播放"


@bp.route("/media/pause")
def 暂停播放音乐():
    # 系统暂停播放
    pygame.mixer.music.pause()
    return "已暂停播放"


@bp.route("/media/resume")
def 继续播放音乐():
    # 系统继续播放
    pygame.mixer.music.unpause()
    return "已继续播放"


# 播放沙画
@bp.route("/sc/start/<name>")
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
def 停止播放沙画():
    # 暂停播放沙画
    b暂停[0] = 1
    # 停止播放音乐
    停止播放音乐()
    当前播放的沙画名称[0] = ""
    return "已停止播放"


# 暂停播放沙画
@bp.route("/sc/pause")
def 暂停播放沙画():
    # 暂停播放沙画
    b暂停[0]= 1
    # 暂停播放音乐
    暂停播放音乐()
    return "已暂停播放"


# 继续播放沙画
@bp.route("/sc/resume")
def 继续播放沙画():
    # 继续播放沙画
    b暂停[0]= 0
    执行G代码列表()
    # 继续播放音乐
    继续播放音乐()
    return "已继续播放"


# 播放初始化沙画
@bp.route("/sc/init")
def 播放初始化沙画():
    播放沙画("init")
    return "已初始化沙画"


# 创建一个播放集
@bp.route("/list/create/<name>")
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
        # 打开文件
        with open(f"www/list/{listname}.txt", "w") as f:
            # 写入文件
            f.writelines(lines)
        return "已从播放集删除沙画"
    else:
        return "播放集不存在"


# 播放集顺序播放
@bp.route("/list/play/<listname>")
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
def 遍历painting目录下所有文件的名称():
    # 遍历painting目录下的txt文件的名称
    # 文件名组成为:沙画名称.txt
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
def 返回单个沙画的信息(name):
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


# 播放集随机播放（可选）

# 播放集循环播放（可选）


# 将清理gcode加入到G代码
@bp.route("/gcode/clear")
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
        if b暂停[0]== 1:
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
        播放沙画(当前播放列表[当前播放列表位置])


# 使用香橙派CM4的GPIO,控制4988步进电机,驱动电机,执行命令
# TODO: 电机控制代码

def 执行一行(line):
    # 判断是否是移动命令
    if line.startswith("G1"):
        # 切割字符串
        x = line.split("X")[1].split("Y")[0]
        y = line.split("Y")[1].split("Z")[0]
        # 转换为浮点数
        x = float(x)
        y = float(y)
        # 计算步数
        x_step = x * 每毫米步数
        y_step = y * 每毫米步数
        # 判断是否需要移动x轴
        if x_step != 0:
            # 判断方向
            if x_step > 0:
                # 正向
                # 电机正转
                # 电机控制代码
                time.sleep(0.1)
                # 电机停止
                # 电机控制代码
            else:
                # 反向
                # 电机反转
                # 电机控制代码
                time.sleep(0.1)
                # 电机停止
                # 电机控制代码
        # 判断是否需要移动y轴
        if y_step != 0:
            # 判断方向
            if y_step > 0:
                # 正向
                # 电机正转
                # 电机控制代码
                time.sleep(0.1)
                # 电机停止
                # 电机控制代码
            else:
                # 反向
                # 电机反转
                # 电机控制代码
                time.sleep(0.1)
                # 电机停止
                # 电机控制代码


播放初始化沙画()