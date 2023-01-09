import ahttp
import json

# payload = "{\r\n    \"ip\":\"121.36.240.202\"}"
# payload2 = "{\r\n    \"ip\":\"124.70.219.89\"}"
# headers = {'Content-Type': 'application/json;charset=utf8'}
# url1 = "http://localhost:8878/delaytime"
# tasks = [ahttp.post(url1, data=payload, headers=headers)]
# results = ahttp.run(tasks)
# for item in results:
#     result = item.content
#     result = result.decode("utf-8")
#     result = json.loads(result)
#     print(result["content"]["time"])
import time
from scapy.all import *

# 发送数据包并记录发送时间
send_time = time.time()
response = sr1(IP(dst="52.83.224.250") / ICMP())
send_time = time.time()