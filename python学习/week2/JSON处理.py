# === 练习：JSON数据处理 ===
#
# 目标：掌握JSON字符串与Python对象之间的转换
#
# 要求：
# 1. 导入json模块
# 2. 创建一个字典 student，包含字段：name、age、skills（列表）、address（嵌套字典，含city和street）
# 3. 将字典转为JSON字符串并打印
#    提示：json.dumps(data, ensure_ascii=False, indent=2)
#    ensure_ascii=False 让中文正常显示，indent=2 让输出格式化缩进
# 4. 将JSON字符串转回字典，修改age后再次转JSON
#    提示：json.loads(json字符串)
# 5. 将字典写入文件 student.json
#    提示：with open('student.json', 'w', encoding='utf-8') as f: json.dump(data, f, ...)
# 6. 从文件读取JSON并打印
#    提示：json.load(f) 注意是load不是loads
# 7. 删除 student.json 文件
#
# 提示：dumps/loads 处理字符串↔字典，dump/load 处理文件↔字典，带s的是字符串操作
