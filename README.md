# 研知笔录 (Research Notes)

一个基于 FastAPI 构建的研究笔记管理系统。

## 功能特点

- 用户认证系统（注册、登录）
- 文章管理
- 评论功能
- RESTful API
- 基于 JWT 的认证
- MySQL 数据库支持

## 技术栈

- Backend: FastAPI
- Database: MySQL
- Authentication: JWT
- Testing: pytest

## 安装步骤

1. 克隆仓库：
```bash
git clone [your-repository-url]
cd research-notes
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置数据库：
- 创建 MySQL 数据库
- 更新配置文件中的数据库连接信息

5. 运行应用：
```bash
uvicorn app.main:app --reload
```

## API 文档

启动应用后，访问以下地址查看 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 测试

运行测试：
```bash
pytest
```

## 许可证

MIT License 