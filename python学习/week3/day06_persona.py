# Day 6（8.6）· 作品1第4步：人设——你的AI听你的话
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
# 【目标】写一个属于你自己的 system prompt，给AI定下性格和规矩

# 【需求】
# 1. 在对话历史第0位插入 system 消息，写一段你设计的提示词
# 2. 要求它具备至少3个你指定的特征（举例：说话直接、会怼你拖延、懂命理但仅供娱乐——你自己定）
# 3. 测试：问它几个能体现人设的问题，验证它真的"入戏"了
# 4. system prompt 单独放在一个变量里（方便以后改，不要写死在请求里）
#
# 【提示】
# - system 消息格式：{"role": "system", "content": "你的提示词"}
# - 好人设的写法：身份 + 性格 + 说话风格 + 禁止事项，四段式
# - 裁剪历史时注意保护第0位的 system（Day3的坑在这里回收）
# - 你day1.py练习1空着没写的那个"AI Python学习助手"system prompt，今天正好在这里补出来
#
# 【完成标志】
# 同一个问题，带人设和不带人设的AI回答风格明显不同
#
# 【最低消费】
# 只写一版 system prompt 并跑通一次对话
#
# ---------- 以下全部留白，自己写 ----------
print("AI助手启动，输入exit退出")
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

messages = [
    {
        "role": "system",
        "content": system_prompt
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
