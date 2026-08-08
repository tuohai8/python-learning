# Day 5（8.5）· 作品1第3.5步：合体——流式 + 多轮 + 历史管理
import os
import json
import requests


url = "https://api.deepseek.com/chat/completions"


API_KEY = os.environ.get("DEEPSEEK_API_KEY")


if not API_KEY:
    raise ValueError("没有找到 DEEPSEEK_API_KEY")


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"}
# 【目标】把前几天的零件组装成一个完整顺手的聊天工具
#
# 【需求】
# 1. 多轮对话 + 流式输出同时工作（边回复边记进历史）
# 2. 流式收完后，把拼接好的完整回复追加进对话历史
# 3. 历史裁剪、异常处理保持有效
# 4. 加两个小体验（自己选做）：
#    - 启动时打印一句欢迎语
#    - AI思考时先显示"正在输入..."，第一块文字到了再清掉
#
# 【提示】
# - 流式的坑：文字是一块块来的，得用变量把完整回复攒起来，最后才能入历史
# - 结构参考：输入 -> 追加历史 -> 流式请求(边收边打边攒) -> 攒完的完整回复入历史 -> 裁剪
#
# 【完成标志】
# 连续流式聊10轮：有记忆、不崩、历史不爆炸、字是蹦出来的
#
# 【最低消费】
# 只完成"流式回复攒起来入历史"这一处，选做项跳过
#
# ---------- 以下全部留白，自己写 ----------
print("AI助手启动，输入exit退出")
messages = [
    {
        "role": "system",
        "content": "你是一名python助手"
    }
]
N=10

while True:
    question=input("你：")
    if question.strip()=="":
        continue
    if question in["exit","quit"]:
        break
    answer = ""
    messages.append({ "role": "user",
            "content": question})
    try:
        response = requests.post(
            url,
            headers=headers,
            json={
                "model": "deepseek-chat",
                "messages": messages,
                "stream": True
            },
            timeout=20,
            stream=True
        )

        response.raise_for_status()



        for line in response.iter_lines():

            line = line.decode("utf-8")

            if line == "":
                continue

            if line.strip() == "data: [DONE]":
                break

            if line.startswith("data: "):
                line = line[6:]

            data = json.loads(line)

            content = data["choices"][0]["delta"].get("content")

            if content:
                print(content, end="", flush=True)
                answer += content
    except requests.exceptions.Timeout:
        print("请求超时，请稍后再试")
        messages.pop()
        continue
    except requests.exceptions.ConnectionError:
        print("网络连接失败")
        messages.pop()
        continue
    except Exception as e:
        print("其他错误",e)
        messages.pop()
        continue
    print()
    if answer:
      messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
    system_message = messages[0]

    history = messages[1:]

    messages = [
                   system_message
               ] + history[-2 * N:]
    
















