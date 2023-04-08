# 在阿里云服务器上部署flask应用
# 此段代码用于接收前端发送的json数据
# 此段代码在阿里云服务器中运行

from flask import Flask, jsonify, render_template, request
import json
from gevent import pywsgi

app = Flask(__name__)

data = []

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html") # 返回index.html页面

@app.route('/json', methods=['GET']) # 配置路由
def receive_data():
    global data
    data = request.get_json()
    return jsonify(data)

@app.route('/location', methods=['GET'])
def location_data():
    global data
    print(data)
    return jsonify(data)


if __name__ == "__main__":
    serve = pywsgi.WSGIServer(('0.0.0.0', 122), app) # 配置端口
    serve.serve_forever()
