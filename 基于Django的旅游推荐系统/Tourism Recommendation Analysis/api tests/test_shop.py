from commons.request_utils import RequestUtils

# 这段代码是一套 商品收藏功能接口测试脚本，使用 pytest 编写，基于封装的 RequestUtils 工具类进行 接口调用与断言。
# 总体功能：
# 模拟用户登录后，测试 商品收藏流程 的完整接口逻辑，包括：
# 获取 token 登录
# 收藏商品
# 查询收藏列表是否存在该商品
# 取消收藏
# 再次查询确认已取消
def test_get_token():
    resp = RequestUtils().send_request(
        method="post",
        url="http://101.34.221.219:8010/api.php",
        params={
            "s": "user/login",
            "application": "app",
            "application_client_type": "ios",
        },
        json={
            "accounts": "beifan_1205",
            "pwd": "beifan_1205",
            "type": "username"
        }
    )

    code = resp.json()['code']
    token = resp.json()['data']['token']

    assert code == 0
    assert token != ""

    RequestUtils.pubilc_params['application'] = "app"
    RequestUtils.pubilc_params['application_client_type'] = "ios"
    RequestUtils.pubilc_params['token'] = token


def test_goods_favor():
    resp = RequestUtils().send_request(
        method="post",
        url="http://101.34.221.219:8010/api.php",
        params={
            "s": "goods/favor",
        },
        json={
            "id": 2,
            "is_mandatory_favor": 1
        }
    )

    code = resp.json()['code']
    msg = resp.json()['msg']

    assert code == 0
    assert msg == "收藏成功"


def test_usergoodsfavor_index_after_favor():
    resp = RequestUtils().send_request(
        method="post",
        url="http://101.34.221.219:8010/api.php",
        params={
            "s": "usergoodsfavor/index",
        },
    )

    code = resp.json()['code']
    text = resp.text

    assert code == 0
    assert '"goods_id":"2"' in text


def test_usergoodsfavor_cancel():
    resp = RequestUtils().send_request(
        method="post",
        url="http://101.34.221.219:8010/api.php",
        params={
            "s": "usergoodsfavor/cancel",
        },
        json={
            "id": "2"
        }
    )

    code = resp.json()['code']
    msg = resp.json()['msg']

    assert code == 0
    assert msg == '取消成功'


def test_usergoodsfavor_index_after_cancel():
    resp = RequestUtils().send_request(
        method="post",
        url="http://101.34.221.219:8010/api.php",
        params={
            "s": "usergoodsfavor/index",
        },
    )

    code = resp.json()['code']
    text = resp.text

    assert code == 0
    assert '"goods_id":"2"' not in text
