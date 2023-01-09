import socket
import time
import json
import traceback
import parm_process
from base_define import command_type, instance_status
import base_define
import os
from free_cad_instance import free_cad_instance
from ping3 import ping
import http.client


class xfreecad_manager:

    def __init__(self):
        self.__port_instance = {}
        self.__last_instance = 0
        self._instance = []
        self.__cmd = ""
        self.__work_folder = ""
        self.__servicesDic = []
        self.__init_by_config()

    def process_messgae():
        pass

    def regist_client(self, ip, port):
        for item in self.__servicesDic:
            conn = http.client.HTTPConnection(item[0], item[1])
            payload = json.dumps({"ip": ip, "port": port})
            headers = {
                'Content-Type': 'application/json',
            }
            res = conn.request("POST", "/register", payload, headers)
            conn.close()
            print(res)

    def new_instance(self, port_id, project_id):
        for key, value in self.__port_instance.items():
            if value.get_status() == instance_status.PENGING or value.get_status() == instance_status.CLOSED:
                curdir = os.path.dirname(__file__)
                current_datetime = time.strftime('%Y-%m-%d-%H-%M-%S')
                # convert datetime obj to string
                str_current_datetime = str(current_datetime)
                file_name = "freecad" + key + "_" + str_current_datetime + ".txt"
                pixyzProcessLog = os.path.join(curdir, "log", file_name)
                value.start_instance(self.__cmd, self.__work_folder, pixyzProcessLog, self.__freecad_closed)
                return value.get_wss()
        return ""

    def __freecad_closed(self, wss):
        print(wss)

    def __init_by_config(self):
        cur_path = os.path.dirname(__file__)
        config_json = os.path.join(cur_path, "config.json")
        with open(config_json, 'r', encoding='utf-8') as f:
            sl = json.load(f)
            self.__cmd = sl["instance_exe"]
            self.__work_folder = sl["instance_work_folder"]
            client_array = sl["service_config"]
            for key in client_array:
                print(key["IP"] + ":" + str(key["Port"]))
                self.__servicesDic.append((key["IP"], key["Port"]))

            ports = sl["ports"]
            for key, value in ports.items():
                self.__port_instance[key] = free_cad_instance(key, value)
            self.__last_instance = len(self.__port_instance)

    def get_latency(self, ip):
        if (self.__last_instance <= 0):
            return float('inf')  # 如果当前没有可用实例端口，返回最大事件，标识此路径不可达
        try:
            result = ping(ip)
            return result
        except Exception as e:
            print(e.args())
            return float('inf')

    def close_instance(self, wss):
        for key, value in self.__port_instance.items():
            if (value.get_wss() == wss):
                return value.close_instance()
        return 0
