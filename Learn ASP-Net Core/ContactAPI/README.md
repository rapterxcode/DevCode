# 📞 Contact API

A modern RESTful API built with ASP.NET Core for managing contacts with comprehensive CRUD operations.

## 🚀 Features

- **CRUD Operations**: Create, Read, Update, Delete contacts
- **Search & Pagination**: Filter contacts with pagination support
- **Data Validation**: Comprehensive input validation
- **Swagger Documentation**: Interactive API docs
- **Entity Framework Core**: Modern ORM with SQLite
- **Clean Architecture**: Service layer with dependency injection

## 🛠️ Technology Stack

- ASP.NET Core 8.0
- Entity Framework Core
- SQLite Database
- Swagger/OpenAPI

## 📋 Prerequisites

- .NET 8.0 SDK
- Visual Studio 2022 or VS Code

## 🚀 Quick Start

```bash
# Navigate to project
cd "DevCode/Learn ASP-Net Core/ContactAPI"

# Restore dependencies
dotnet restore

# Run the application
dotnet run
```

**Access Points:**
- API: `https://localhost:7001`
- Swagger UI: `https://localhost:7001` (root URL)
- Health Check: `https://localhost:7001/api/contacts/health`

## 📚 API Endpoints

### Get All Contacts
```http
GET /api/contacts
GET /api/contacts?search=john&page=1&pageSize=10
```

### Get Contact by ID
```http
GET /api/contacts/{id}
```

### Create Contact
```http
POST /api/contacts
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "phoneNumber": "+1234567890",
  "address": "123 Main St, City, State 12345"
}
```

### Update Contact
```http
PUT /api/contacts/{id}
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Smith"
}
```

### Delete Contact
```http
DELETE /api/contacts/{id}
```

## 📊 Data Model

```csharp
public class Contact
{
    public int Id { get; set; }                    // Primary key
    public string FirstName { get; set; }          // Required, max 50 chars
    public string LastName { get; set; }           // Required, max 50 chars
    public string Email { get; set; }              // Required, unique, max 100 chars
    public string PhoneNumber { get; set; }        // Required, max 20 chars
    public string? Address { get; set; }           // Optional, max 200 chars
    public DateTime CreatedAt { get; set; }        // Auto-generated
    public DateTime UpdatedAt { get; set; }        // Auto-updated
    public string FullName => $"{FirstName} {LastName}".Trim(); // Computed
}
```

## 🏗️ Project Structure

```
ContactAPI/
├── Controllers/ContactsController.cs    # API endpoints
├── Data/ContactDbContext.cs             # Database context
├── DTOs/ContactDto.cs                   # Data transfer objects
├── Models/Contact.cs                    # Entity model
├── Services/                            # Business logic
│   ├── IContactService.cs
│   └── ContactService.cs
├── Program.cs                           # App configuration
└── appsettings.json                     # Configuration
```

## 🔧 Configuration

Database connection in `appsettings.json`:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Data Source=ContactAPI.db"
  }
}
```

## 🧪 Testing

### Using Swagger UI
1. Navigate to `https://localhost:7001` when running
2. Use interactive interface to test endpoints

### Using curl
```bash
# Get all contacts
curl -X GET "https://localhost:7001/api/contacts"

# Create contact
curl -X POST "https://localhost:7001/api/contacts" \
  -H "Content-Type: application/json" \
  -d '{"firstName":"Jane","lastName":"Doe","email":"jane@example.com","phoneNumber":"+1234567890"}'
```

## 🔒 Security & Validation

- Input validation using Data Annotations
- SQL injection protection via EF Core
- CORS configuration
- Proper HTTP status codes

## 🚀 Deployment

```bash
# Development
dotnet run

# Production build
dotnet publish -c Release
```

## 📄 License

MIT License

---

**Happy Coding! 🎉** 