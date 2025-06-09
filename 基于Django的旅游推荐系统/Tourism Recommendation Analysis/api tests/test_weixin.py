import requests

import json

g_var = {}


def test_get_token():
    resp = requests.request(
        method='GET',
        url='https://api.weixin.qq.com/cgi-bin/token',
        params={
            "grant_type": "client_credential",
            "appid": "wxc000c173bbf436ba",
            "secret": "d64530af286c88f67eef268bda2642aa"
        }
    )

    assert resp.status_code == 200

    access_token = resp.json()['access_token']

    assert access_token != ""

    g_var['access_token'] = access_token  # 保存变量，为了其他接口使用


def test_get_tags():
    resp = requests.request(
        method='GET',
        url='https://api.weixin.qq.com/cgi-bin/tags/get',
        params={
            "access_token": g_var['access_token'],  # 读取变量
        }
    )

    assert resp.status_code == 200

    tags = resp.json()['tags']

    assert tags

    tag_id = tags[0]['id']

    assert tag_id == 2


def test_create_tags():
    resp = requests.request(
        method='POST',
        url='https://api.weixin.qq.com/cgi-bin/tags/create',
        params={
            "access_token": g_var['access_token'],  # 读取变量
        },
        json={"tag": {"name": "广西4"}}
    )

    assert resp.status_code == 200

    s = resp.text.replace("\\\\", "\\")
    resp_json = json.loads(s)  # 修改文本后，手动进行json反序列化

    tag = resp_json['tag']

    tag_id = tag['id']
    tag_name = tag['name']

    assert isinstance(tag_id, int)
    assert tag_name == '广西4'

    g_var['tag_id'] = tag_id
    g_var['tag_name'] = tag_name


def test_edit_tags():
    resp = requests.request(
        method='POST',
        url='https://api.weixin.qq.com/cgi-bin/tags/update',
        params={
            "access_token": g_var['access_token'],  # 读取变量
        },
        json={"tag": {"id": g_var['tag_id'], "name": g_var['tag_name'] + '0'}}
    )

    assert resp.status_code == 200

    errcode = resp.json()['errcode']
    errmsg = resp.json()['errmsg']

    assert errcode == 0
    assert errmsg == 'ok'


def test_del_tags():
    resp = requests.request(
        method='POST',
        url='https://api.weixin.qq.com/cgi-bin/tags/delete',
        params={
            "access_token": g_var['access_token'],  # 读取变量
        },
        json={"tag": {"id": g_var['tag_id']}}
    )

    assert resp.status_code == 200

    errcode = resp.json()['errcode']
    errmsg = resp.json()['errmsg']

    assert errcode == 0
    assert errmsg == 'ok'


def test_upload_file():
    resp = requests.request(
        method='POST',
        url='https://api.weixin.qq.com/cgi-bin/media/uploadimg',
        params={
            "access_token": g_var['access_token'],  # 读取变量
        },
        files={
            "media": open("data/baidu.png", "rb")  # 二进制模式打开
            # "media": "data/baidu.png"  # 二进制模式打开
        }
    )

    assert resp.status_code == 200

    url = resp.json()['url']

    assert 'http' in url
    assert 'mmbiz.qpic.cn' in url
