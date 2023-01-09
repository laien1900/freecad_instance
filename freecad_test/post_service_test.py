import requests
import json
import http.client

conn = http.client.HTTPConnection("127.0.0.1", 8878)
payload = "{\r\n    \"ip\":\"121.36.240.202\",\r\n    \"useID\":\"1\",\r\n    \"projectID\":\"2\"\r\n}"
headers = {'Content-Type': 'application/json;charset=utf8'}
conn.request("POST", "/getwss", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))