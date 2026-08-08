# Day 4（8.4）· 作品1第3步：流式输出——字一个个蹦出来
#
# 【目标】告别"转圈等待一整段"，让AI的回答像真人打字一样逐字出现
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
# 【需求】
# 1. API请求加上流式参数（DeepSeek/OpenAI都是 data里加 "stream": True）
# 2. 收到的是一块一块的增量内容（chunk），边收边打印，不换行
# 3. 打印完一整句后换行，程序逻辑其他部分不变
#
# 【提示】
# - 流式请求要用 requests.post(..., stream=True)，然后逐行读 response.iter_lines()
# - DeepSeek流式返回是SSE格式：每行以 "data: " 开头，结尾有 "data: [DONE]"
#   先 print 一下原始行看看长什么样，再决定怎么解析（每行是json字符串，取delta里的content）
# - 逐字打印不换行：print(text, end="", flush=True)
# - flush=True 是关键，没有它字会攒着不出来
#
# 【完成标志】
# AI回答时文字逐段蹦出，不用等全部生成完
#
# 【最低消费】
# 跑通流式请求并把原始行打印出来看看结构，就算数
#
# ---------- 以下全部留白，自己写 ----------
# 保存整个聊天历史
# API的messages参数需要这个格式：
# [{"role":"user","content":"问题"}, {"role":"assistant","content":"回答"}]
messages = [
    {
        "role": "system",
        "content": "你是一名python助手"
    }
]





# 最大保存10轮对话
# 一轮 = 用户消息 + AI消息
# 所以实际保存数量 = 10 * 2 = 20条
N = 10


# 无限循环，让程序持续聊天
while True:


    # 获取用户输入的问题
    question = input("你：")


    # 如果用户只输入空格或者什么都没输入
    # 直接跳过，不发送给AI
    if question.strip() == "":
        continue


    # 用户输入quit或者exit，结束程序
    if question in ["quit", "exit"]:
        break






    # 把用户的问题加入聊天历史
    # 这样下一次请求AI时，AI能看到之前的问题
    messages.append(
        {
            "role": "user",
            "content": question
        }
    )



    try:

        # 向大模型API发送请求
        # stream=True表示开启流式输出
        # AI生成一点就返回一点，不需要等待全部生成
        response = requests.post(
            url,
            headers=headers,
            json={
                "model": "deepseek-chat",
                "messages": messages,

                # 告诉API开启流式返回
                "stream": True
            },

            # requests开启流式接收
            stream=True,

            # 最多等待30秒，防止一直卡住
            timeout=30
        )



        # 检查HTTP状态
        # 例如401(API Key错误)、500(服务器错误)
        # 如果错误会直接进入except
        response.raise_for_status()



        # 保存AI完整回答
        # 因为流式是一小块一小块返回
        # 所以需要把每个chunk拼起来
        answer = ""



        # 一行一行读取服务器返回的数据
        # 每一行就是一个chunk
        for line in response.iter_lines():



            # requests返回的是bytes
            # 转换成普通字符串
            line = line.decode("utf-8")



            # 空行跳过
            if line == "":
                continue



            # AI生成结束标志
            # 收到后停止读取
            if line.strip() == "data: [DONE]":
                break



            # SSE格式前面有"data: "
            # 去掉它，只留下JSON内容
            if line.startswith("data: "):
                line = line[6:]



            # 把JSON字符串转换成Python字典
            data = json.loads(line)



            # 获取这一小块AI生成的文字
            #
            # 普通模式：
            # message.content
            #
            # 流式模式：
            # delta.content
            content = data["choices"][0]["delta"].get("content")



            # 如果这一块有文字
            if content:


                # 实时打印
                # end=""表示不换行
                # flush=True表示马上显示
                print(content, end="", flush=True)


                # 同时保存到完整答案里
                answer += content



    # 如果请求失败
    # 比如网络断开、API错误
    except Exception as e:


        # 打印错误原因
        print("请求失败:", e)



        # 删除刚才加入的问题
        # 因为AI没有成功回答
        # 不应该把这个问题留在历史里面
        messages.pop()


        # 回到下一轮聊天
        continue




    # 流式输出结束后换行
    print()



    # 把AI完整回答保存进历史
    # 下一轮聊天AI才能知道自己之前说过什么
    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )



    # -----------------------------
    # 历史长度控制
    # -----------------------------


    # 保存system提示词
    # 防止裁剪时把AI身份删除
    system_message = messages[0]



    # 去掉system，只留下聊天记录
    history = messages[1:]



    # 只保留最近10轮聊天
    # -2*N代表：
    # 一个用户消息 + 一个AI消息 = 一轮
    #
    # 10轮 = 20条消息
    messages = [
        system_message
    ] + history[-2 * N:]
