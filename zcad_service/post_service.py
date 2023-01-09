# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/10/12 11:11
# @author   :Mo
# @function :service of flask

# flask
import asyncio
import threading
from flask import Flask, request, jsonify

import json
import http.client

app = Flask(__name__)

service_instance = {}
from client_instance import client_instance


@app.route('/getwss', methods=["POST"])
def get_instance():
    params = request.form if request.form else request.json
    print(params)
    a = params.get("ip", 0)
    b = params.get("useID", 0)
    c = params.get("projectID", 0)
    wss = new_instance(a, b, c)
    status = '200'
    reason = 'success'
    if (wss == None or len(wss) == 0):
        status = '300'
        reason = 'create failed'
    res = {"wss": wss}
    return jsonify(content_type='application/json;charset=utf-8', reason=reason, charset='utf-8', status=status, content=res)


@app.route('/close', methods=["POST"])
def close_instance():
    params = request.form if request.form else request.json
    print(params)
    a = params.get("wss", 0)
    result = close_instance(a)
    res = {"state": result}
    return jsonify(content_type='application/json;charset=utf-8', reason='success', charset='utf-8', status='200', content=res)


@app.route('/register', methods=["POST"])
def register_service():
    params = request.form if request.form else request.json
    print(params)
    b = params.get("port", 0)
    a = params.get("ip", 0)

    result = "successed"
    state = '200'
    key = a + b
    if key in service_instance:
        result = "service exist"
        state = 300
    else:
        service_instance[key] = client_instance(a, b)
        print(key)
    res = {"status": result}
    return jsonify(content_type='application/json;charset=utf-8', reason='success', charset='utf-8', status=state, content=res)


def get_delay_time(service, time, ip):
    time = service.query_delay_time_cmd(ip)


def new_instance(ip, use_id, project_id):
    tasks = []
    clien_instance = []
    for key, value in service_instance.items():
        clien_instance.append(value)
    thread_array = []
    time_array = [0.0 for i in range(len(clien_instance))]
    for index, item in enumerate(clien_instance):
        t = threading.Thread(target=get_delay_time, args=(item, time_array[index], ip))
        t.start()
        thread_array.append(t)
    for item in thread_array:
        item.join()
    print(time_array)
    cur_index = -1
    if len(time_array) > 0:
        cur_index = time_array.index(min(time_array))
    if (cur_index == -1):
        return None
    return clien_instance[cur_index].get_xfreecad_wss(use_id, project_id)


def close_instance(wss):
    for key, value in service_instance.items():
        if (value.has_wss(wss)):
            return value.close_xfreecad_wss(wss)
    return 0


import socket
if __name__ == '__main__':
    app.run(port=8868)
