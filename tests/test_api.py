import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.session import Base, get_db

# Test database URL
SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://root:hyx72565700@localhost/research_notes"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)

TestingSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest.fixture
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def client(test_db):
    async def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            await db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_create_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"

def test_login(client):
    # First create a user
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    
    # Then try to login
    response = client.post(
        "/api/auth/token",
        data={
            "username": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_article(client):
    # First create a user and get token
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    
    login_response = client.post(
        "/api/auth/token",
        data={
            "username": "test@example.com",
            "password": "testpass123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Create an article
    response = client.post(
        "/api/articles/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Article",
            "content": "This is a test article content"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Article"
    assert data["content"] == "This is a test article content" 