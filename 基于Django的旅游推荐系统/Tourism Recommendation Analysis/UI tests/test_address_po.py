import pytest

from commons.list_page import UserAddressIndex, UserAddressSaveInfo

# 你这段代码是基于 pytest + Selenium + 页面对象模型（POM） 实现的收货地址模块的自动化测试脚本，共包含 4 个测试用例，
# 目标是完整覆盖用户在地址管理页的核心功能。
# 测试“收货地址管理”功能，包括新增、校验失败、编辑、删除。
@pytest.fixture
def get_user_address_index(user_driver):
    user_driver.get('http://101.34.221.219:8010/?s=useraddress/index.html')


def test_new_address(user_driver, del_all_address, get_user_address_index):
    page = UserAddressIndex(user_driver)
    page.new_address()  # 打开新的页面

    page = UserAddressSaveInfo(user_driver)  # 重新实例化PO
    msg = page.save("第一个地址", '北凡', '1311112222', 'XX胡同1号', '湖南省', '长沙市', '芙蓉区')

    assert msg == '操作成功'


def test_new_address_fail(user_driver, del_all_address, get_user_address_index):
    page = UserAddressIndex(user_driver)
    page.new_address()  # 打开新的页面

    page = UserAddressSaveInfo(user_driver)  # 重新实例化PO
    msg = page.save("第一个地址", '', '1', 'XX胡同1号', '湖南省', '长沙市', '芙蓉区')

    assert msg == '姓名格式 2~16 个字符之间'


def test_update_address(user_driver, del_all_address, get_user_address_index):
    page = UserAddressIndex(user_driver)
    page.edit_address()  # 打开新的页面

    page = UserAddressSaveInfo(user_driver)  # 重新实例化PO
    msg = page.save("第二个地址", '百里', '1911112222', 'XX胡同999号', '湖南省', '长沙市', '天心区')

    assert msg == '操作成功'


def test_del_address(user_driver, del_all_address, get_user_address_index):
    page = UserAddressIndex(user_driver)
    msg = page.del_address()  # 打开新的页面

    assert msg == '删除成功'
