import time

import pytest

from commons import settings
from commons.kdt import Word
from commons.exchange import g_vars
# 这段代码是基于 pytest + Selenium + 封装库 Word（自定义封装的操作类） 的用户收货地址管理系统的自动化测试脚本，
# 主要功能是模拟用户在网页上新增、验证失败、修改、删除地址信息的全流程操作。

# 自动化测试用户收货地址模块的增删改查行为（CRUD），验证其功能是否符合预期。

@pytest.fixture
def get_user_address_index(user_driver):
    user_driver.get('http://101.34.221.219:8010/?s=useraddress/index.html')


def test_new_address(user_driver, del_all_address, get_user_address_index):
    wd = Word(user_driver)
    wd.click('/html/body/div[4]/div[3]/div/div[1]/button')
    wd.goto_iframe('//iframe[starts-with(@src,"http://101.34.221.219:8010/")]')
    wd.send_keys('/html/body/div[1]/form/div[1]/input', '我的地址')
    wd.send_keys('/html/body/div[1]/form/div[2]/input', '北凡')
    wd.send_keys('/html/body/div[1]/form/div[3]/input', '1311112222')
    wd.send_keys('//*[@id="form-address"]', 'XX胡同1号')
    wd.send_keys('/html/body/div[1]/form/div[1]/input', '我的地址')

    # 省份
    wd.click('/html/body/div[1]/form/div[4]/div[1]/a/span')
    wd.click('/html/body/div[1]/form/div[4]/div[1]/div/ul/li[text() = "湖南省"]')
    # 城市
    wd.click('/html/body/div[1]/form/div[4]/div[2]/a/span')
    wd.click('/html/body/div[1]/form/div[4]/div[2]/div/ul/li[text()="长沙市"]')
    # 区县
    wd.click('/html/body/div[1]/form/div[4]/div[3]/a/span')
    wd.click('/html/body/div[1]/form/div[4]/div[3]/div/ul/li[text()="芙蓉区"]')

    # 提交
    wd.click('/html/body/div[1]/form/div[7]/button')
    wd.save_text(settings.xpath_msg, 'msg')

    wd.assert_equal('${msg}', '操作成功')


def test_new_address_fail(user_driver, del_all_address, get_user_address_index):
    wd = Word(user_driver)
    wd.click('/html/body/div[4]/div[3]/div/div[1]/button')
    wd.goto_iframe('//iframe[starts-with(@src,"http://101.34.221.219:8010/")]')
    wd.send_keys('/html/body/div[1]/form/div[1]/input', '我的地址')
    wd.send_keys('/html/body/div[1]/form/div[2]/input', '')
    wd.send_keys('/html/body/div[1]/form/div[3]/input', '1311112222')
    wd.send_keys('//*[@id="form-address"]', 'XX胡同1号')
    # 省份
    wd.click('/html/body/div[1]/form/div[4]/div[1]/a/span')
    wd.click('/html/body/div[1]/form/div[4]/div[1]/div/ul/li[text() = "湖南省"]')
    # 城市
    wd.click('/html/body/div[1]/form/div[4]/div[2]/a/span')
    wd.click('/html/body/div[1]/form/div[4]/div[2]/div/ul/li[text()="长沙市"]')
    # 区县
    wd.click('/html/body/div[1]/form/div[4]/div[3]/a/span')
    wd.click('/html/body/div[1]/form/div[4]/div[3]/div/ul/li[text()="芙蓉区"]')

    # 提交
    wd.click('/html/body/div[1]/form/div[7]/button')
    wd.click('/html/body/div[1]/form/div[7]/button')
    wd.save_text(settings.xpath_msg, 'msg')

    wd.assert_equal('${msg}', '姓名格式 2~16 个字符之间')


def test_update_address(user_driver, del_all_address, get_user_address_index):
    wd = Word(user_driver)
    wd.click('//a[text()=" 编辑"]')
    wd.goto_iframe('//iframe[starts-with(@src,"http://101.34.221.219:8010/")]')

    wd.clear('/html/body/div[1]/form/div[1]/input')
    wd.send_keys('/html/body/div[1]/form/div[1]/input', '第二个地址')

    wd.clear('/html/body/div[1]/form/div[2]/input')
    wd.send_keys('/html/body/div[1]/form/div[2]/input', '百里')

    wd.clear('/html/body/div[1]/form/div[3]/input')
    wd.send_keys('/html/body/div[1]/form/div[3]/input', '1911112222')

    wd.clear('//*[@id="form-address"]')
    wd.send_keys('//*[@id="form-address"]', 'XX胡同1号')

    # 省份
    wd.click('/html/body/div[1]/form/div[4]/div[1]/a/span')
    wd.click('/html/body/div[1]/form/div[4]/div[1]/div/ul/li[text() = "湖南省"]')
    # 城市
    wd.click('/html/body/div[1]/form/div[4]/div[2]/a/span')
    wd.click('/html/body/div[1]/form/div[4]/div[2]/div/ul/li[text()="长沙市"]')
    # 区县
    wd.click('/html/body/div[1]/form/div[4]/div[3]/a/span')
    wd.click('/html/body/div[1]/form/div[4]/div[3]/div/ul/li[text()="天心区"]')

    # 等待5秒
    wd.sleep(5)
    # 提交
    wd.click('/html/body/div[1]/form/div[7]/button')
    wd.save_text(settings.xpath_msg, 'msg')

    wd.assert_equal('${msg}', '操作成功')


def test_del_address(user_driver, del_all_address, get_user_address_index):
    wd = Word(user_driver)
    wd.click('//a[text()=" 删除"]')
    wd.confirm()
    wd.save_text(settings.xpath_msg, 'msg')
    wd.assert_equal('${msg}', '删除成功')
