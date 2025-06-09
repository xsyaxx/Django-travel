import pytest
import logging
import allure

logger = logging.getLogger(__name__)


@allure.epic('码尚自动化测试项目')
@allure.feature('模块A')
@allure.story('文件上传功能')
@allure.title('上传失败')
def test_abc():
    logger.info('11111')


@allure.epic('码尚自动化测试项目')
@allure.feature('模块A')
@allure.story('文件上传功能')
@allure.title('上传成功')
def test_baa():
    logger.info('22222')


@allure.epic('码尚自动化测试项目')
@allure.feature('模块B')
@allure.story('充值体现功能')
@allure.title('充值成功')
def test_bbc():
    logger.info('444444')
