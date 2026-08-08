# === 练习：requests发送GET请求 ===
#
# 目标：用requests库发送HTTP GET请求，获取并解析网页数据
#
# 要求：
# 1. 导入requests库
# 2. 向 http://httpbin.org/get 发送GET请求
#    提示：response = requests.get(url)
# 3. 打印响应状态码 response.status_code
# 4. 打印响应头中的 Content-Type
# 5. 将响应JSON数据解析为字典并打印
#    提示：response.json() 可以直接把JSON响应转成Python字典
# 6. 在请求中添加自定义参数：传 params={"name": "tuohai", "age": 20}
#    提示：requests.get(url, params=参数字典)
# 7. 观察返回的JSON中 args 字段的变化
#
# 提示：httpbin.org 是专门给开发者测试HTTP请求的网站，你发的参数它都会原样返回
