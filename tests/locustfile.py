from locust import HttpUser, task, between
import random
import string

class ResearchNotesUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """登录并获取token"""
        # 先注册一个用户
        self.username = ''.join(random.choices(string.ascii_letters, k=10))
        self.email = f"{self.username}@example.com"
        self.password = "testpass123"
        
        self.client.post("/api/auth/register", json={
            "email": self.email,
            "username": self.username,
            "password": self.password
        })
        
        # 登录获取token
        response = self.client.post("/api/auth/token", data={
            "username": self.email,
            "password": self.password
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def view_articles(self):
        """查看文章列表"""
        self.client.get("/api/articles/")
    
    @task(1)
    def create_article(self):
        """创建新文章"""
        title = ''.join(random.choices(string.ascii_letters, k=20))
        content = ''.join(random.choices(string.ascii_letters + ' ', k=200))
        
        self.client.post(
            "/api/articles/",
            headers=self.headers,
            json={
                "title": title,
                "content": content
            }
        )
    
    @task(2)
    def view_article_details(self):
        """查看文章详情"""
        # 假设文章ID范围在1-100之间
        article_id = random.randint(1, 100)
        self.client.get(f"/api/articles/{article_id}")
    
    @task(1)
    def add_comment(self):
        """添加评论"""
        article_id = random.randint(1, 100)
        content = ''.join(random.choices(string.ascii_letters + ' ', k=50))
        
        self.client.post(
            "/api/comments/",
            headers=self.headers,
            json={
                "content": content,
                "article_id": article_id
            }
        ) 