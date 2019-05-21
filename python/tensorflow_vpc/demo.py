#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from pai_tf_predict_proto import tf_predict_pb2


def demo():
    # 以下三行的信息均可在EAS管控台的服务列表，点击服务名称查看
    url = 'http://pai-eas-internet.cn-shanghai.aliyuncs.com/api/predict/mnist_saved_model_example'

    # 请求数据可以参考阿里云EAS官方文档「通用processor服务请求数据构造」章节，根据自己的模型类型进行请求数据构造并序列化之后再进行请求
    request = tf_predict_pb2.PredictRequest()
    request.signature_name = 'predict_images'
    request.inputs['images'].dtype = tf_predict_pb2.DT_FLOAT  # 与模型中inputs.type对应
    request.inputs['images'].array_shape.dim.extend([1, 784])  # 与模型中inputs.shape对应
    request.inputs['images'].float_val.extend([0] * 784)  # data

    # 将pb序列化成string进行传输
    request_data = request.SerializeToString()

    req = urllib2.Request(url, data=request_data)
    # 若服务非public的，请将下行注释去掉，并填入正确的access_token
    req.add_header('Authorization', 'YTg2ZjE0ZjM4ZmE3OTc0NzYxZDMyNmYzMTJjZTQ1YmU0N2FjMTAyMA==')
    try:
        resp = urllib2.urlopen(req)
        content = resp.read()
        resp.close()
        response = tf_predict_pb2.PredictResponse()
        response.ParseFromString(content)
        print(response)
    except urllib2.HTTPError as e:
        print('Error Code: %s, Message: %s' % (e.code, e.read()))


if __name__ == '__main__':
    demo()
