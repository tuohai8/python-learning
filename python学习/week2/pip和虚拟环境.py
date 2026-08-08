# === 练习：pip安装和虚拟环境 ===
#
# 目标：掌握pip包管理器和venv虚拟环境
#
# 要求：
# 1. 在终端中执行以下操作（本文件只记录命令，不需要写Python代码）：
#    - 查看当前pip版本：pip --version
#    - 安装requests库：pip install requests
#    - 查看已安装的包：pip list
#    - 导出依赖列表：pip freeze > requirements.txt
# 2. 创建虚拟环境：
#    - python -m venv .venv
#    - 激活虚拟环境：.venv\Scripts\activate（Windows）
#    - 在虚拟环境中安装requests，观察和全局安装的区别
# 3. 思考题（写在注释里）：为什么项目要用虚拟环境而不是全局安装包？
#
# 提示：虚拟环境的好处是每个项目独立管理依赖，避免版本冲突
