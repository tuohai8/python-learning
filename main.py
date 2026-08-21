# main.py —— RAG知识库问答系统入口
#
# 功能：
# 1. 接收命令行参数
# 2. 加载PDF/TXT知识库
# 3. RAG检索相关资料
# 4. 调用ChatBot生成回答


import os
import argparse


from rag_core import RAGSystem
from chatbot import ChatBot





# ==========================
# 模块1：命令行参数
# ==========================


def parse_args():

    parser = argparse.ArgumentParser(

        description="RAG知识库问答系统"

    )


    parser.add_argument(

        "--file",

        required=True,

        help="知识库文件路径"

    )


    parser.add_argument(

        "--model",

        default="deepseek-chat",

        help="使用模型"

    )


    parser.add_argument(

        "--topk",

        type=int,

        default=3,

        help="检索文本数量"

    )


    return parser.parse_args()







# ==========================
# 模块2：生成Prompt
# ==========================


def build_prompt(

        question,

        context

):


    prompt = f"""

你是一个企业知识库助手。

请根据下面提供的文档内容回答用户问题。


【文档内容】

{context}


【用户问题】

{question}


回答要求：

1. 只能根据文档内容回答。

2. 如果文档没有相关信息，请明确告诉用户不知道。

3. 不允许编造不存在的信息。


"""


    return prompt







# ==========================
# 模块3：主程序
# ==========================


def main():


    # 获取命令行参数

    args = parse_args()





    # ----------------------
    # 检查文件
    # ----------------------


    if not os.path.exists(args.file):


        print(

            "错误：文件不存在"

        )

        return






    # ----------------------
    # 创建RAG系统
    # ----------------------


    rag = RAGSystem()



    try:


        print(

            "正在加载知识库..."

        )


        rag.load_document(

            args.file

        )


        print(

            "知识库加载完成"

        )



    except Exception as e:


        print(

            "知识库加载失败：",

            e

        )


        return






    # ----------------------
    # 创建ChatBot
    # ----------------------


    bot = ChatBot(

        model=args.model

    )



    print()

    print(

        "AI知识库助手启动"

    )


    print(

        "输入 exit 退出"

    )


    print(

        "输入 clear 清空聊天历史"

    )








    # ----------------------
    # 聊天循环
    # ----------------------


    while True:


        question = input(

            "\n你："

        )



        # 空输入

        if question.strip() == "":

            continue





        # 退出

        if question == "exit":

            print(

                "系统退出"

            )

            break






        # 清空历史

        if question == "clear":


            bot.clear_history()


            print(

                "聊天历史已清空"

            )


            continue







        try:


            # ------------------
            # RAG检索资料
            # ------------------


            context = rag.retrieve(

                question,

                args.topk

            )



            if not context:


                print(

                    "没有找到相关资料"

                )


                continue






            # ------------------
            # 拼接Prompt
            # ------------------


            prompt = build_prompt(

                question,

                context

            )






            # ------------------
            # 调用AI
            # ------------------

            answer = bot.chat(
                question,
                context
            )



            if answer is None:


                print(

                    "回答失败"

                )





        except Exception as e:


            print(

                "运行错误：",

                e

            )









# ==========================
# 程序入口
# ==========================


if __name__ == "__main__":


    main()