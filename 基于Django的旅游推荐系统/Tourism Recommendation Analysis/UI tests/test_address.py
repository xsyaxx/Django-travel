import time
from commons import settings

def test_new_address(user_driver, del_all_address):
    #  1. 访问我的地址：http://101.34.221.219:8010/?s=useraddress/index.html
    user_driver.get('http://101.34.221.219:8010/?s=useraddress/index.html')

    # 2. 点击【新增地址】按钮：/html/body/div[4]/div[3]/div/div[1]/button
    el = user_driver.find_element('xpath', '/html/body/div[4]/div[3]/div/div[1]/button')
    el.click()

    # 找到iframe、进入iframe：//iframe[@src="http://101.34.221.219:8010/?s=useraddress/saveinfo.html"]

    iframe = user_driver.find_element('xpath',
                                      '//iframe[@src="http://101.34.221.219:8010/?s=useraddress/saveinfo.html"]')
    user_driver.switch_to.frame(iframe)

    # 3. 输入【别名】：/html/body/div[1]/form/div[1]/input

    # /html/body/div[1]/form/div[1]/input
    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[1]/input')
    el.send_keys('第一个地址')

    # 4. 输入【姓名】：/html/body/div[1]/form/div[2]/input
    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[2]/input')
    el.send_keys('收件人北凡')

    # 5. 输入【电话】：/html/body/div[1]/form/div[3]/input
    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[3]/input')
    el.send_keys('13111121211')

    # 6. 输入【地址】：//*[@id="form-address"]
    el = user_driver.find_element('xpath', '//*[@id="form-address"]')
    el.send_keys('XX胡同101号')

    # 7.    选择【省份】：
    # 点击【省份】，展示选项： /html/body/div[1]/form/div[4]/div[1]/a/span
    # 点击【选项】，完成选择： /html/body/div[1]/form/div[4]/div[1]/div/ul/li[text() = "北京市"]
    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[4]/div[1]/a/span')
    el.click()

    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[4]/div[1]/div/ul/li[text() = "北京市"]')
    el.click()

    # 8.    选择【城市】
    # 点击【城市】，展示选项： /html/body/div[1]/form/div[4]/div[2]/a/span
    # 点击【选项】，完成选择： /html/body/div[1]/form/div[4]/div[2]/div/ul/li[text()="东城区"]

    el = user_driver.find_element('xpath', ' /html/body/div[1]/form/div[4]/div[2]/a/span')
    el.click()

    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[4]/div[2]/div/ul/li[text()="东城区"] ')
    el.click()

    # 9. 选择【区县】
    # 点击【区县】，展示选项： /html/body/div[1]/form/div[4]/div[3]/a/span
    # 点击【选项】，完成选择： /html/body/div[1]/form/div[4]/div[3]/div/ul/li[text()="东四街道"]

    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[4]/div[3]/a/span')
    el.click()

    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[4]/div[3]/div/ul/li[text()="东四街道"]')
    el.click()

    # 10. 点击【保存】按钮：/html/body/div[1]/form/div[7]/button

    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[7]/button')
    el.click()

    # 11.  获取系统提示
    # 12  断言：系统提示== "操作成功"

    user_driver.wait.until(lambda x: user_driver.find_element('xpath', settings.xpath_msg).text != "")

    el = user_driver.find_element('xpath', settings.xpath_msg)
    msg = el.text

    assert msg == '操作成功'


def test_update_address(user_driver, del_all_address):
    """
    1. 访问收货地址：http://101.34.221.219:8010/?s=useraddress/index.html
    2. 点击【编辑按钮】: //a[text()=" 编辑"]
       切换iframe
    3. 清空【别名】：/html/body/div[1]/form/div[1]/input
    3. 输入【别名】：/html/body/div[1]/form/div[1]/input
    4. 清空【姓名】：/html/body/div[1]/form/div[2]/input
    4. 输入【姓名】：/html/body/div[1]/form/div[2]/input
    5. 清空【电话】：/html/body/div[1]/form/div[3]/input
    5. 输入【电话】：/html/body/div[1]/form/div[3]/input
    6. 清空【地址】：//*[@id="form-address"]
    6. 输入【地址】：//*[@id="form-address"]
    7. 选择【省份】：
        点击【省份】，展示选项：/html/body/div[1]/form/div[4]/div[1]/a/span
        点击【选项】，完成选择：/html/body/div[1]/form/div[4]/div[1]/div/ul/li[text()="北京市"]

    8. 选择【城市】
        点击【城市】，展示选项：/html/body/div[1]/form/div[4]/div[2]/a/span
        点击【选项】，完成选择：/html/body/div[1]/form/div[4]/div[2]/div/ul/li[text()="东城区"]
    9. 选择【区县】
        点击【区县】，展示选项：/html/body/div[1]/form/div[4]/div[3]/a/span
        点击【选项】，完成选择：/html/body/div[1]/form/div[4]/div[3]/div/ul/li[text()="东四街道"]


    10. 点击【保存】按钮：/html/body/div[1]/form/div[7]/button

    11.  获取系统提示
    12  断言：系统提示== "操作成功"

    """
    #  1. 访问我的地址：http://101.34.221.219:8010/?s=useraddress/index.html
    user_driver.get('http://101.34.221.219:8010/?s=useraddress/index.html')

    # 2. 点击【编辑按钮】: //a[text()=" 编辑"]
    el = user_driver.find_element('xpath', '//a[text()=" 编辑"]')
    el.click()

    # 找到iframe、进入iframe：//iframe[starts-with(@src,"http://101.34.221.219:8010/")]
    iframe = user_driver.find_element('xpath',
                                      '//iframe[starts-with(@src,"http://101.34.221.219:8010/")]')
    user_driver.switch_to.frame(iframe)

    # 3. 输入【别名】：/html/body/div[1]/form/div[1]/input

    # /html/body/div[1]/form/div[1]/input
    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[1]/input')
    el.clear()
    el.send_keys('第二个地址')

    # 4. 输入【姓名】：/html/body/div[1]/form/div[2]/input
    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[2]/input')
    el.clear()
    el.send_keys('收件人百里')

    # 5. 输入【电话】：/html/body/div[1]/form/div[3]/input
    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[3]/input')
    el.clear()
    el.send_keys('19111112222')

    # 6. 输入【地址】：//*[@id="form-address"]
    el = user_driver.find_element('xpath', '//*[@id="form-address"]')
    el.clear()
    el.send_keys('XX胡同999号')

    # 7.    选择【省份】：
    # 点击【省份】，展示选项： /html/body/div[1]/form/div[4]/div[1]/a/span
    # 点击【选项】，完成选择： /html/body/div[1]/form/div[4]/div[1]/div/ul/li[text() = "北京市"]
    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[4]/div[1]/a/span')
    el.click()

    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[4]/div[1]/div/ul/li[text() = "天津市"]')
    el.click()

    # 8.    选择【城市】
    # 点击【城市】，展示选项： /html/body/div[1]/form/div[4]/div[2]/a/span
    # 点击【选项】，完成选择： /html/body/div[1]/form/div[4]/div[2]/div/ul/li[text()="东城区"]

    el = user_driver.find_element('xpath', ' /html/body/div[1]/form/div[4]/div[2]/a/span')
    el.click()

    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[4]/div[2]/div/ul/li[text()="和平区"] ')
    el.click()

    # 9. 选择【区县】
    # 点击【区县】，展示选项： /html/body/div[1]/form/div[4]/div[3]/a/span
    # 点击【选项】，完成选择： /html/body/div[1]/form/div[4]/div[3]/div/ul/li[text()="东四街道"]

    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[4]/div[3]/a/span')
    el.click()

    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[4]/div[3]/div/ul/li[text()="小白楼街道"]')
    el.click()

    # 10. 点击【保存】按钮：/html/body/div[1]/form/div[7]/button

    time.sleep(4)  # 等待编辑时，系统提示小时
    el = user_driver.find_element('xpath', '/html/body/div[1]/form/div[7]/button')
    el.click()

    # 11.  获取系统提示
    # 12  断言：系统提示== "操作成功"
    user_driver.wait.until(lambda x: user_driver.find_element('xpath', settings.xpath_msg).text != "")
    el = user_driver.find_element('xpath', settings.xpath_msg)
    msg = el.text

    assert msg == '操作成功'


def test_del_address(user_driver, del_all_address):
    """
    1. 访问收货地址：http://101.34.221.219:8010/?s=useraddress/index.html
    2. 点击【删除按钮】: //a[text()=" 删除"]
    3. 点击【确认】操作：//span[text()="确定"]


    11.  获取系统提示
    12  断言：系统提示== "删除成功"

    """

    user_driver.get('http://101.34.221.219:8010/?s=useraddress/index.html')
    el = user_driver.find_element('xpath', '//a[text()=" 删除"]')
    el.click()

    el = user_driver.find_element('xpath', '//span[text()="确定"]')
    el.click()

    user_driver.wait.until(lambda x: user_driver.find_element('xpath', settings.xpath_msg).text != "")
    el = user_driver.find_element('xpath', settings.xpath_msg)
    msg = el.text

    assert msg == '删除成功'
