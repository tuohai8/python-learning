# chatbot.py —— DeepSeek流式对话封装
# 功能：多轮对话、流式输出、自定义AI人设、异常处理、历史管理
# 使用：
# from chatbot import ChatBot
# bot = ChatBot()
# bot.chat("你好")
# 依赖：
# pip install requests


# =========================
# 导入模块
# =========================

import os
import json
import time
import requests

from datetime import datetime



# =========================
# API配置
# =========================

url = "https://api.deepseek.com/chat/completions"


# 从系统环境变量读取API Key
# 避免把key直接写进代码上传GitHub

API_KEY = os.environ.get("DEEPSEEK_API_KEY")


# 如果没有找到key，程序直接提醒
if not API_KEY:
    raise ValueError(
        "没有找到 DEEPSEEK_API_KEY，请先配置环境变量"
    )


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}




# =========================
# AI人设Prompt
# =========================

system_prompt = """
你是一名陪伴用户学习Python、后端和AI应用开发的技术导师。

你的身份：
帮助用户学习Python、后端开发和AI应用开发。

你的特点：
1. 解释代码时先讲原理，再讲具体代码。
2. 发现用户理解错误时直接指出，不盲目夸奖。
3. 会通过提问检查用户是否真正理解。

说话方式：
- 简洁直接，不说无意义的话。
- 先分析问题，再给解决方案。
- 代码示例要解释为什么这样写。

禁止：
- 不确定的信息不要编造。
- 不直接替用户完成所有思考，要引导用户分析。
"""




# =========================
# 日志配置
# =========================


# 创建日志文件夹

os.makedirs(
    "logs",
    exist_ok=True
)


LOG_FILE = "logs/chat.log"





# =========================
# ChatBot核心类
# =========================

class ChatBot:


    def __init__(
        self,
        model="deepseek-chat",
        temperature=0.7,
        max_history=10
    ):

        # 使用的大模型
        self.model = model


        # 控制回答随机程度
        self.temperature = temperature


        # 保存多少轮聊天
        # 一轮 = 用户 + AI
        self.max_history = max_history


        # 对话历史
        # 第0个永远保存system
        self.messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]



    # =========================
    # 日志函数
    # =========================

    def _log(self, level, message):

        time_now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                f"{time_now} [{level}] {message}\n"
            )



    # =========================
    # API请求函数
    # =========================

    def _request(self):

        """
        负责发送API请求
        如果429限流，自动重试一次
        """


        for retry in range(2):

            response = requests.post(

                url,

                headers=headers,

                json={
                    "model": self.model,

                    "messages": self.messages,

                    "stream": True,

                    "temperature": self.temperature
                },


                # 开启流式接收

                stream=True,


                # 最大等待时间

                timeout=20
            )


            # 如果没有限流
            # 直接返回

            if response.status_code != 429:

                return response



            # 429说明请求太频繁

            self._log(
                "WARN",
                "触发429限流，等待重试"
            )


            print(
                "请求过于频繁，2秒后重试..."
            )


            time.sleep(2)



        return response






    # =========================
    # 核心聊天函数
    # =========================

    def chat(self, question):


        # 保存用户问题

        self.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        # 用来保存完整AI回答

        answer = ""



        try:


            # 请求API

            response = self._request()



            # 检查HTTP状态

            response.raise_for_status()



            # =====================
            # 流式读取
            # =====================


            for line in response.iter_lines():


                # requests返回bytes
                # 转换字符串

                line = line.decode(
                    "utf-8"
                )



                # 空行跳过

                if line == "":
                    continue



                # AI结束标志

                if line.strip() == "data: [DONE]":

                    break



                # SSE格式：
                # data: {...}

                if line.startswith(
                    "data: "
                ):

                    line = line[6:]



                # JSON解析保护

                try:

                    data = json.loads(
                        line
                    )


                except json.JSONDecodeError:

                    continue




                # 获取本次chunk文字

                content = (
                    data["choices"][0]
                    ["delta"]
                    .get("content")
                )



                if content:


                    # 边生成边打印

                    print(
                        content,
                        end="",
                        flush=True
                    )


                    # 拼接完整回答

                    answer += content




        except requests.exceptions.Timeout:


            print(
                "请求超时，请稍后再试"
            )


            self._log(
                "ERROR",
                "请求超时"
            )


            self.messages.pop()

            return None




        except requests.exceptions.ConnectionError:


            print(
                "网络连接失败"
            )


            self._log(
                "ERROR",
                "网络连接失败"
            )


            self.messages.pop()

            return None




        except requests.exceptions.HTTPError as e:


            print(
                "HTTP错误:",
                e
            )


            self._log(
                "ERROR",
                str(e)
            )


            self.messages.pop()

            return None




        except Exception as e:


            print(
                "其他错误:",
                e
            )


            self._log(
                "ERROR",
                str(e)
            )


            self.messages.pop()

            return None




        # =====================
        # 保存AI回答
        # =====================


        if answer:


            self.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


        else:


            self.messages.pop()



        # =====================
        # 历史裁剪
        # =====================


        system_message = self.messages[0]


        history = self.messages[1:]


        self.messages = (

            [system_message]

            +

            history[
                -2 * self.max_history:
            ]

        )



        self._log(
            "INFO",
            "聊天成功"
        )


        return answer






    # =========================
    # 清空历史
    # =========================

    def clear_history(self):


        self.messages = [

            {
                "role": "system",
                "content": system_prompt
            }

        ]


        self._log(
            "INFO",
            "历史清空"
        )







# =========================
# 测试入口
# =========================

if __name__ == "__main__":


    bot = ChatBot()


    print(
        "AI助手启动，输入exit退出"
    )


    while True:


        question = input(
            "你："
        )


        if question.strip() == "":

            continue



        if question in [
            "exit",
            "quit"
        ]:

            break



        if question == "clear":

            bot.clear_history()

            print(
                "历史已清空"
            )

            continue



        answer = bot.chat(
            question
        )


        print()