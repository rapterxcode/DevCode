# Users Management API

A complete RESTful API for user and customer management built with FastAPI, SQLModel, and SQLite.

## 🚀 Features

- **User Management**: Complete CRUD operations for users
- **Customer Management**: Complete CRUD operations for customers
- **SQLite Database**: Lightweight database with SQLModel ORM
- **CORS Support**: Cross-origin request handling
- **Request Logging**: Comprehensive request monitoring
- **Performance Tracking**: Request timing middleware
- **Health Monitoring**: System health check endpoint
- **Type Safety**: Full Pydantic validation

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)

## 🛠️ Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "DevCode/Learn FastAPI/Users-Management-API"
   ```

2. **Install dependencies**
   ```bash
   pip install fastapi uvicorn sqlmodel pydantic-settings
   ```

3. **Run the server**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## 🌐 API Endpoints

### Health Check
- `GET /` - Basic API information
- `GET /health` - Detailed health status and API documentation

### Users
- `POST /users` - Create new user
- `GET /users` - Get all users
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Customers
- `POST /customers` - Create new customer
- `GET /customers` - Get all customers
- `GET /customers/{customer_id}` - Get customer by ID
- `PUT /customers/{customer_id}` - Update customer
- `DELETE /customers/{customer_id}` - Delete customer

## 📖 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing with Postman

### Import Postman Collection

1. **Open Postman**
2. **Import Collection**: Click "Import" and select `Users-Management-API.postman_collection.json`
3. **Ready to use**: The collection is pre-configured for localhost:8000

### Collection Structure

The Postman collection is organized into three main folders:

#### 1. Health Check
- **Root Endpoint**: Basic API information
- **Health Check**: Detailed system status

#### 2. Users
- **Create User**: POST with user data
- **Get All Users**: GET all users
- **Get User by ID**: GET specific user
- **Update User**: PUT with partial data
- **Delete User**: DELETE by ID

#### 3. Customers
- **Create Customer**: POST with customer data
- **Get All Customers**: GET all customers
- **Get Customer by ID**: GET specific customer
- **Update Customer**: PUT with partial data
- **Delete Customer**: DELETE by ID

### Testing Workflow

1. **Start the API server**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

2. **Test Health Check**
   - Run "Health Check" to verify API is running

3. **Test Users Endpoints**
   - Create a user first
   - Get all users to see the created user
   - Get user by ID using the returned ID
   - Update the user
   - Delete the user

4. **Test Customers Endpoints**
   - Create a customer
   - Get all customers
   - Get customer by ID
   - Update customer status
   - Delete customer

## 📝 Example Requests

### Create User
```bash
POST http://localhost:8000/users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

### Create Customer
```bash
POST http://localhost:8000/customers
Content-Type: application/json

{
  "name": "Jane Smith",
  "email": "jane.smith@company.com",
  "phone": "+1-555-123-4567",
  "address": "456 Business Ave, Suite 100, New York, NY 10001",
  "company": "Tech Solutions Inc.",
  "status": "active"
}
```

### Update Customer Status
```bash
PUT http://localhost:8000/customers/1
Content-Type: application/json

{
  "status": "premium"
}
```

## 🔧 Configuration

The API uses environment variables for configuration. Create a `.env` file for custom settings:

```env
DB_NAME=users_store.db
PORT=8000
ENVIRONMENT=development
APP_NAME=Users Management API
APP_VERSION=1.0.0
APP_DESCRIPTION=Users Management API with SQLite database
```

## 📊 Database Schema

### Users Table
- `id`: Primary key (auto-generated)
- `name`: User's full name (indexed)
- `email`: Email address (unique, indexed)
- `password`: Password (should be hashed in production)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Customers Table
- `id`: Primary key (auto-generated)
- `name`: Customer's full name (indexed)
- `email`: Email address (unique, indexed)
- `phone`: Phone number (indexed)
- `address`: Full address
- `company`: Company name (optional)
- `status`: Customer status (active/inactive/premium)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## 🚨 Production Considerations

- **Password Hashing**: Implement proper password hashing
- **Environment Variables**: Use secure environment configuration
- **CORS Configuration**: Restrict CORS origins for production
- **Authentication**: Add JWT or OAuth authentication
- **Database**: Use PostgreSQL or MySQL for production
- **Rate Limiting**: Implement API rate limiting
- **Logging**: Configure proper logging levels
- **Input Validation**: Add comprehensive input sanitization
- **HTTPS**: Use SSL/TLS encryption

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   uvicorn main:app --reload --port 8001
   ```

2. **Database file not found**
   - The database will be created automatically on first run

3. **Import errors**
   ```bash
   pip install -r requirements.txt
   ```

### Logs

The API provides detailed logging:
- Request/response logging
- Performance timing
- Error tracking
- Database operations

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Happy Testing! 🎉** 