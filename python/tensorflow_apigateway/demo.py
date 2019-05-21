#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from urlparse import urlparse
from com.aliyun.api.gateway.sdk import client
from com.aliyun.api.gateway.sdk.http import request
from com.aliyun.api.gateway.sdk.common import constant
from pai_tf_predict_proto import tf_predict_pb2


def predict(url, app_key, app_secret, request_data):
    cli = client.DefaultClient(app_key=app_key, app_secret=app_secret)
    body = request_data
    url_ele = urlparse(url)
    host = 'http://' + url_ele.hostname
    path = url_ele.path
    req_post = request.Request(host=host, protocol=constant.HTTP, url=path, method="POST", time_out=6000)
    req_post.set_body(body)
    req_post.set_content_type(constant.CONTENT_TYPE_STREAM)
    stat,header, content = cli.execute(req_post)
    return stat, dict(header) if header is not None else {}, content


def demo():
    # 以下三行的信息均可在EAS管控台的服务列表，点击服务名称查看
    app_key = ''
    app_secret = ''
    url = 'http://1c3b37ea83c047efa0dc6df0cacb70d3-cn-shanghai.alicloudapi.com/EAPI_249821151493486525_mnist_saved_model_example'

    # 请求数据可以参考阿里云EAS官方文档「通用processor服务请求数据构造」章节，根据自己的模型类型进行请求数据构造并序列化之后再进行请求
    request = tf_predict_pb2.PredictRequest()
    request.signature_name = 'predict_images'
    request.inputs['images'].dtype = tf_predict_pb2.DT_FLOAT  # 与模型中inputs.type对应
    request.inputs['images'].array_shape.dim.extend([1, 784])  # 与模型中inputs.shape对应
    request.inputs['images'].float_val.extend([0] * 784)  # data

    # 将pb序列化成string进行传输
    request_data = request.SerializeToString()

    stat, header, content = predict(url, app_key, app_secret, request_data)
    if stat != 200:
        print 'Http status code: ', stat
        print 'Error msg in header: ', header['x-ca-error-message'] if 'x-ca-error-message' in header else ''
        print 'Error msg in body: ', content
    else:
        response = tf_predict_pb2.PredictResponse()
        response.ParseFromString(content)
        print(response)


if __name__ == '__main__':
    demo()
