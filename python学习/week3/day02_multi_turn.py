# Day 2（8.2）· 作品1第2步：多轮对话
#
# 【目标】让AI拥有记忆——它记得住你上面说过的话
#
# 昨天你的AI是"一问一答"，每句话都是陌生人。
# 今天把对话历史一起发给API，让它接上上下文。
import os
import requests


url = "https://api.deepseek.com/chat/completions"


API_KEY = os.environ.get("DEEPSEEK_API_KEY")


if not API_KEY:
    raise ValueError("没有找到 DEEPSEEK_API_KEY")


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"}
# 【需求】
# 1. 用一个列表维护对话历史（每条消息 = 角色 + 内容）
# 2. 每轮对话：用户输入 -> 追加进历史 -> 把完整历史发给API -> 打印回复 -> 把回复也追加进历史
# 3. 支持循环聊天，直到用户输入退出指令
#
# 【提示】
# - API 的 messages 参数就是对话历史：
#   [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}, ...]
# - 结构骨架：while 循环里完成"输入->追加->请求->打印->追加"五步
# - 先不管历史变长的问题，Day3 会处理
# - 复用你day1.py的ask_ai思路，但这次messages不再是临时组装，而是"历史"这个变量
#
# 【完成标志】
# 连续聊5轮以上，先告诉它"我叫拓海"，隔几轮问"我叫什么"，它答得出来
#
# 【最低消费】（不想做的日子只做这步）
# 只写"把历史列表传给API"这一处改动，跑通就算数
#
# ---------- 以下全部留白，自己写 ----------
messages = [
    {
        "role":"system",
        "content":"你是一名python助手"
    }
]
username=None
while True:

    question = input("你：")
    if question in ["exit", "退出"]:
        break
    if question.startswith("我叫"):
        username = question.replace("我叫", "")
        print("已保存用户名:", username)

    messages.append(
        {
            "role":"user",
            "content":question
        }
    )
    response = requests.post(
        url,
        headers=headers,
        json={
            "model": "deepseek-chat",
            "messages": messages
        }
    )
    result = response.json()

    answer = result["choices"][0]["message"]["content"]

    print("AI:", answer)
    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )




