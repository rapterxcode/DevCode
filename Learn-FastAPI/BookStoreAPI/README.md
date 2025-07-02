# 📚 Bookstore API

A modern, high-performance RESTful API for bookstore management built with **FastAPI** and **SQLModel**. This project demonstrates best practices for building production-ready APIs with automatic documentation, database integration, and comprehensive CRUD operations.

## ✨ Features

- 🚀 **FastAPI** - High-performance web framework for building APIs
- 🗄️ **SQLModel** - Modern SQL databases with Python, combining SQLAlchemy and Pydantic
- 📊 **SQLite** - Lightweight, serverless database
- 📖 **Automatic Documentation** - Interactive API docs with Swagger UI and ReDoc
- 🔍 **Data Validation** - Automatic request/response validation with Pydantic
- 🏷️ **Organized Endpoints** - Tagged and documented API endpoints
- 🔄 **CRUD Operations** - Complete Create, Read, Update, Delete functionality
- 📝 **OpenAPI Schema** - Fully compliant OpenAPI 3.0 specification

## 🛠️ Technology Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **FastAPI** | Web framework | >= 0.68.0 |
| **SQLModel** | ORM and validation | >= 0.0.8 |
| **SQLite** | Database | Built-in |
| **Uvicorn** | ASGI server | >= 0.15.0 |
| **Python** | Programming language | >= 3.7 |

## 📁 Project Structure

```
BookStoreAPI/
├── 📄 main.py              # Main application file
├── 📄 requirements.txt     # Python dependencies
├── 📄 README.md           # This file
├── 🗄️ bookstore.db        # SQLite database (auto-generated)
└── 📊 __pycache__/        # Python cache files
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd BookStoreAPI
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```
   
   Or with uvicorn for development:
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API:**
   - **API Base URL:** http://localhost:8000
   - **Interactive Documentation:** http://localhost:8000/docs
   - **Alternative Documentation:** http://localhost:8000/redoc
   - **OpenAPI Schema:** http://localhost:8000/openapi.json

## 📋 API Endpoints

### 🏠 Root Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message |

### 📚 Books Management

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|-------------|
| `POST` | `/books/` | Create a new book | BookCreate |
| `GET` | `/books/` | Get all books | - |
| `GET` | `/books/{id}` | Get book by ID | - |
| `PUT` | `/books/{id}` | Update book | BookUpdate |
| `DELETE` | `/books/{id}` | Delete book | - |

## 📊 Data Models

### BookCreate (Request)
```json
{
  "title": "Python Programming Guide",
  "author": "John Smith",
  "price": 29.99,
  "isbn": "978-0123456789",
  "stock": 15
}
```

### BookRead (Response)
```json
{
  "id": 1,
  "title": "Python Programming Guide",
  "author": "John Smith",
  "price": 29.99,
  "isbn": "978-0123456789",
  "stock": 15
}
```

### BookUpdate (Request)
```json
{
  "title": "Updated Book Title",
  "price": 35.99,
  "stock": 20
}
```

## 🔧 Usage Examples

### Using curl

#### Create a new book
```bash
curl -X POST "http://localhost:8000/books/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "FastAPI Guide",
       "author": "Jane Doe",
       "price": 39.99,
       "isbn": "978-0987654321",
       "stock": 25
     }'
```

#### Get all books
```bash
curl -X GET "http://localhost:8000/books/"
```

#### Get a specific book
```bash
curl -X GET "http://localhost:8000/books/1"
```

#### Update a book
```bash
curl -X PUT "http://localhost:8000/books/1" \
     -H "Content-Type: application/json" \
     -d '{
       "price": 45.99,
       "stock": 30
     }'
```

#### Delete a book
```bash
curl -X DELETE "http://localhost:8000/books/1"
```

### Using Python requests

```python
import requests

base_url = "http://localhost:8000"

# Create a book
book_data = {
    "title": "SQLModel Tutorial",
    "author": "Sebastian Ramirez",
    "price": 49.99,
    "isbn": "978-1234567890",
    "stock": 10
}

response = requests.post(f"{base_url}/books/", json=book_data)
print(response.json())

# Get all books
response = requests.get(f"{base_url}/books/")
print(response.json())
```

## 🏗️ Architecture & Design

### 📋 SQLModel Architecture

This project uses **SQLModel**, which provides:

1. **Unified Models**: Same model classes for database tables and API schemas
2. **Type Safety**: Full type hints and validation
3. **Modern Syntax**: Pythonic way to work with databases
4. **FastAPI Integration**: Seamless integration with FastAPI features

### 🗄️ Database Design

```sql
-- Books table structure
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    price FLOAT NOT NULL,
    isbn VARCHAR UNIQUE NOT NULL,
    stock INTEGER DEFAULT 0
);

-- Indexes for performance
CREATE INDEX ix_books_title ON books(title);
CREATE INDEX ix_books_author ON books(author);
CREATE INDEX ix_books_isbn ON books(isbn);
```

## 🔄 Development Workflow

### 1. **Model-First Approach**
   - Define SQLModel classes that serve as both database models and API schemas
   - Automatic validation and serialization

### 2. **Dependency Injection**
   - Database session management through FastAPI's dependency system
   - Clean separation of concerns

### 3. **Automatic Documentation**
   - OpenAPI schema generation
   - Interactive API documentation

## 🚀 Advanced Features & Extensions

### 🔐 Authentication & Authorization
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/protected")
def protected_route(token: str = Depends(security)):
    # Implement JWT validation
    pass
```

### 📊 Pagination
```python
from fastapi import Query

@app.get("/books/")
def get_books(skip: int = 0, limit: int = Query(default=100, le=100)):
    # Implement pagination logic
    pass
```

### 🔍 Search & Filtering
```python
@app.get("/books/search")
def search_books(q: str, author: Optional[str] = None):
    # Implement search functionality
    pass
```

### 📈 Monitoring & Logging
```python
import logging
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log request details
    response = await call_next(request)
    return response
```

## 🔧 Configuration Options

### Environment Variables
```bash
# .env file
DATABASE_URL=sqlite:///./bookstore.db
DEBUG=True
LOG_LEVEL=INFO
```

### Advanced Configuration
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./bookstore.db"
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## 🧪 Testing

### Unit Tests
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_book():
    response = client.post("/books/", json={
        "title": "Test Book",
        "author": "Test Author",
        "price": 19.99,
        "isbn": "978-0000000000",
        "stock": 5
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"
```

## 📈 Scaling & Production

### 🐳 Docker Deployment

#### Quick Start with Docker

**Development Mode:**
```bash
# Run with hot reload for development
docker-compose -f docker-compose.dev.yml up --build

# Access API at http://localhost:8000
```

**Production Mode:**
```bash
# Full production stack with PostgreSQL, Redis, Nginx
docker-compose up -d --build

# Access API at http://localhost (port 80)
# Grafana dashboard at http://localhost:3000
# Prometheus at http://localhost:9090
```

#### Available Docker Configurations

| File | Purpose | Services |
|------|---------|----------|
| `docker-compose.dev.yml` | Development | API only with SQLite |
| `docker-compose.yml` | Production | API + PostgreSQL + Redis + Nginx + Monitoring |

#### Docker Commands

```bash
# Build and run development
docker-compose -f docker-compose.dev.yml up --build

# Run production stack
docker-compose up -d

# View logs
docker-compose logs -f bookstore-api

# Stop services
docker-compose down

# Remove volumes (caution: deletes data)
docker-compose down -v
```

#### Production Features

- **Load Balancer**: Nginx for reverse proxy and load balancing
- **Database**: PostgreSQL for production data storage
- **Caching**: Redis for improved performance
- **Monitoring**: Prometheus + Grafana for metrics and dashboards
- **Health Checks**: Built-in container health monitoring
- **Security**: Non-root user in containers
- **Persistence**: Data volumes for database and cache

### 🌐 Production Database
```python
# PostgreSQL example
DATABASE_URL = "postgresql://user:password@localhost/bookstore"
engine = create_engine(DATABASE_URL)
```

### 🔄 Database Migrations
```python
# Using Alembic
from alembic import command
from alembic.config import Config

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** - For the amazing web framework
- **SQLModel** - For the modern ORM solution
- **Pydantic** - For data validation and settings management
- **Uvicorn** - For the lightning-fast ASGI server

## 📞 Support

If you have any questions or issues, please:

1. Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
2. Review the [SQLModel documentation](https://sqlmodel.tiangolo.com/)
3. Open an issue in this repository

---

**Happy Coding! 🚀**