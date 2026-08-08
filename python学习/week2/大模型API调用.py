# === 练习：调用大模型API ===
#
# 目标：用requests调用大语言模型API，实现文本生成
#
# 要求：
# 1. 导入requests和json
# 2. 定义函数 chat(prompt, model="deepseek-chat")：
#    - API地址：https://api.deepseek.com/chat/completions
#    - 请求头：Content-Type: application/json，Authorization: Bearer YOUR_API_KEY
#    - 请求体结构（字典）：
#      {
#          "model": model,
#          "messages": [{"role": "user", "content": prompt}],
#          "temperature": 0.7
#      }
#    - 发送POST请求，返回AI的回复文本
#    提示：response.json()["choices"][0]["message"]["content"]
# 3. 定义函数 chat_stream(prompt, model="deepseek-chat")：
#    - 和上面一样，但加上 "stream": True
#    - 用 for line in response.iter_lines() 逐行读取流式响应
#    - 每行以 "data: " 开头，去掉前缀后用json.loads解析
#    - 打印每个chunk的content字段（逐字输出效果）
#    提示：遇到 [DONE] 就停止
# 4. 测试非流式调用：问它 "用一句话解释什么是RAG"
# 5. 测试流式调用：问它 "写一首关于编程的四行诗"
#
# ⚠️ 注意：API_KEY 需要替换为你自己的密钥，不要硬编码在代码里
#    建议用环境变量：os.environ.get("DEEPSEEK_API_KEY")
#    设置环境变量：在终端执行 set DEEPSEEK_API_KEY=sk-xxx（Windows）
#
# 提示：DeepSeek API 兼容 OpenAI 格式，是练习大模型调用最经济的选择
