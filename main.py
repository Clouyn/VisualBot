# 主程序
import keyboard  # 检测键盘按键
import yaml

import ai
import global_data
import msg

# 读取YAML文件
with open("config.yml", "r", encoding='utf-8') as file:
    config = yaml.safe_load(file)


# 归零初始化
msg.return_zero()
if __name__ == "__main__":
    # 如果这是执行的脚本（及主程序）
    # 定义聊天时间，聊天次数，聊天列表
    chat_time = 0
    chat_ans = 0
    chat_list = []
    print("###启动QQBot")
    while True:
        # 控制Bot的结束与暂停
        if keyboard.is_pressed("home"):
            global_data.is_exit = True
        if keyboard.is_pressed("end"):
            input("###程序暂停")
        if global_data.is_exit:
            print("###程序结束")
            exit()

        try:
            # 如果发现了新消息
            if msg.find():
                # 聊天次数 + 1
                chat_ans += 1
                print(f"###发言计数器：{chat_ans}")
                if chat_ans >= 5:
                    # 如果聊天次数 >= 5，聊天时间 + 1，聊天次数归1
                    chat_ans = 1
                    print("###计数器已满，开始发言")
                    # 获取消息加入至聊天列表
                    chat_list.append(msg.get() + "\n")
                    chat_text = ""
                    if chat_time < 3:
                        # 如果聊天时间 < 3，把0~聊天时间的聊天记录加入聊天文本
                        for i in range(0, chat_time):
                            chat_text += chat_list[i]
                    else:
                        # 否则，把聊天时间 - 3~聊天时间的聊天记录加入聊天文本
                        for i in range(chat_time - 3, chat_time):
                            chat_text += chat_list[i]
                    # 询问Ai，并且处理消息
                    text = msg.process(ai.zhipu_call_text(config["ai_settings"] + chat_text + "\n你：？"))
                    print(text)
                    if not ("拒绝回答" in text[0]):
                        msg.send(text)
                    else:
                        print("###拒绝回答")
                    chat_time += 1
            # 归零
            msg.return_zero()
        except:
            pass
        # time.sleep(0.1)
