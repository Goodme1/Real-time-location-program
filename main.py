# 从STM32获取GPS数据中的经纬度信息并发送到阿里云服务器
# 此段代码在本地运行，从串口读取数据并解码，将解析后的GPS数据存储在gps_data中，然后发送GET请求并获取响应
# 2023.3.12
# by jinyb

import serial
import json
import requests
import pynmea2

# 串口的设备名称和波特率
ser_1 = serial.Serial('COM21', 9600, timeout=0.2)
ser = serial.Serial('COM18', 115200, timeout=0.2)

url = 'http://120.55.93.225:122/json'   # http://120.55.93.225:122为阿里云服务器的URL，配置为json路由

while True:
    data = ser.readline().decode('utf-8', 'ignore')   # 从串口读取数据并解码
    data = data[data.find('$'):]     # 去掉有效数据前的乱码
    print(data)
    if data.startswith('$GPRMC'):   # 只处理RMC语句，该语句包含了GPS的定位信息

        record = pynmea2.parse(data)
        # gps_data = data.split(',')   # 将语句按逗号分隔
        # # 对GPS数据进行解析
        # latitude = float(gps_data[3][0:2]) + float(gps_data[3][2:])/60.0   # 纬度
        # longitude = float(gps_data[5][0:3]) + float(gps_data[5][3:])/60.0   # 经度
        # 将解析后的GPS数据存储在gps_data中
        gps_data = {
                  "latitude": record.latitude,
                  "longitude": record.longitude,
              }
        response = requests.get(url, json=gps_data)   # 发送GET请求并获取响应
        if response.status_code == 200:
            print("Request successful")
        else:
            print("Request failed with status code:", response.status_code)


# import requests
# import json
# # 以下为测试过程代码
#
# # 准备数据
# data = {
#     "latitude": 34.03232366666667,
#     "longitude": 108.76100783333334,
# }
#
# # 发送GET请求
# url = "http://120.55.93.225:122/json"   # 配置路由
#
# response = requests.get(url, json=data)
#
# if response.status_code == 200:
#     print("Request successful")
# else:
#     print("Request failed with status code:", response.status_code)
#

