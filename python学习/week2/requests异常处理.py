# === 练习：requests异常处理 ===
#
# 目标：掌握网络请求中的异常处理和重试机制
#
# 要求：
# 1. 导入requests和相关异常类：
#    from requests.exceptions import Timeout, ConnectionError, HTTPError
# 2. 定义函数 safe_get(url, max_retries=3, timeout=5):
#    - 用 for 循环尝试 max_retries 次
#    - 每次用 try/except 捕获以下异常并打印友好提示：
#      Timeout：提示 "请求超时，第x次重试..."
#      ConnectionError：提示 "网络连接失败，请检查网络"
#      HTTPError：提示 "服务器返回错误状态码：xx"
#    - 每次请求设置 timeout 参数
#    - 全部重试失败后返回 None
#    - 成功则返回 response
# 3. 测试你的函数：
#    - 请求 http://httpbin.org/delay/3 （正常，延迟3秒返回）
#    - 请求 http://httpbin.org/delay/10 （设timeout=3，会触发超时）
#    - 请求 http://httpbin.org/status/404 （会返回404状态码）
#      提示：response.raise_for_status() 可以在状态码非200时抛出HTTPError
#
# 提示：实际项目中网络请求一定要做异常处理和超时设置，不能裸奔
