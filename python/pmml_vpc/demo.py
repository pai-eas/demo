#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2


def demo():
    request_data = '[{"sex":0,"cp":0,"fbs":0,"thal":0,"age":0,"trestbps":0,"chol":0,"thalach":0,"oldpeak":0,"ca":0}]'

    # 该API需要上海vpc内访问
    url = 'http://pai-eas-internet.cn-shanghai.aliyuncs.com/api/predict/scorecard_pmml_example'

    req = urllib2.Request(url, data=request_data)
    # 若服务非public的，请将下行注释去掉，并填入正确的access_token
    req.add_header('Authorization', 'YWFlMDYyZDNmNTc3M2I3MzMwYmY0MmYwM2Y2MTYxMTY4NzBkNzdjOQ==')
    try:
        resp = urllib2.urlopen(req)
        content = resp.read()
        resp.close()
        print(content)
    except urllib2.HTTPError as e:
        print('Error Code: %s, Message: %s' % (e.code, e.read()))


if __name__ == '__main__':
    demo()
