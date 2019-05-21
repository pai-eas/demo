#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from urlparse import urlparse
from com.aliyun.api.gateway.sdk import client
from com.aliyun.api.gateway.sdk.http import request
from com.aliyun.api.gateway.sdk.common import constant


def predict(url, app_key, app_secret, request_data):
    cli = client.DefaultClient(app_key=app_key, app_secret=app_secret)
    body = request_data
    url_ele = urlparse(url)
    host = 'http://' + url_ele.hostname
    path = url_ele.path
    req_post = request.Request(host=host, protocol=constant.HTTP, url=path, method="POST", time_out=6000)
    req_post.set_body(bytearray(source=body, encoding="utf8"))
    req_post.set_content_type(constant.CONTENT_TYPE_STREAM)
    stat,header, content = cli.execute(req_post)
    return stat, dict(header) if header is not None else {}, content


def demo():
    # 以下三行的信息均可在EAS管控台的服务列表，点击服务名称查看
    app_key = ''
    app_secret = ''
    url = 'http://1c3b37ea83c047efa0dc6df0cacb70d3-cn-shanghai.alicloudapi.com/EAPI_249821151493486525_scorecard_pmml_example'
    # 请求数据可以参考阿里云EAS官方文档「通用processor服务请求数据构造」章节，根据自己的模型类型进行请求数据构造并序列化之后再进行请求
    request_data = '[{"sex":0,"cp":0,"fbs":0,"restecg":0,"exang":0,"slop":0,"thal":0,"age":0,"trestbps":0,"chol":0,"thalach":0,"oldpeak":0,"ca":0}]'

    stat, header, content = predict( url, app_key, app_secret, request_data)
    if stat != 200:
        print 'Http status code: ', stat
        print 'Error msg in header: ', header['x-ca-error-message'] if 'x-ca-error-message' in header else ''
        print 'Error msg in body: ', content
    else:
        print content

if __name__ == '__main__':
    demo()
