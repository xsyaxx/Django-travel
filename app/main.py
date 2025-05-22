from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routers import auth, articles, comments

app = FastAPI(
    title="研知笔录",
    description="面向科研人员的轻量级笔记与日志系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(articles.router, prefix="/api/articles", tags=["articles"])
app.include_router(comments.router, prefix="/api/comments", tags=["comments"])

@app.get("/")
async def root():
    return {"message": "Welcome to 研知笔录 API"} 