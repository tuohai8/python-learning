# === 练习：requests发送POST请求 ===
#
# 目标：用requests发送POST请求，提交表单和JSON数据
#
# 要求：
# 1. 向 http://httpbin.org/post 发送POST请求，提交表单数据
#    提示：requests.post(url, data={"username": "admin", "password": "123456"})
# 2. 打印返回的JSON中 form 字段，观察你提交的数据
# 3. 向同一个URL发送JSON格式的数据
#    提示：requests.post(url, json={"name": "tuohai", "skill": "Python"})
# 4. 打印返回的JSON中 json 字段，对比和表单提交的区别
# 5. 添加自定义请求头：User-Agent 设为 "MyApp/1.0"
#    提示：requests.post(url, headers={"User-Agent": "MyApp/1.0"}, json=数据)
# 6. 打印返回的JSON中 headers 字段，确认User-Agent已生效
#
# 提示：data= 提交表单（Content-Type: application/x-www-form-urlencoded）
#       json= 提交JSON（Content-Type: application/json），两种方式后端接收方式不同
