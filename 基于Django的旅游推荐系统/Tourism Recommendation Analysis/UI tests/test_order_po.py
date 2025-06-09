import time

import pytest
from commons.list_page import *
import datetime

# 这段代码是使用 pytest + Selenium + 页面对象模型（POM） 实现的一个完整自动化测试用例，测试的是：用户购买商品的整个流程，包括：
# 功能概述：添加地址 + 加入购物车 + 下单 + 取消订单 + 删除订单
@pytest.fixture
def add_address(user_driver):
    user_driver.get('http://101.34.221.219:8010/?s=useraddress/index.html')
    page = UserAddressIndex(user_driver)
    page.new_address()  # 打开新的页面

    page = UserAddressSaveInfo(user_driver)  # 重新实例化PO
    msg = page.save("第一个地址", '北凡', '1311112222', 'XX胡同1号', '湖南省', '长沙市', '芙蓉区')

    assert msg == '操作成功'

    yield


def test_add_cart_and_buy(user_driver, add_address, del_all_address):
    user_driver.get('http://101.34.221.219:8010/?s=goods/index/id/5.html')

    page = GoodsIndex(user_driver)
    msg = page.add_car()

    assert msg == '加入成功'

    user_driver.get('http://101.34.221.219:8010/?s=cart/index.html')
    page = CartIndex(user_driver)
    page.select_all()
    page.buy()

    url = user_driver.current_url
    assert url != 'http://101.34.221.219:8010/?s=cart/index.html'

    page = BuyIndex(user_driver)
    msg = page.buy_order()

    assert msg == '操作成功'

    page = OrderIndex(user_driver)

    today = datetime.datetime.now().strftime("%Y%m%d")
    assert page.get_order_no("1").startswith(today)

    name = 'Meizu/魅族 MX4 Pro移动版 八核大屏智能手机 黑色 16G'
    assert page.get_goods_name("1") == name

    amount = 2499.00
    assert page.get_order_amount("1") == amount

    msg = page.cancel("1")

    assert msg == '取消成功'

    # time.sleep(4) # 取消和删除之间，需等待
    msg = page.delete("1")

    assert msg == '删除成功'
