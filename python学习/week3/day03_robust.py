# Day 3（8.3）· 作品1第2.5步：健壮性——报错不崩，历史不爆炸
#
# 【目标】让昨天的多轮对话工具扛造：网络抽风不闪退，聊久了不把API撑爆
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
# 1. API调用包一层异常处理：网络超时/API报错时，打印友好提示，程序不退出，用户可以继续聊
# 2. 输入处理：空输入直接跳过；输入 quit/exit 才退出
# 3. 历史长度控制：只保留最近 N 轮对话（N自己定，比如10轮），最早的消息丢弃
#
# 【提示】
# - try / except 包住请求那几行；想想哪些异常该拦（连接错误？超时？返回非200？）
# - 你day1.py里 response.json() 后直接取 result["choices"]，API报错时这里会KeyError崩掉——今天先解决它
# - 历史裁剪用列表切片：messages = messages[-2*N:]（为什么是2*N不是N？自己想）
# - 注意：system prompt 如果被放在历史第0位，裁剪时别把"头"切掉了
#
# 【完成标志】
# 1. 乱填key或断网时程序不崩，提示后继续可用
# 2. 连聊20轮，历史始终控制在设定长度内
#
# 【最低消费】
# 只加 try/except，历史裁剪明天再做也行
#
# ---------- 以下全部留白，自己写 ----------
messages = [
    {
        "role": "system",
        "content": "你是一名python助手"
    }
]

username = None

N = 10   # 保存最近10轮对话


while True:

    question = input("你：")

    # 空输入跳过
    if question.strip() == "":
        continue

    # 退出
    if question in ["quit", "exit"]:
        break


    # 保存用户名（可选功能）
    if question.startswith("我叫"):
        username = question.replace("我叫", "")
        print("已保存用户名:", username)


    # 添加用户消息
    messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    try:
        response = requests.post(
            url,
            headers=headers,
            json={
                "model": "deepseek-chat",
                "messages": messages
            },
            timeout=30
        )


        # 非200状态直接报错
        response.raise_for_status()


        result = response.json()


        answer = result["choices"][0]["message"]["content"]


    except Exception as e:

        print("请求失败:", e)

        # 删除刚才加入的用户消息
        messages.pop()

        continue



    print("AI:", answer)


    # 保存AI回复
    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # 历史裁剪
    system_message = messages[0]

    history = messages[1:]

    messages = [
        system_message
    ] + history[-2 * N:]