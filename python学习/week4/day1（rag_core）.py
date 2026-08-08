# ========== Week4 Day1 任务清单 ==========
# 日期：2026-08-08
# 进度：
#   chatbot.py ✅ 已封装完成（类、流式、多轮、异常、日志）
#   rag_core.py ❌ 未开始
#   main.py ❌ 未开始
# 今日目标：完成 rag_core.py，实现 RAGSystem 类


# ---------- 任务：新建 rag_core.py ----------
# 文件名：rag_core.py
# 类名：RAGSystem
# 依赖：pip install PyPDF2 scikit-learn requests

# 文件头注释：
# # rag_core.py —— 手写RAG向量检索模块
# # 用法：from rag_core import RAGSystem; rag = RAGSystem(); rag.load_document("xxx.pdf")
# # 依赖：pip install PyPDF2 scikit-learn requests


# 方法1：__init__(self)
#   初始化：self.chunks = []（存文本片段）、self.vectors = []（存向量）


# 方法2：_get_embedding(self, text: str) -> list
#   功能：调 DeepSeek Embedding API，把文本变成向量
#   API地址：https://api.deepseek.com/embeddings
#   请求头：复用 chatbot.py 里的 headers（Authorization Bearer + Content-Type）
#   请求体：{"model": "deepseek-embedding", "input": text}
#   返回：response.json()["data"][0]["embedding"]
#   异常：Timeout、ConnectionError 返回 None


# 方法3：load_document(self, file_path: str)
#   功能：读取文件 → 切文本 → 向量化 → 存到 self.chunks / self.vectors
#   步骤：
#   1. 判断后缀：.pdf 用 PyPDF2.PdfReader，.txt 用 open()
#   2. 提取全部文本（PDF逐页读，TXT一次性读）
#   3. 切文本：每500字一段，在句号/换行处切，不要切在词中间
#   4. 每段调 _get_embedding() 拿到向量
#   5. 存到 self.chunks（文本列表）和 self.vectors（向量列表）
#   6. print 进度：正在处理第X段/共Y段


# 方法4：retrieve(self, question: str, top_k: int = 3) -> str
#   功能：检索最相关的文本片段，拼接成字符串返回
#   步骤：
#   1. question 调 _get_embedding() 变成向量
#   2. 用 sklearn.metrics.pairwise.cosine_similarity 算相似度
#      注意：传入的矩阵形状要对，可能需要 reshape(1, -1)
#   3. 取相似度最高的 top_k 个索引（numpy.argsort 或手动排序）
#   4. 从 self.chunks 取对应文本，用 "\n\n---\n\n" 拼接
#   5. 返回拼接字符串


# ---------- 自测 ----------
# 写完后单独测试（不要等main.py）：
#
# from rag_core import RAGSystem
# rag = RAGSystem()
# rag.load_document("你的文档.pdf")          # 或 .txt
# context = rag.retrieve("年假有几天？", top_k=3)
# print(context)
#
# 通过标准：print 出的内容包含文档里关于年假的原文片段


# ---------- 晚上 ----------
# git push rag_core.py
# 截图：retrieve() 的返回结果 → 发项目群
# 睡前复盘三句话：今天跑通了什么？卡在哪？明天先攻哪？


# ========== 断点续传 ==========
# 如果 Embedding API 调不通：
#   检查 API key、模型名是不是 "deepseek-embedding"、请求格式
#   卡壳1小时先 Google/问GPT，再卡1小时才降级
#   降级：_get_embedding 返回假向量 [0.1]*100，让结构能跑通

# 如果 PyPDF2 装不上或读不了 PDF：
#   先用 .txt 文件测试，PDF 解析明天再补