# === 练习：面向对象基础 ===
#
# 目标：理解类、对象、属性和方法
#
# 要求：
# 1. 创建一个 Student 类，包含以下属性和方法：
#    - __init__(self, name, age, grade): 初始化姓名、年龄、成绩
#    - introduce(self): 打印自我介绍，格式 "我叫xx，今年xx岁"
#    - study(self, subject): 打印 "xx正在学习xx"
#    - get_grade_level(self): 根据grade返回等级
#      90及以上返回"优秀"，80-89返回"良好"，70-79返回"中等"，60-69返回"及格"，60以下返回"不及格"
# 2. 创建3个Student对象，分别传入不同的参数
# 3. 调用每个对象的 introduce() 和 study() 方法
# 4. 打印每个对象的成绩等级
#
# 提示：类用 class 类名: 定义，__init__ 是构造方法，self 代表对象自身
