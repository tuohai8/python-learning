# === 练习：多轮对话聊天机器人 ===
#
# 目标：基于大模型API实现一个支持上下文记忆的命令行聊天机器人
#
# 要求：
# 1. 维护一个消息列表 messages，初始时加入系统提示词：
#    {"role": "system", "content": "你是一个友好的AI助手，回答简洁有趣"}
# 2. 用 while True 循环实现持续对话：
#    - 获取用户输入，如果输入 "quit" 或 "exit" 则退出
#    - 将用户消息追加到 messages 列表（role="user"）
#    - 调用API，把整个 messages 列表作为请求体发送
#      提示：这样AI就能看到之前所有的对话内容
#    - 将AI的回复也追加到 messages 列表（role="assistant"）
#    - 打印AI的回复
# 3. 添加异常处理：
#    - 网络超时提示 "网络不给力，请重试"
#    - API返回错误时打印具体的错误信息
#    提示：try/except 包住 requests.post，捕获 requests.exceptions.Timeout 等
# 4. 额外功能（选做）：
#    - 输入 "clear" 清空对话历史（重新开始）
#    - 每次回复后显示当前对话轮数
#
# 提示：多轮对话的关键是每次请求都把完整的 messages 列表发过去
#       AI本身没有记忆，靠你传的messages列表"回忆"之前的对话
