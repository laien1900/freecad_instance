# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/10/12 11:11
# @author   :Mo
# @function :service of flask

# flask
from flask import Flask, request, jsonify
from xfreecad_manager import xfreecad_manager

app = Flask(__name__)


@app.route('/getwss', methods=["POST"])
def get_instance():
    params = request.form if request.form else request.json
    print(params)
    a = params.get("useID", 0)
    b = params.get("projectID", 0)
    wss = new_instance(a, b)
    res = {"wss": wss}
    print(res)
    result = jsonify(content_type='application/json;charset=utf-8', reason='success', charset='utf-8', status='200', content=res)
    print(result)
    return result


@app.route('/close', methods=["POST"])
def close_instance():
    params = request.form if request.form else request.json
    print(params)
    a = params.get("wss", 0)
    result = close_instance(a)
    res = {"state": result}
    return jsonify(content_type='application/json;charset=utf-8', reason='success', charset='utf-8', status='200', content=res)


@app.route('/delaytime', methods=["POST"])
def get_delay_time():
    params = request.form if request.form else request.json
    print(params)
    a = params.get("ip", 0)
    result = g_xfreecad_manager.get_latency(a)
    res = {"time": result}
    return jsonify(content_type='application/json;charset=utf-8', reason='success', charset='utf-8', status='200', content=res)


def new_instance(use_id, project_id):
    if g_xfreecad_manager is not None:
        return g_xfreecad_manager.new_instance(use_id, project_id)
    return "fault"


def close_instance(wss):
    if g_xfreecad_manager is not None:
        return g_xfreecad_manager.close_instance(wss)
    return 0


if __name__ == '__main__':
    global g_xfreecad_manager
    g_xfreecad_manager = xfreecad_manager()
    g_xfreecad_manager.regist_client('127.0.0.1', '8878')
    app.run(port=8878)
