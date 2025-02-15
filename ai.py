# 处理与调用Ai相关的脚本
import base64
import yaml
from zhipuai import ZhipuAI  # 调用ZhipuAi
from openai import OpenAI  # 调用DeepSeek

# 读取YAML文件
with open("config.yml", "r", encoding='utf-8') as file:
    config = yaml.safe_load(file)

# 定义ZhipuAI的key
zhipu_client = ZhipuAI(api_key=config["zhipu_ai_key"])
ds_client = OpenAI(api_key=config["ds_ai_key"], base_url="https://api.deepseek.com")
# 定义Ai的聊天记录
ai_msg = []
zhipu_ai_msg = []


# 调用DSAi回答对话
def call_text(msg):
    try:
        # 加入用户的新发言
        ai_msg.append({"role": "user", "content": msg})
        # 调用Ai
        response = ds_client.chat.completions.create(
            # 调用的模型名称
            model="deepseek-chat",
            # 与Ai对话的历史记录
            messages=ai_msg,
            stream=False
        )
        # 加入Ai的新发言
        ai_msg.append({"role": "system", "content": response.choices[0].message.content})
        print("###调用Ai回答")
        # 返回Ai回答的文本内容
        return response.choices[0].message.content
    except:
        print("ai.call_text error")


# 调用ZhipuAi回答对话
def zhipu_call_text(msg):
    try:
        # 加入用户的新发言
        zhipu_ai_msg.append({"role": "user", "content": msg})
        # 调用Ai
        response = zhipu_client.chat.completions.create(
            # 调用的模型名称
            model="glm-4-plus",
            # 与Ai对话的历史记录
            messages=zhipu_ai_msg,
        )
        # 加入Ai的新发言
        zhipu_ai_msg.append({"role": "assistant", "content": response.choices[0].message.content})
        print("###调用Ai回答")
        # 返回Ai回答的文本内容
        return response.choices[0].message.content
    except:
        print("ai.zhipu_call_text error")


# 调用Ai分析图片
def call_photo(msg, photo):
    try:
        # 读取照片文件base64，并且转换为url
        img_path = photo
        with open(img_path, "rb") as img_file:
            img_base = base64.b64encode(img_file.read()).decode('utf-8')
        # 调用Ai
        response = zhipu_client.chat.completions.create(
            # 调用的模型名称
            model="glm-4v-plus-0111",
            # 信息（未携带聊天记录）
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                # 照片url
                                "url": img_base
                            }
                        },
                        {
                            "type": "text",
                            # 文本信息
                            "text": msg
                        }
                    ]
                }
            ]
        )
        print("###调用Ai识别图片")
        return response.choices[0].message.content
    except:
        print("ai.call_photo error")
