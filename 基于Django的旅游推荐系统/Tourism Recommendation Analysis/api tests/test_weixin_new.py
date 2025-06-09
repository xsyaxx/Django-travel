import pytest
import logging

from commons.request_utils import RequestUtils
from commons.to_python import by_yaml
import json

g_var = {}
logger = logging.getLogger('ddt')  # 日志记录器

data_ddt_create_tag = by_yaml('data/ddt_create_tag.yaml')
logger.info(f'data_ddt_create_tag={data_ddt_create_tag}')

ddt_edit_fail_tag = by_yaml('data/ddt_edit_fail_tag.yaml')
logger.info(f'ddt_edit_fail_tag={ddt_edit_fail_tag}')


@pytest.fixture(scope='session')
def del_tags():
    yield
    # 所有用例之后执行

    print('所有用例都执行完毕，开始删除测试数据')

    resp = RequestUtils().send_request(method='get', url='https://api.weixin.qq.com/cgi-bin/tags/get')
    s = resp.text.replace("\\\\", "\\")
    resp_json = json.loads(s)  # 修改文本后，手动进行json反序列化
    tags = resp_json['tags']  # 获取所有的tag

    for tag_name in data_ddt_create_tag:  # 删除这几个标签
        tag_id = '000'
        for tag in tags:  # 根据tag_name 获取tag_id
            if tag['name'] == tag_name:
                tag_id = tag['id']

        if tag_id == '000':  # 没有找到tag_id
            continue

        RequestUtils().send_request(  # 不在乎是否成功
            method='POST',
            url='https://api.weixin.qq.com/cgi-bin/tags/delete',
            json={"tag": {"id": tag_id}}  # 根据tag_id 进行删除
        )


def test_get_token(del_tags):
    resp = RequestUtils().send_request(
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
    RequestUtils.pubilc_params['access_token'] = access_token


def test_get_tags():
    resp = RequestUtils().send_request(
        method='GET',
        url='https://api.weixin.qq.com/cgi-bin/tags/get',
    )

    assert resp.status_code == 200

    tags = resp.json()['tags']

    assert tags

    tag_id = tags[0]['id']

    assert tag_id == 2


@pytest.mark.parametrize(
    "name",
    data_ddt_create_tag
)
def test_create_tags(name, del_tags):
    resp = RequestUtils().send_request(
        method='POST',
        url='https://api.weixin.qq.com/cgi-bin/tags/create',
        json={"tag": {"name": name}}
    )

    assert resp.status_code == 200

    s = resp.text.replace("\\\\", "\\")
    resp_json = json.loads(s)  # 修改文本后，手动进行json反序列化

    tag = resp_json['tag']

    tag_id = tag['id']
    tag_name = tag['name']

    assert isinstance(tag_id, int)
    assert tag_name == name

    g_var['tag_id'] = tag_id
    g_var['tag_name'] = tag_name


def test_edit_tags():
    resp = RequestUtils().send_request(
        method='POST',
        url='https://api.weixin.qq.com/cgi-bin/tags/update',
        json={"tag": {"id": g_var['tag_id'], "name": g_var['tag_name'] + '0'}}
    )

    assert resp.status_code == 200

    errcode = resp.json()['errcode']
    errmsg = resp.json()['errmsg']

    assert errcode == 0
    assert errmsg == 'ok'


@pytest.mark.parametrize(
    "name,code",
    ddt_edit_fail_tag
)
def test_edit_fail_tag(name, code):
    resp = RequestUtils().send_request(
        method='POST',
        url='https://api.weixin.qq.com/cgi-bin/tags/update',
        json={"tag": {"id": g_var['tag_id'], "name": name}}  # 是已存在的标签
    )

    assert resp.status_code == 200

    errcode = resp.json()['errcode']

    assert errcode == code


def test_del_tags():
    resp = RequestUtils().send_request(
        method='POST',
        url='https://api.weixin.qq.com/cgi-bin/tags/delete',
        json={"tag": {"id": g_var['tag_id']}}
    )

    assert resp.status_code == 200

    errcode = resp.json()['errcode']
    errmsg = resp.json()['errmsg']

    assert errcode == 0
    assert errmsg == 'ok'


def test_upload_file():
    resp = RequestUtils().send_request(
        method='POST',
        url='https://api.weixin.qq.com/cgi-bin/media/uploadimg',
        files={
            # "media": open("data/baidu.png", "rb")  # 二进制模式打开
            "media": "data/baidu.png"  # 二进制模式打开
        }
    )

    assert resp.status_code == 200

    url = resp.json()['url']

    assert 'http' in url
    assert 'mmbiz.qpic.cn' in url
