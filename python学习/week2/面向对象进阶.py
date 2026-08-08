# === 练习：面向对象进阶（继承与多态） ===
#
# 目标：掌握类的继承、方法重写和魔术方法
#
# 要求：
# 1. 创建基类 Animal：
#    - __init__(self, name, sound): 初始化名字和叫声
#    - speak(self): 打印 "xx发出了xx的声音"
#    - __str__(self): 返回 "Animal(名字=xx，叫声=xx)"
#    - __repr__(self): 返回和__str__一样的内容
# 2. 创建子类 Dog 继承 Animal：
#    - __init__(self, name, breed): 调用super().__init__()，sound固定传"汪汪"，额外保存breed品种
#    - fetch(self, item): 打印 "xx捡回了xx"
#    - 重写 __str__: 返回 "Dog(名字=xx，品种=xx)"
# 3. 创建子类 Cat 继承 Animal：
#    - __init__(self, name, indoor): 调用super().__init__()，sound固定传"喵喵"，额外保存indoor是否家猫
#    - purr(self): 打印 "xx发出了呼噜声"
#    - 重写 __str__: 返回 "Cat(名字=xx，家猫=xx)"
# 4. 创建一个Dog和一个Cat对象，测试所有方法
# 5. 创建列表 animals = [dog, cat]，遍历调用 speak()
#    观察多态效果：同样的 speak() 调用，不同对象表现不同
# 6. 打印 dog 和 cat 对象本身（测试 __str__）
#
# 提示：super().__init__() 调用父类构造方法；子类重写父类方法就是多态的体现
