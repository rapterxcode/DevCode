from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import List, Optional

DATABASE_URL = "sqlite:///./bookstore.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

class BookBase(SQLModel):
    title: str = Field(index=True)
    author: str = Field(index=True)
    price: float
    isbn: str = Field(unique=True, index=True)
    stock: int = Field(default=0)

class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int

class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    isbn: Optional[str] = None
    stock: Optional[int] = None

SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="Bookstore API",
    description="A comprehensive bookstore management API with SQLite database",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "books",
            "description": "Operations with books. Create, read, update and delete books.",
        },
        {
            "name": "root",
            "description": "Root endpoint",
        }
    ]
)


def get_session():
    with Session(engine) as session:
        yield session

@app.get("/", tags=["root"], summary="Welcome message")
def read_root():
    """
    Welcome endpoint that returns a greeting message.
    """
    return {"message": "Welcome to the Bookstore API"}

@app.post("/books/", response_model=BookRead, tags=["books"], summary="Create a new book")
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    """
    Create a new book with the following information:
    
    - **title**: Book title (required)
    - **author**: Book author (required)
    - **price**: Book price (required)
    - **isbn**: Book ISBN (required, must be unique)
    - **stock**: Number of books in stock (optional, default: 0)
    """
    statement = select(Book).where(Book.isbn == book.isbn)
    existing_book = session.exec(statement).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    db_book = Book(**book.dict())
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[BookRead], tags=["books"], summary="Get all books")
def get_books(session: Session = Depends(get_session)):
    """
    Retrieve all books from the database.
    
    Returns a list of all books with their complete information.
    """
    books = session.exec(select(Book)).all()
    return books

@app.get("/books/{book_id}", response_model=BookRead, tags=["books"], summary="Get a specific book")
def get_book(book_id: int, session: Session = Depends(get_session)):
    """
    Get a specific book by its ID.
    
    - **book_id**: The ID of the book to retrieve
    """
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=BookRead, tags=["books"], summary="Update a book")
def update_book(book_id: int, book_update: BookUpdate, session: Session = Depends(get_session)):
    """
    Update a specific book by its ID.
    
    - **book_id**: The ID of the book to update
    - **book_update**: Fields to update (all fields are optional)
    """
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_data = book_update.dict(exclude_unset=True)
    for field, value in book_data.items():
        setattr(book, field, value)
    
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@app.delete("/books/{book_id}", tags=["books"], summary="Delete a book")
def delete_book(book_id: int, session: Session = Depends(get_session)):
    """
    Delete a specific book by its ID.
    
    - **book_id**: The ID of the book to delete
    """
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_title = book.title
    session.delete(book)
    session.commit()
    return {"message": f"Book '{book_title}' deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)