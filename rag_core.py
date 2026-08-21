# rag_core.py —— RAG向量检索模块
#
# 功能：
# 1. 读取PDF/TXT
# 2. 文本切片
# 3. 文本向量化
# 4. 根据问题检索相关文本


import os
import PyPDF2


from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity





# ==========================
# RAG系统类
# ==========================


class RAGSystem:


    def __init__(self):

        """
        初始化RAG系统

        chunks:
        保存文本切片

        vectors:
        保存文本向量

        vectorizer:
        文本转向量工具
        """


        self.chunks = []


        self.vectors = []


        self.vectorizer = TfidfVectorizer()







    # ==========================
    # 加载文档
    # ==========================


    def load_document(

            self,

            file_path

    ):


        """
        加载PDF或者TXT文件


        流程：

        文件

        ↓

        文本

        ↓

        chunks切片

        ↓

        TF-IDF向量化

        ↓

        保存


        """



        # 防止重复加载

        self.chunks = []

        self.vectors = []





        text = ""





        # ==================
        # PDF读取
        # ==================


        if file_path.endswith(".pdf"):


            reader = PyPDF2.PdfReader(

                file_path

            )


            for page in reader.pages:


                page_text = page.extract_text()



                if page_text:


                    text += page_text






        # ==================
        # TXT读取
        # ==================


        elif file_path.endswith(".txt"):


            with open(

                file_path,

                "r",

                encoding="utf-8"

            ) as f:


                text = f.read()






        else:


            raise ValueError(

                "只支持PDF和TXT文件"

            )







        if not text.strip():


            raise ValueError(

                "文件没有读取到文本内容"

            )







        # ==================
        # 文本切片
        # ==================


        self.chunks = self._split_text(

            text

        )







        # ==================
        # 文本向量化
        # ==================


        self.vectors = self.vectorizer.fit_transform(

            self.chunks

        )




        print(

            f"加载完成，共{len(self.chunks)}个文本块"

        )









    # ==========================
    # 文本切片
    # ==========================


    def _split_text(

            self,

            text,

            size=500

    ):


        """
        长文本切成多个chunk

        """



        chunks = []



        for i in range(

                0,

                len(text),

                size

        ):


            chunks.append(

                text[i:i+size]

            )



        return chunks







    # ==========================
    # 检索
    # ==========================


    def retrieve(

            self,

            question,

            top_k=3

    ):


        """
        根据问题寻找相关文本


        流程：

        问题

        ↓

        转向量

        ↓

        相似度计算

        ↓

        返回最高的文本块

        """




        if not self.chunks:


            return ""







        # ==================
        # 问题向量化
        # ==================


        question_vector = self.vectorizer.transform(

            [question]

        )








        # ==================
        # 计算相似度
        # ==================


        scores = cosine_similarity(

            question_vector,

            self.vectors

        )[0]







        # ==================
        # 获取top_k
        # ==================


        indexes = scores.argsort()[

            -top_k:

        ][::-1]







        result = []



        for index in indexes:


            result.append(

                self.chunks[index]

            )







        return "\n\n".join(result)