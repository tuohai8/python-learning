# chatbot.py —— RAG问答系统的AI生成模块
# 功能：
# 1. 管理聊天上下文
# 2. 调用DeepSeek API
# 3. 根据问题+资料生成答案
# 4. 流式输出


import os
import json
import requests


# ==============================
# 模块1：API配置
# ==============================


URL = "https://api.deepseek.com/chat/completions"


API_KEY = os.environ.get(
    "DEEPSEEK_API_KEY"
)


if not API_KEY:
    raise ValueError(
        "没有找到DEEPSEEK_API_KEY"
    )


HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}



SYSTEM_PROMPT = """
你是一名企业知识库AI助手。

回答规则：
1. 优先根据提供的资料回答。
2. 如果资料没有答案，明确说明不知道。
3. 不要编造不存在的信息。
"""



# ==============================
# 模块2：ChatBot类
# ==============================


class ChatBot:


    def __init__(
        self,
        model="deepseek-chat",
        temperature=0.3,
        max_history=5
    ):


        self.model = model

        self.temperature = temperature

        self.max_history = max_history


        # 保存上下文

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]



    # ==============================
    # 模块3：核心问答方法
    # ==============================


    def chat(
        self,
        question,
        context
    ):


        # 1. 拼接RAG资料和用户问题


        prompt = f"""
根据以下资料回答问题：

资料：
{context}


问题：
{question}


如果资料中没有答案，请说明。
"""


        # 保存用户输入

        self.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )



        try:


            # 2. 请求DeepSeek


            response = requests.post(
                URL,
                headers=HEADERS,
                json={
                    "model": self.model,
                    "messages": self.messages,
                    "temperature": self.temperature,
                    "stream": True
                },
                timeout=30
            )


            response.raise_for_status()



        except Exception as e:


            print(
                "API请求失败:",
                e
            )


            # 删除失败的问题

            self.messages.pop()


            return None




        # ==============================
        # 模块4：流式解析
        # ==============================


        answer = ""


        for line in response.iter_lines():


            if not line:
                continue



            line = line.decode(
                "utf-8"
            )



            if line.strip() == "data: [DONE]":

                break



            if line.startswith(
                "data: "
            ):

                line = line[6:]



            try:

                data = json.loads(
                    line
                )


            except json.JSONDecodeError:

                continue




            content = (
                data
                .get("choices", [{}])[0]
                .get("delta", {})
                .get("content")
            )



            if content:


                print(
                    content,
                    end="",
                    flush=True
                )


                answer += content




        print()



        # ==============================
        # 模块5：保存AI回答
        # ==============================


        self.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )



        # 控制上下文长度


        if len(self.messages) > self.max_history * 2 + 1:


            self.messages = (
                [self.messages[0]]
                +
                self.messages[-self.max_history*2:]
            )


        return answer




    # ==============================
    # 模块6：清空历史
    # ==============================


    def clear_history(self):


        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]




