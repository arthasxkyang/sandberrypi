# coding=utf-8

import os
from time import sleep

import pygame
# import serial
from flask import *
from .stepper import Stepper

bp = Blueprint("main", __name__, url_prefix="/main")
每毫米步数 = 50
b暂停 = [0]
当前G代码列表 = []
当前播放列表 = []
当前播放列表位置 = [0]
当前播放的沙画名称 = [""]
初始化沙画名称 = '龙年大吉'
配置 = {"比例伸缩": 0.5, "运动速度(米/秒)": 0.01, "每毫米步数": 每毫米步数}
状态 = dict(当前x坐标=float(0), 当前y坐标=float(0), 移动中=False)


@bp.route("/media/play/<filename>")
# 沙画的结构由:沙画名称/缩略图/音乐/备注组成
# 分别以沙画名称为文件名保存在painting/media/remark目录下
# list目录是自定义播放集,以播放集名称为文件名保存
# 开机直接播放init沙画
# 播放音乐
# 返回值:"正在播放+filename" 或者是 "不支持的文件格式"
def 播放音乐(filename):
    # 系统开始播放循环音乐，文件位置在media文件夹下
    # 判断结尾是否是MP3
    if filename:
        pygame.mixer.init()
        pygame.mixer.music.set_volume(10)
        # 如果这个mp3文件存在，则播放，不存在就播放默认音乐init.mp3
        if not os.path.exists(f"www/media/re/{filename}.mp3"):
            filename = "init"
            pygame.mixer.music.load(f"www/media/{filename}.mp3")
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.load(f"www/media/re/{filename}.mp3")
            pygame.mixer.music.play(-1)
        return f"正在播放{filename}"
    else:
        return "不支持的文件格式"


@bp.route("/media/volume/<volume>")
# 设置音量
# 函数接受一个浮点数作为参数，
# 表示音量的大小。音量参数的上下限是0.0到1.0之间，
# 其中0.0表示静音，1.0表示最大音量。
# 你可以根据需要选择任何介于这两个值之间的音量大小。
# 例如，0.5表示一半的音量大小。
# 返回值:"音量设置为+volume" 或者是 "音量设置失败"
def 设置音量(volume):
    # 设置音量
    try:
        pygame.mixer.music.set_volume(float(volume))
        return f"音量设置为{volume}"
    except:
        return "音量设置失败"


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
    归零()
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


# 创建一个usr播放集
@bp.route("/list/create/<name>")
# 返回值:"已创建播放集" 或者是 "播放集已存在"
def 创建一个播放集(name):
    # 判断list文件夹里是否有同名文件
    if os.path.exists(f"www/list/usr/{name}.txt"):
        return "播放集已存在"
    else:
        # 创建一个同名文件
        with open(f"www/list/usr/{name}.txt", "w", encoding='utf-8') as f:
            f.write("")
    return "已创建播放集"


# 添加沙画到usr播放集
@bp.route("/list/add/<listname>/<sandpaintingname>")
# 返回值:"已添加沙画到播放集" 或者是 "播放集不存在"
def 添加沙画到播放集(listname, sandpaintingname):
    # 判断list文件夹里是否有同名文件
    if os.path.exists(f"www/list/usr/{listname}.txt"):
        # 打开文件
        with open(f"www/list/usr/{listname}.txt", "a", encoding='utf-8') as f:
            # 写入沙画名
            f.write(f"{sandpaintingname}\n")
        return "已添加沙画到播放集"
    else:
        return "播放集不存在"


# 从usr播放集删除沙画
@bp.route("/list/delete/<listname>/<sandpaintingname>")
# 返回值:"已从播放集删除沙画" 或者是 "播放集不存在"
def 从播放集删除沙画(listname, sandpaintingname):
    # 判断list文件夹里是否有同名文件
    if os.path.exists(f"www/list/usr/{listname}.txt"):
        # 打开文件
        with open(f"www/list/usr/{listname}.txt", "r", encoding='utf-8') as f:
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
        # 将删除后的内容写入文件
        with open(f"www/list/usr/{listname}.txt", "w", encoding='utf-8') as f:
            for line in lines:
                f.write(line)
        return "已从播放集删除沙画"
    else:
        return "播放集不存在"


# pre播放集顺序播放
@bp.route("/list/pre/play/<listname>")
# 返回值:"已开始顺序播放播放集" 或者是 "播放集不存在"
def pre播放集顺序播放(listname):
    # 判断list文件夹里是否有同名文件
    if os.path.exists(f"www/list/pre/{listname}.txt"):
        # 清空当前播放列表,重置播放位置
        当前播放列表.clear()
        当前播放列表位置[0] = 0
        # 打开文件
        with open(f"www/list/pre/{listname}.txt", "r", encoding='utf-8') as f:
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


# usr播放集顺序播放
@bp.route("/list/usr/play/<listname>")
# 返回值:"已开始顺序播放播放集" 或者是 "播放集不存在"
def usr播放集顺序播放(listname):
    # 判断list文件夹里是否有同名文件
    if os.path.exists(f"www/list/usr/{listname}.txt"):
        # 清空当前播放列表,重置播放位置
        当前播放列表.clear()
        当前播放列表位置[0] = 0
        # 打开文件
        with open(f"www/list/usr/{listname}.txt", "r", encoding='utf-8') as f:
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


# 读取pre播放集,返回播放集列表用于前端显示
@bp.route("/list/pre/read/<listname>")
# 返回值:正在读取的播放集的变量值 或者是 "播放集不存在"
def pre读取播放集(listname):
    # 判断list文件夹里是否有同名文件
    if os.path.exists(f"www/list/pre/{listname}.txt"):
        正在读取的播放集 = []
        # 打开文件
        with open(f"www/list/pre/{listname}.txt", "r", encoding='utf-8') as f:
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


# 读取usr播放集,返回播放集列表用于前端显示
@bp.route("/list/usr/read/<listname>")
# 返回值:正在读取的播放集的变量值 或者是 "播放集不存在"
def usr读取播放集(listname):
    # 判断list文件夹里是否有同名文件
    if os.path.exists(f"www/list/usr/{listname}.txt"):
        正在读取的播放集 = []
        # 打开文件
        with open(f"www/list/usr/{listname}.txt", "r", encoding='utf-8') as f:
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


# 遍历list/pre目录下所有存在文件的名称用于前端显示
@bp.route("/list/pre/readall")
# 返回值:播放集名称列表得变量值
def 遍历list目录下pre所有文件的名称():
    # 遍历list目录下的txt文件的名称
    播放集名称列表 = []
    for filename in os.listdir("www/list/pre"):
        # 判断是否是txt文件
        if filename.endswith(".txt"):
            # 去除后缀
            filename = filename.split(".")[0]
            # 添加到列表
            播放集名称列表.append(filename)
    return 播放集名称列表


# 遍历list/usr目录下所有存在文件的名称用于前端显示
@bp.route("/list/usr/readall")
# 返回值:播放集名称列表得变量值
def 遍历list目录下usr所有文件的名称():
    # 遍历list目录下的txt文件的名称
    播放集名称列表 = []
    for filename in os.listdir("www/list/usr"):
        # 判断是否是txt文件
        if filename.endswith(".txt"):
            # 去除后缀
            filename = filename.split(".")[0]
            # 添加到列表
            播放集名称列表.append(filename)
    return 播放集名称列表


@bp.route("/list/usr/reorder/<listname>/<content>")
# 传入的content是一个字符串,里面包含了沙画名称,以逗号分隔,删除逗号,使用换行符连接
# 将传入的字符串按逗号分隔后,覆盖存储到对应的文件中
# 返回值:"已重新排序播放集" 或者是 "播放集不存在, 创建播放集"
def usr重新排序播放集(listname, content):
    # 判断list文件夹里是否有同名文件
    if os.path.exists(f"www/list/usr/{listname}.txt"):
        model = "已重新排序播放集"
    else:
        model = "播放集不存在, 创建播放集"
    # w模式打开
    with open(f"www/list/usr/{listname}.txt", "w", encoding='utf-8') as f:
        # 将传入的字符串按逗号分隔
        content_edited = content.replace(",", "\n")
        # 覆盖存储到对应的文件中
        f.write(content_edited)
    return {"模式": model, "内容": content_edited}


@bp.route("/list/usr/direct/<listname>", methods=["POST"])
# 使用request.get_data(as_text=True)获取传入的文本
# 将传入的文本覆盖存储到对应的文件中
# 返回值:"已修改播放集" 或者是 "播放集不存在，创建播放集"
def usr直接修改播放集(listname):
    # 判断list文件夹里是否有同名文件
    if os.path.exists(f"www/list/usr/{listname}.txt"):
        # 打开文件
        with open(f"www/list/usr/{listname}.txt", "w", encoding='utf-8') as f:
            # 写入传入的文本
            f.write(request.get_data(as_text=True))
        return f"已修改播放集, 内容为:\n{request.get_data(as_text=True)}"
    else:
        # 创建一个同名文件
        with open(f"www/list/usr/{listname}.txt", "w", encoding='utf-8') as f:
            # 写入传入的文本
            f.write(request.get_data(as_text=True))
        return f"播放集不存在, 创建播放集, 内容为:\n{request.get_data(as_text=True)}"


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
    # return 'Hello World'


# 读取类别文件,按类别返回沙画名称列表
@bp.route("/tag/read/<tagname>")
# 返回值:沙画名称列表的变量值
def 按类别返回沙画名称列表(tagname):
    沙画名称列表 = []
    # 打开文件
    try:
        with open(f"www/tag/{tagname}.txt", "r", encoding='utf-8') as f:
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
    except:
        return "出错了"


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
    with open(f"www/remark/{name}.txt", "r", encoding='utf-8') as f:
        沙画结构["remark"] = f.read()
    # except:
    #     沙画结构["remark"] = "会当凌绝顶，一览众山小"
    # 如果当前播放的沙画名称是当前沙画,则添加播放状态为正在播放.
    if 当前播放的沙画名称[0] == name & b暂停[0] == 0:
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
        with open(f"www/gcode/clear.gcode", "r", encoding='utf-8') as f:
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

    # 打开文件
    try:
        with open(f"www/gcode/{filename}.gcode", "r", encoding='utf-8') as f:
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


# 使用香橙派CM4控制4988步进电机,驱动电机,执行命令
# TODO: 电机控制代码
开发测试 = 2
串口配置 = {"port": 'COM22', "bdr": 115200}

if 开发测试 == 2:
    for i in range(10):
        try:
            # 打开串口
            stepper = Stepper(port=串口配置["port"], bdr=串口配置["bdr"])
            break
        except:
            print(f"[ERROR] 串口打开失败,第{i + 1}次尝试!!!")
            sleep(1)
    print(f"[ERROR] 串口打开失败!!!程序继续执行!!!")


@bp.route("/execute/<line>")
def 执行一行(line):
    # 将%20替换为空格
    line_url_decoded = line.replace("%20", " ")
    # 解析 x坐标和y坐标
    if "X" in line_url_decoded:
        gcode90_X = line_url_decoded.split("X")[1].split(" ")[0]
        gcode90_X = float(gcode90_X * 配置["比例伸缩"])
    else:
        gcode90_X = -1
    if "Y" in line_url_decoded:
        gcode90_Y = line_url_decoded.split("Y")[1].split(" ")[0]
        gcode90_Y = float(gcode90_Y * 配置["比例伸缩"])
    else:
        gcode90_Y = -1
    # 根据当前坐标和目标坐标计算步数
    if gcode90_X != -1:
        delta_X = gcode90_X - 状态["当前x坐标"]
    else:
        delta_X = 0
    if gcode90_Y != -1:
        delta_Y = gcode90_Y - 状态["当前y坐标"]
    else:
        delta_Y = 0
    # 计算X和Y的增量的绝对值和符号,符号以1和2表示
    delta_X_abs = abs(delta_X)
    delta_Y_abs = abs(delta_Y)
    delta_X_sign = 1 if delta_X >= 0 else 2
    delta_Y_sign = 1 if delta_Y >= 0 else 2
    # 计算直线差值运动长度
    delta_L = (delta_X_abs ** 2 + delta_Y_abs ** 2) ** 0.5
    # 计算运动时间
    time = int(delta_L / 配置["运动速度"])
    # 计算步数
    step_X = int(delta_X_abs * 每毫米步数)
    step_Y = int(delta_Y_abs * 每毫米步数)
    # 将step_X,stepY,time 发送到串口
    # 串口发送
    stepper.move(step_X, step_Y, time)
    result = {"传递的参数为": line, "URL解码结果": line_url_decoded, "串口拼接结果": line_prepared4_serial,
              "串口实际发送": f"{line_prepared4_serial.encode()}",
              "报告": "已执行一行", "返回结果": data.decode()}
    print(result)
    if data.decode() == "success":
        # 更新当前坐标
        状态["当前x坐标"] = 状态["当前x坐标"] + delta_X
        状态["当前y坐标"] = 状态["当前y坐标"] + delta_Y
        print(f"执行成功, 当前坐标为:({状态['当前x坐标']},{状态['当前y坐标']})")
        return result
    else:
        print("执行失败,正在重新执行")
        执行一行(line)


@bp.route("/axis-home")
def 归零():
    # 串口发送归零请求
    # TODO: 串口发送归零请求
    归零请求 = b'G28\n'
    ser.write(归零请求)
    # 接收归零成功信息
    while True:
        data = ser.readline()
        if data:
            break
    # 如果接收到归零成功信息,返回成功
    if data.decode() == "success":
        # 重置当前坐标
        状态["当前x坐标"] = 0
        状态["当前y坐标"] = 0
        return "归零成功"
    else:
        return "归零失败"


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

# 下面是一些测试用函数

# 测试函数结束

# 会阻塞后续程序初始化,导致无法直接进入端口监听状态
# 播放初始化沙画()
