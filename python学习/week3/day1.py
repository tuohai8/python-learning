# ============================================================
# Week3 Day1 · Prompt工程基础 练习
# 今日验收：能传system的ask_ai() + prompt对比观察笔记
# ============================================================
import os
import requests


url = "https://api.deepseek.com/chat/completions"


API_KEY = os.environ.get("DEEPSEEK_API_KEY")


if not API_KEY:
    raise ValueError("没有找到 DEEPSEEK_API_KEY")


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"}

# ------------------------------------------------------------
# 练习1：Role设计（不写代码，把结果写在注释里）
# ------------------------------------------------------------
# 任务：为你的"AI Python学习助手"设计一段system prompt
# 要求：包含五要素（角色/任务/背景/限制/输出格式），3-6行
# 让GPT给你打分并指出最弱的一条，改到8分以上
# 最终版本写在这下面几行注释里：
#
# 【我的system prompt】





# ------------------------------------------------------------
# 练习2：升级 ask_ai() —— 今天核心任务（60分钟）
# ------------------------------------------------------------
# 任务：把Week2的ask_ai()升级，支持system参数
# 要求：
#   1. 函数能接受第二个参数 system，且有默认值（不传也能用）
#   2. 发给API的messages里要包含 system 和 user 两条消息
#   3. 进阶：支持多轮对话（把历史消息一起传进去）
# 卡住超1小时：降级为单轮对话，先跑通再说
#
# 【在下面写你的代码】
def ask_ai(question, system="你是一名AI助手"):
    messages = [
        {
            "role": "system",
            "content": system
        },
        {
            "role": "user",
            "content": question
        }
    ]

    data = {
        "model": "deepseek-chat",
        "messages": messages
    }

    response = requests.post(
        url,
        headers=headers,
        json=data

    )

    result = response.json()

    return result["choices"][0]["message"]["content"]
print(
    ask_ai(
        "什么是RAG？",
        "你是一名Python老师，面向零基础学生解释"
    )
)





# ------------------------------------------------------------
# 练习3：Prompt对比实验（30分钟）
# ------------------------------------------------------------
# 任务：同一个问题"解释什么是RAG？"，用4种prompt各问一次：
#   第1种：裸问（不带system）
#   第2种：只有角色
#   第3种：角色 + 限制（300字以内 + 举一个生活例子）
#   第4种：角色 + 限制 + 输出格式（先定义、再举例、最后一句话总结）
# 要求：把4个回答保存到 rag_prompt_test.txt 文件里
#
# 【在下面写你的代码】明白了原理。主要由角色和限制影响回答的质量和要求


# ------------------------------------------------------------
# 练习3收尾：观察笔记（今天最重要的产出）
# ------------------------------------------------------------
# 写在txt文件末尾，或写在这里：
# 1. 第几个回答最有用？为什么？
#    答：这个是看需要的，我想要符合我要求的回答，就给身份和限制就可以了
# 2. 哪个要素影响最大（角色/限制/输出格式）？
#    答：角色影响最大
# 3. 有没有哪个回答出乎你意料？
#    答：没


# ------------------------------------------------------------
# 练习4（可选）：为Week4的RAG系统提前写system prompt
# ------------------------------------------------------------
# 角色：企业文档问答助手
# 必须包含一条限制："只能根据提供的资料回答，不知道就说不知道"
# 写好存着，Week4直接用
#
# 【我的RAG system prompt草稿】
def ask_ai(question, system="你是一名企业文档问答助手"):
    messages = [
        {
            "role": "system",
            "content": system
        },
        {
            "role": "user",
            "content": question
        }
    ]

    data = {
        "model": "deepseek-chat",
        "messages": messages
    }

    response = requests.post(
        url,
        headers=headers,
        json=data

    )

    result = response.json()

    return result["choices"][0]["message"]["content"]
print(
    ask_ai(
        "什么是RAG？",
        "你是一名企业文档问答助手，只能根据提供资料回答  不知道就说不知道"
    )
)



# ------------------------------------------------------------
# 最后测试：跑通后应看到三种截然不同的回答风格
# ------------------------------------------------------------
# 用同一个问题"什么是列表？"分别测：
#   1. 不传system
#   2. system = 你是一名Python老师，面向零基础，必须带代码例子。
#   3. system = 你是一名毒舌面试官，用最简短的话回答。
# 三个回答风格差异明显 = 今天任务完成