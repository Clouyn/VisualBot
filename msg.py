# 处理与信息相关的脚本
import random

import pyautogui  # 控制鼠标和键盘
import pyperclip  # 操作剪贴板
import yaml

import ai
import global_data

# 读取YAML文件
with open("config.yml", "r", encoding='utf-8') as file:
    config = yaml.safe_load(file)


# 检测是否有新消息
def find():
    try:
        # 如果检测到新消息（因为调用了locateOnScreen，所以没有try程序会崩的）
        # 定位news，icons3的位置
        left, top, width, height = pyautogui.locateOnScreen("photo/news.png", grayscale=False, confidence=0.9)
        y = top
        left, top, width, height = pyautogui.locateOnScreen("photo/icons3.png", grayscale=False, confidence=0.9)
        x = left
        try:
            # 确认该群是否为检测的头像
            left, top, width, height = pyautogui.locateOnScreen(global_data.check_photo, grayscale=False, confidence=0.9)
            if abs(left - x) < 50 and abs(top - y) < 30:
                # 如果是检测的头像，那么点击并进入聊天界面并且返回True
                print("###发现了新消息")
                pyautogui.moveTo(left, top)
                pyautogui.click()
                return True
            left, top, width, height = pyautogui.locateOnScreen(config["admin_photo"], grayscale=False, confidence=0.9)
            if abs(left - x) < 50 and abs(top - y) < 30:
                # 如果是检测的管理员，那么点击并进入聊天界面并且调用admin函数
                print("###发现了管理员的新消息")
                pyautogui.moveTo(left, top)
                pyautogui.click()
                admin()
            # 不是监测好友/群聊的消息，消除消息提示
            pyautogui.moveTo(x, y)
            pyautogui.click()
            return_zero()
        except:
            pass
    except:
        pass


# 获取聊天界面的新消息
def get():
    try:
        # 截屏并且给Ai识别聊天记录
        # 获取左下角icons图标位置
        left, top, width, height = pyautogui.locateOnScreen("photo/icons.png", confidence=0.9)
        x1 = int(left - 10)
        y1 = int(top - 10)
        # 获取右下角icons2图标位置
        left, top, width, height = pyautogui.locateOnScreen("photo/icons2.png", confidence=0.9)
        x2 = int(left + 20)
        y2 = int(top + 35)
        # 在聊天界面的区域内截屏，并且保存至photo文件夹
        pyautogui.screenshot(region=(x1, y2, (x2 - x1), (y1 - y2))).save("photo/chat_photo.png")
        # 让ai分析聊天记录的内容
        ai_text = ai.call_photo(config["ai_chatlist"], "photo/chat_photo.png")
        print("###获取到了新消息")
        print(ai_text)
        # 返回分析好的聊天记录
        return ai_text
    except:
        print("msg.get error")


def old_get():
    try:
        left, top, width, height = pyautogui.locateOnScreen("photo/icons.png", confidence=0.9)
        pyautogui.moveTo(left + 60, top - 40)
        for i in range(3):
            pyautogui.click()
        pyautogui.hotkey('ctrl', 'c')
        msg = pyperclip.paste()
        print("###获取到了新消息")
        return msg
    except:
        print("msg.old_get error")


# 发送消息
def send(msg):
    try:
        # 获取icons的位置，并且在该位置下方点击聊天框
        left, top, width, height = pyautogui.locateOnScreen("photo/icons.png", confidence=0.9)
        pyautogui.moveTo(left + 20, top + 60)
        pyautogui.click()
        for text in msg:
            # 将即将发送的消息拷贝至粘贴板，并且粘贴至聊天框后发送
            pyperclip.copy(text)
            pyautogui.hotkey("ctrl", "v")
            pyautogui.press("enter")
        print(f"###发送消息成功！消息内容：{msg}")
    except:
        print("msg.send error")


# 处理Bot发送的消息使Bot的发言更像人类
def process(text):
    try:
        # 导入emoji库
        emoji = {"快乐": "😄", "平静": "🧐", "幽默": "😋", "伤心": "😭"}
        # 如果拒绝回答则直接返回
        if not ("拒绝回答" in text):
            # 定义发送文本，分割Ai回答的内容
            send_text = []
            processed_text = text.split("###")
            symbol_text = processed_text[0].split("，")
            # 将分割好的内容一一加入列表
            for temp_text in symbol_text:
                send_text.append(temp_text)
            # 随机给最后一句话打上括号（，（）
            if random.randint(1, 3) == 1:
                if random.randint(1, 4) == 1:
                    send_text[-1] += "()"
                else:
                    send_text[-1] += "("
            # 随机加入一个emoji
            # if random.randint(0, 2) == 1:
            #   send_text.append(emoji[processed_text[1]])
            return send_text
        else:
            return ["拒绝回答"]
    except:
        print("msg.process error")


# 复原以待命下一次获取消息
def return_zero():
    try:
        # 获取自己qq的头像并且点击进入
        left, top, width, height = pyautogui.locateOnScreen("photo/myself.png", confidence=0.9)
        pyautogui.click(left, top)
        # print("###归零")
    except:
        pass


def admin():
    msg = old_get()
    process_msg = msg.split(" ")
    if process_msg[0] == "test":
        send(["测试"])
    elif process_msg[0] == "change":
        global_data.check_photo = process_msg[1]
        send([global_data.check_photo])
        print(global_data.check_photo)
    elif process_msg[0] == "exit":
        if str(config["exit_key"]) == process_msg[1]:
            send(["###程序结束"])
            global_data.is_exit = True
