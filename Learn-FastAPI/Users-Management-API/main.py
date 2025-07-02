"""
FastAPI Users Management API - User CRUD operations with SQLite database
"""

from pydantic_settings import BaseSettings
from datetime import datetime
from pydantic import BaseModel
from typing import Annotated, Optional, List
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application configuration settings"""
    db_name: str = "users_store.db"
    port: int = 8000
    environment: str = "development"
    app_name: str = "Users Management API"
    app_version: str = "1.0.0"
    app_description: str = "Users Management API with SQLite database"

settings = Settings()


class Users(SQLModel, table=True):
    """User database model"""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)


class Customer(SQLModel, table=True):
    """Customer database model"""
    __tablename__ = "customers"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    phone: str = Field(index=True)
    address: str
    company: Optional[str] = None
    status: str = Field(default="active")  # active, inactive, premium
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)


# Database Configuration
sqlite_file_name = "users_store.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# SQLite connection arguments for thread safety
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    """Create database and tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Database session dependency"""
    with Session(engine) as session:
        yield session


# Type alias for session dependency injection
SessionDep = Annotated[Session, Depends(get_session)]


class UserCreate(BaseModel):
    """User creation model"""
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    """User response model (excludes password)"""
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    """User update model (partial updates)"""
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class CustomerCreate(BaseModel):
    """Customer creation model"""
    name: str
    email: str
    phone: str
    address: str
    company: Optional[str] = None
    status: str = "active"


class CustomerResponse(BaseModel):
    """Customer response model"""
    id: int
    name: str
    email: str
    phone: str
    address: str
    company: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime


class CustomerUpdate(BaseModel):
    """Customer update model (partial updates)"""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None


class UserResponseWithMessage(BaseModel):
    """User response with success message"""
    message: str
    data: UserResponse


class CustomerResponseWithMessage(BaseModel):
    """Customer response with success message"""
    message: str
    data: CustomerResponse


class ListResponseWithMessage(BaseModel):
    """List response with success message"""
    message: str
    data: List[CustomerResponse]
    count: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup: Initialize database
    logger.info("Starting up Users Management API...")
    create_db_and_tables()
    logger.info("Database initialized successfully")
    
    yield
    
    # Shutdown: Clean up resources
    logger.info("Shutting down Users Management API...")
    engine.dispose()
    logger.info("Database connections disposed")


# Initialize FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests with timing"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s"
    )
    
    return response


# API Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Hello Users Management API"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": {
            "name": settings.app_name,
            "version": settings.app_version,
            "description": settings.app_description,
            "environment": settings.environment
        },
        "database": {
            "status": "connected",
            "type": "SQLite",
            "file": settings.db_name
        },
        "endpoints": {
            "root": "/",
            "health": "/health",
            "users": {
                "list": "/users",
                "create": "/users",
                "get": "/users/{user_id}",
                "update": "/users/{user_id}",
                "delete": "/users/{user_id}"
            },
            "customers": {
                "list": "/customers",
                "create": "/customers",
                "get": "/customers/{customer_id}",
                "update": "/customers/{customer_id}",
                "delete": "/customers/{customer_id}"
            }
        },
        "docs": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


@app.post("/users", response_model=UserResponseWithMessage)
async def create_user(user: UserCreate, session: SessionDep):
    """Create a new user"""
    new_user = Users(name=user.name, email=user.email, password=user.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    logger.info(f"Created new user: {new_user.email}")
    return {
        "message": "User created successfully",
        "data": new_user
    }


@app.get("/users", response_model=List[UserResponse])
async def get_users(session: SessionDep):
    """Get all users"""
    users = session.exec(select(Users)).all()
    logger.info(f"Retrieved {len(users)} users")
    return users


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: SessionDep):
    """Get user by ID"""
    user = session.get(Users, user_id)
    if not user:
        logger.warning(f"User not found with ID: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Retrieved user: {user.email}")
    return user


@app.put("/users/{user_id}", response_model=UserResponseWithMessage)
async def update_user(user_id: int, user: UserUpdate, session: SessionDep):
    """Update user by ID"""
    # Find existing user
    db_user = session.get(Users, user_id)
    if not db_user:
        logger.warning(f"User not found for update with ID: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only provided fields
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    # Update timestamp
    db_user.updated_at = datetime.now()
    
    # Save changes
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    logger.info(f"Updated user: {db_user.email}")
    return {
        "message": "User updated successfully",
        "data": db_user
    }


@app.delete("/users/{user_id}", response_model=UserResponseWithMessage)
async def delete_user(user_id: int, session: SessionDep):
    """Delete user by ID"""
    # Find user to delete
    user = session.get(Users, user_id)
    if not user:
        logger.warning(f"User not found for deletion with ID: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete user
    session.delete(user)
    session.commit()
    
    logger.info(f"Deleted user: {user.email}")
    return {
        "message": "User deleted successfully",
        "data": user
    }


@app.post("/customers", response_model=CustomerResponseWithMessage)
async def create_customer(customer: CustomerCreate, session: SessionDep):
    """Create a new customer"""
    new_customer = Customer(name=customer.name, email=customer.email, phone=customer.phone, address=customer.address, company=customer.company, status=customer.status)
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    
    logger.info(f"Created new customer: {new_customer.email}")
    return {
        "message": "Customer created successfully",
        "data": new_customer
    }


@app.get("/customers", response_model=ListResponseWithMessage)
async def get_customers(session: SessionDep):
    """Get all customers"""
    customers = session.exec(select(Customer)).all()
    logger.info(f"Retrieved {len(customers)} customers")
    return {
        "message": f"Retrieved {len(customers)} customers successfully",
        "data": customers,
        "count": len(customers)
    }


@app.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: int, session: SessionDep):
    """Get customer by ID"""
    customer = session.get(Customer, customer_id)
    if not customer:
        logger.warning(f"Customer not found with ID: {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    
    logger.info(f"Retrieved customer: {customer.email}")
    return customer


@app.put("/customers/{customer_id}", response_model=CustomerResponseWithMessage)
async def update_customer(customer_id: int, customer: CustomerUpdate, session: SessionDep):
    """Update customer by ID"""
    # Find existing customer
    db_customer = session.get(Customer, customer_id)
    if not db_customer:
        logger.warning(f"Customer not found for update with ID: {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Update only provided fields
    customer_data = customer.model_dump(exclude_unset=True)
    for key, value in customer_data.items():
        setattr(db_customer, key, value)
    
    # Update timestamp
    db_customer.updated_at = datetime.now()
    
    # Save changes
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    
    logger.info(f"Updated customer: {db_customer.email}")
    return {
        "message": "Customer updated successfully",
        "data": db_customer
    }


@app.delete("/customers/{customer_id}", response_model=CustomerResponseWithMessage)
async def delete_customer(customer_id: int, session: SessionDep):
    """Delete customer by ID"""
    # Find customer to delete
    customer = session.get(Customer, customer_id)
    if not customer:
        logger.warning(f"Customer not found for deletion with ID: {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Delete customer
    session.delete(customer)
    session.commit()
    
    logger.info(f"Deleted customer: {customer.email}")
    return {
        "message": "Customer deleted successfully",
        "data": customer
    }
