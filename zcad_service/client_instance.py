import http.client
import json

import ahttp


class client_instance:

    def __init__(self, ip, port):
        self.__address = (ip, port)
        self.__wss_araray = []

    def query_delay_time_cmd(self, ip):
        if (self.__address):
            conn = http.client.HTTPConnection(self.__address[0], self.__address[1])
            payload = "{\r\n    \"ip\":\"124.70.219.89\"}"
            headers = {'Content-Type': 'application/json;charset=utf8'}
            url1 = "http://" + self.__address[0] + ":" + self.__address[1] + "/delaytime"
            conn.request("POST", "/delaytime", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
            conn.close()
            json_data = json.loads(data.decode("utf-8"))
            if ("content" in json_data and "status" in json_data):
                if (json_data["status"] == "200" and "time" in json_data["content"]):
                    return json_data["content"]["time"]
            return float('inf')

    def get_xfreecad_wss(self, usr_id, project_id):
        if (self.__address):
            conn = http.client.HTTPConnection(self.__address[0], self.__address[1])
            print("self.__address")
            print(self.__address)
            payload = json.dumps({"usrID": usr_id, "projectID": project_id})
            headers = {'Content-Type': 'application/json;charset=utf-8'}
            conn.request("POST", "/getwss", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
            conn.close()
            json_data = json.loads(data.decode("utf-8"))
            if ("content" in json_data and "status" in json_data):
                if (json_data["status"] == "200" and "wss" in json_data["content"]):
                    wss = json_data["content"]["wss"]
                    self.__wss_araray.append(wss)
                    return wss
            return ""

    def has_wss(self, wss):
        try:
            id = self.__wss_araray.index(wss)
            return id >= 0
        except ValueError:
            return False

    def close_xfreecad_wss(self, wss):
        if (self.__address and len(self.__address) > 0):
            conn = http.client.HTTPConnection(self.__address[0], self.__address[1])
            payload = json.dumps({"wss": wss})
            headers = {
                'Content-Type': 'application/json;charset=utf-8',
            }
            conn.request("POST", "/close", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
            conn.close()
            json_data = json.loads(data.decode("utf-8"))
            if ("content" in json_data and "status" in json_data):
                if (json_data["status"] == "200" and "state" in json_data["content"]):
                    state = json_data["content"]["state"]
                    print(state)
                    if (state == 1):
                        self.__wss_araray.remove(wss)
                        return 1
                    return 0
        return 0
