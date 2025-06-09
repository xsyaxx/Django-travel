import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from commons.driver_utils import get_webdriver
from commons.user_action import login, logout
from commons.address_action import del_all
# 这段代码的功能是为自动化测试框架（基于 pytest + Selenium）提供统一的测试前置/后置环境配置，主要包含：
# 创建并管理浏览器驱动，并在测试执行前后完成登录、登出、清除地址等准备/清理工作。

@pytest.fixture(scope='session')
def user_driver():
    """返回已登录的浏览器"""
    driver = get_webdriver()  # 启动浏览器
    driver.implicitly_wait(3)
    driver.wait = WebDriverWait(driver, 10)   # 显示等待
    # driver.implicitly_wait(10)

    login(driver)  # 登录账号

    yield driver  # 返回浏览器

    logout(driver)  # 退出账号

    driver.quit()  # 关闭浏览器


@pytest.fixture(scope='session')
def del_all_address(user_driver):

    yield
    del_all(user_driver)


@pytest.fixture
def get_user_address_index(user_driver):
    user_driver.get('http://101.34.221.219:8010/?s=useraddress/index.html')