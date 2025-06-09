from pathlib import Path

img_path = 'data/jmeter.png'  # 不需要变化、不需要后置的特殊前置条件，可以写出变量


# 一定要写相对路径
# 这段代码是一个基于 Selenium 的自动化测试用例，用于测试 Web 系统中“用户头像上传”功能是否正常工作

def test_upload_img(user_driver):
    # 1. 进入个人资料
    user_driver.get('http://101.34.221.219:8010/?s=personal/index.html')

    # 2. 点击头像的【修改】按钮
    el = user_driver.find_element('xpath', '/html/body/div[4]/div[3]/div/dl/dd[1]/span/a')
    el.click()

    # 3. 发送文件路径
    el = user_driver.find_element('xpath', '//*[@id="user-avatar-popup"]/div/div[2]/form/div[2]/div/input')

    #  技巧：相对转绝对
    path = Path(img_path)
    abs_path = str(path.absolute())
    print('文件的绝对路径', abs_path)

    el.send_keys(abs_path)  # 要求传递绝对路径

    # 4.点击【确认上传】按钮
    el = user_driver.find_element('xpath', '//*[@id="user-avatar-popup"]/div/div[2]/form/button')

    # el.click() # 出现 ElementNotInteractableException

    def f(x):
        try:
            el.click()
            return True
        except:
            return False

    user_driver.wait.until(f)

    # 1. time.sleep
    # 2. 显式等待

    # 5. 获取系统提示
    def f(x):
        try:
            user_driver.find_element('xpath', '/html/body/div[10]/div/p')
            return True
        except:
            return False

    user_driver.wait.until(f)

    el = user_driver.find_element('xpath', '/html/body/div[10]/div/p')
    msg = el.text

    # 6. 断言：系统提示

    assert msg == '上传成功'
