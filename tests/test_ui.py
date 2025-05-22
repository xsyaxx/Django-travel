import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import string

class TestUI:
    @pytest.fixture(autouse=True)
    def setup(self):
        # 设置 Chrome 选项
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')  # 无头模式，如果需要可以取消注释
        
        # 初始化 WebDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        
        # 打开测试页面
        self.driver.get("http://localhost:8000/static/index.html")
        
        yield
        
        # 清理
        self.driver.quit()
    
    def generate_random_string(self, length=10):
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    def test_register_and_login(self):
        """测试注册和登录功能"""
        # 生成测试数据
        email = f"test_{self.generate_random_string()}@example.com"
        username = f"user_{self.generate_random_string()}"
        password = "testpass123"
        
        # 点击注册按钮
        self.driver.find_element(By.XPATH, "//button[text()='注册']").click()
        
        # 填写注册表单
        self.driver.find_element(By.ID, "registerEmail").send_keys(email)
        self.driver.find_element(By.ID, "registerUsername").send_keys(username)
        self.driver.find_element(By.ID, "registerPassword").send_keys(password)
        
        # 提交注册表单
        self.driver.find_element(By.XPATH, "//button[text()='注册']").click()
        
        # 等待注册成功提示
        time.sleep(2)  # 等待alert出现
        alert = self.driver.switch_to.alert
        assert "注册成功" in alert.text
        alert.accept()
        
        # 填写登录表单
        self.driver.find_element(By.ID, "loginEmail").send_keys(email)
        self.driver.find_element(By.ID, "loginPassword").send_keys(password)
        
        # 提交登录表单
        self.driver.find_element(By.XPATH, "//form[@onsubmit='login(event)']//button").click()
        
        # 验证登录成功
        user_email = self.wait.until(
            EC.presence_of_element_located((By.ID, "userEmail"))
        )
        assert email == user_email.text
    
    def test_create_article(self):
        """测试创建文章功能"""
        # 先登录
        self.test_register_and_login()
        
        # 点击新建文章按钮
        self.driver.find_element(By.ID, "newArticleBtn").click()
        
        # 填写文章表单
        title = f"Test Article {self.generate_random_string()}"
        content = f"Test Content {self.generate_random_string(20)}"
        
        self.driver.find_element(By.ID, "articleTitle").send_keys(title)
        self.driver.find_element(By.ID, "articleContent").send_keys(content)
        
        # 提交文章
        self.driver.find_element(By.XPATH, "//form[@onsubmit='createArticle(event)']//button").click()
        
        # 等待文章出现在列表中
        time.sleep(2)  # 等待文章列表更新
        articles = self.driver.find_elements(By.CLASS_NAME, "card-title")
        article_titles = [article.text for article in articles]
        assert title in article_titles
    
    def test_logout(self):
        """测试退出功能"""
        # 先登录
        self.test_register_and_login()
        
        # 点击退出按钮
        self.driver.find_element(By.XPATH, "//button[text()='退出']").click()
        
        # 验证回到未登录状态
        login_section = self.wait.until(
            EC.presence_of_element_located((By.ID, "loginSection"))
        )
        assert "hidden" not in login_section.get_attribute("class") 