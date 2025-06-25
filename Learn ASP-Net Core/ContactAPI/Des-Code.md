# 📞 Contact API - ขั้นตอนการพัฒนาโปรเจค

## 🎯 ภาพรวมโปรเจค
โปรเจค Contact API เป็น RESTful API ที่สร้างด้วย ASP.NET Core 8.0 สำหรับจัดการข้อมูลผู้ติดต่อ โดยใช้ Entity Framework Core กับ SQLite และมี Swagger สำหรับเอกสาร API

## 🛠️ เทคโนโลยีที่ใช้
- **ASP.NET Core 8.0** - Web Framework
- **Entity Framework Core** - ORM สำหรับจัดการฐานข้อมูล
- **SQLite** - ฐานข้อมูล (ไม่ต้องติดตั้งเพิ่ม)
- **Swagger/OpenAPI** - เอกสารและทดสอบ API
- **C#** - ภาษาโปรแกรม

## 📋 ขั้นตอนการพัฒนา

### 1. การเตรียมเครื่องมือ
```bash
# ตรวจสอบ .NET SDK
dotnet --version

# ตรวจสอบว่ามี .NET 8.0 หรือใหม่กว่า
```

### 2. สร้างโปรเจคใหม่
```bash
# สร้างโฟลเดอร์โปรเจค
mkdir "DevCode/Learn ASP-Net Core/ContactAPI"
cd "DevCode/Learn ASP-Net Core/ContactAPI"

# สร้าง Web API project
dotnet new webapi -n ContactAPI

# เข้าไปในโฟลเดอร์โปรเจค
cd ContactAPI
```

### 3. ติดตั้ง NuGet Packages
```bash
# ติดตั้ง Entity Framework Core packages
dotnet add package Microsoft.EntityFrameworkCore --version 8.0.17
dotnet add package Microsoft.EntityFrameworkCore.Sqlite --version 8.0.17
dotnet add package Microsoft.EntityFrameworkCore.Tools --version 8.0.17
dotnet add package Microsoft.EntityFrameworkCore.Design --version 8.0.17

# ตรวจสอบ packages ที่ติดตั้ง
dotnet list package
```

### 4. สร้างโครงสร้างโฟลเดอร์
```bash
# สร้างโฟลเดอร์สำหรับ Models
mkdir Models

# สร้างโฟลเดอร์สำหรับ Data
mkdir Data

# สร้างโฟลเดอร์สำหรับ DTOs
mkdir DTOs

# สร้างโฟลเดอร์สำหรับ Services
mkdir Services

# สร้างโฟลเดอร์สำหรับ Controllers
mkdir Controllers

# สร้างโฟลเดอร์สำหรับ Postman Collection
mkdir "Postman-Collection"
```

### 5. สร้าง Model (Contact.cs)
```bash
# สร้างไฟล์ Contact.cs ในโฟลเดอร์ Models
```

**เนื้อหาไฟล์ Models/Contact.cs:**
```csharp
using System.ComponentModel.DataAnnotations;

namespace ContactAPI.Models
{
    public class Contact
    {
        public int Id { get; set; }
        
        [Required]
        [StringLength(50)]
        public string FirstName { get; set; } = string.Empty;
        
        [Required]
        [StringLength(50)]
        public string LastName { get; set; } = string.Empty;
        
        [Required]
        [EmailAddress]
        [StringLength(100)]
        public string Email { get; set; } = string.Empty;
        
        [Required]
        [Phone]
        [StringLength(20)]
        public string PhoneNumber { get; set; } = string.Empty;
        
        [StringLength(200)]
        public string? Address { get; set; }
        
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
        
        public string FullName => $"{FirstName} {LastName}".Trim();
    }
}
```

### 6. สร้าง DTOs (Data Transfer Objects)
```bash
# สร้างไฟล์ ContactDto.cs ในโฟลเดอร์ DTOs
```

**เนื้อหาไฟล์ DTOs/ContactDto.cs:**
```csharp
using System.ComponentModel.DataAnnotations;

namespace ContactAPI.DTOs
{
    public class CreateContactDto
    {
        [Required(ErrorMessage = "First name is required")]
        [StringLength(50, ErrorMessage = "First name cannot exceed 50 characters")]
        public string FirstName { get; set; } = string.Empty;
        
        [Required(ErrorMessage = "Last name is required")]
        [StringLength(50, ErrorMessage = "Last name cannot exceed 50 characters")]
        public string LastName { get; set; } = string.Empty;
        
        [Required(ErrorMessage = "Email is required")]
        [EmailAddress(ErrorMessage = "Invalid email format")]
        [StringLength(100, ErrorMessage = "Email cannot exceed 100 characters")]
        public string Email { get; set; } = string.Empty;
        
        [Required(ErrorMessage = "Phone number is required")]
        [Phone(ErrorMessage = "Invalid phone number format")]
        [StringLength(20, ErrorMessage = "Phone number cannot exceed 20 characters")]
        public string PhoneNumber { get; set; } = string.Empty;
        
        [StringLength(200, ErrorMessage = "Address cannot exceed 200 characters")]
        public string? Address { get; set; }
    }
    
    public class UpdateContactDto
    {
        [StringLength(50, ErrorMessage = "First name cannot exceed 50 characters")]
        public string? FirstName { get; set; }
        
        [StringLength(50, ErrorMessage = "Last name cannot exceed 50 characters")]
        public string? LastName { get; set; }
        
        [EmailAddress(ErrorMessage = "Invalid email format")]
        [StringLength(100, ErrorMessage = "Email cannot exceed 100 characters")]
        public string? Email { get; set; }
        
        [Phone(ErrorMessage = "Invalid phone number format")]
        [StringLength(20, ErrorMessage = "Phone number cannot exceed 20 characters")]
        public string? PhoneNumber { get; set; }
        
        [StringLength(200, ErrorMessage = "Address cannot exceed 200 characters")]
        public string? Address { get; set; }
    }
    
    public class ContactResponseDto
    {
        public int Id { get; set; }
        public string FirstName { get; set; } = string.Empty;
        public string LastName { get; set; } = string.Empty;
        public string FullName { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string PhoneNumber { get; set; } = string.Empty;
        public string? Address { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set; }
    }
}
```

### 7. สร้าง Database Context
```bash
# สร้างไฟล์ ContactDbContext.cs ในโฟลเดอร์ Data
```

**เนื้อหาไฟล์ Data/ContactDbContext.cs:**
```csharp
using Microsoft.EntityFrameworkCore;
using ContactAPI.Models;

namespace ContactAPI.Data
{
    public class ContactDbContext : DbContext
    {
        public ContactDbContext(DbContextOptions<ContactDbContext> options) : base(options)
        {
        }
        
        public DbSet<Contact> Contacts { get; set; }
        
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            
            modelBuilder.Entity<Contact>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Id).ValueGeneratedOnAdd();
                entity.HasIndex(e => e.Email).IsUnique();
                
                entity.Property(e => e.FirstName).IsRequired().HasMaxLength(50);
                entity.Property(e => e.LastName).IsRequired().HasMaxLength(50);
                entity.Property(e => e.Email).IsRequired().HasMaxLength(100);
                entity.Property(e => e.PhoneNumber).IsRequired().HasMaxLength(20);
                entity.Property(e => e.Address).HasMaxLength(200);
                
                entity.Property(e => e.CreatedAt).HasDefaultValueSql("CURRENT_TIMESTAMP");
                entity.Property(e => e.UpdatedAt).HasDefaultValueSql("CURRENT_TIMESTAMP");
            });
            
            // Seed data
            modelBuilder.Entity<Contact>().HasData(
                new Contact
                {
                    Id = 1,
                    FirstName = "John",
                    LastName = "Doe",
                    Email = "john.doe@example.com",
                    PhoneNumber = "+1234567890",
                    Address = "123 Main St, City, State 12345",
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                },
                new Contact
                {
                    Id = 2,
                    FirstName = "Jane",
                    LastName = "Smith",
                    Email = "jane.smith@example.com",
                    PhoneNumber = "+0987654321",
                    Address = "456 Oak Ave, Town, State 67890",
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                }
            );
        }
    }
}
```

### 8. สร้าง Service Interface
```bash
# สร้างไฟล์ IContactService.cs ในโฟลเดอร์ Services
```

**เนื้อหาไฟล์ Services/IContactService.cs:**
```csharp
using ContactAPI.DTOs;

namespace ContactAPI.Services
{
    public interface IContactService
    {
        Task<IEnumerable<ContactResponseDto>> GetAllContactsAsync(string? searchTerm = null, int page = 1, int pageSize = 10);
        Task<ContactResponseDto?> GetContactByIdAsync(int id);
        Task<ContactResponseDto?> GetContactByEmailAsync(string email);
        Task<ContactResponseDto> CreateContactAsync(CreateContactDto createContactDto);
        Task<ContactResponseDto?> UpdateContactAsync(int id, UpdateContactDto updateContactDto);
        Task<bool> DeleteContactAsync(int id);
        Task<bool> ContactExistsByEmailAsync(string email, int? excludeId = null);
    }
}
```

### 9. สร้าง Service Implementation
```bash
# สร้างไฟล์ ContactService.cs ในโฟลเดอร์ Services
```

**เนื้อหาไฟล์ Services/ContactService.cs:**
```csharp
using Microsoft.EntityFrameworkCore;
using ContactAPI.Data;
using ContactAPI.DTOs;
using ContactAPI.Models;

namespace ContactAPI.Services
{
    public class ContactService : IContactService
    {
        private readonly ContactDbContext _context;
        
        public ContactService(ContactDbContext context)
        {
            _context = context;
        }
        
        public async Task<IEnumerable<ContactResponseDto>> GetAllContactsAsync(string? searchTerm = null, int page = 1, int pageSize = 10)
        {
            var query = _context.Contacts.AsQueryable();
            
            if (!string.IsNullOrWhiteSpace(searchTerm))
            {
                query = query.Where(c => 
                    c.FirstName.Contains(searchTerm) || 
                    c.LastName.Contains(searchTerm) || 
                    c.Email.Contains(searchTerm) ||
                    c.PhoneNumber.Contains(searchTerm) ||
                    (c.Address != null && c.Address.Contains(searchTerm))
                );
            }
            
            var skip = (page - 1) * pageSize;
            var contacts = await query
                .OrderBy(c => c.FirstName)
                .ThenBy(c => c.LastName)
                .Skip(skip)
                .Take(pageSize)
                .ToListAsync();
            
            return contacts.Select(MapToResponseDto);
        }
        
        public async Task<ContactResponseDto?> GetContactByIdAsync(int id)
        {
            var contact = await _context.Contacts.FindAsync(id);
            return contact != null ? MapToResponseDto(contact) : null;
        }
        
        public async Task<ContactResponseDto?> GetContactByEmailAsync(string email)
        {
            var contact = await _context.Contacts
                .FirstOrDefaultAsync(c => c.Email.ToLower() == email.ToLower());
            return contact != null ? MapToResponseDto(contact) : null;
        }
        
        public async Task<ContactResponseDto> CreateContactAsync(CreateContactDto createContactDto)
        {
            if (await ContactExistsByEmailAsync(createContactDto.Email))
            {
                throw new InvalidOperationException($"Contact with email '{createContactDto.Email}' already exists.");
            }
            
            var contact = new Contact
            {
                FirstName = createContactDto.FirstName,
                LastName = createContactDto.LastName,
                Email = createContactDto.Email,
                PhoneNumber = createContactDto.PhoneNumber,
                Address = createContactDto.Address,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };
            
            _context.Contacts.Add(contact);
            await _context.SaveChangesAsync();
            
            return MapToResponseDto(contact);
        }
        
        public async Task<ContactResponseDto?> UpdateContactAsync(int id, UpdateContactDto updateContactDto)
        {
            var contact = await _context.Contacts.FindAsync(id);
            if (contact == null)
                return null;
            
            if (!string.IsNullOrEmpty(updateContactDto.Email) && 
                await ContactExistsByEmailAsync(updateContactDto.Email, id))
            {
                throw new InvalidOperationException($"Contact with email '{updateContactDto.Email}' already exists.");
            }
            
            if (!string.IsNullOrEmpty(updateContactDto.FirstName))
                contact.FirstName = updateContactDto.FirstName;
            
            if (!string.IsNullOrEmpty(updateContactDto.LastName))
                contact.LastName = updateContactDto.LastName;
            
            if (!string.IsNullOrEmpty(updateContactDto.Email))
                contact.Email = updateContactDto.Email;
            
            if (!string.IsNullOrEmpty(updateContactDto.PhoneNumber))
                contact.PhoneNumber = updateContactDto.PhoneNumber;
            
            if (updateContactDto.Address != null)
                contact.Address = updateContactDto.Address;
            
            contact.UpdatedAt = DateTime.UtcNow;
            
            await _context.SaveChangesAsync();
            
            return MapToResponseDto(contact);
        }
        
        public async Task<bool> DeleteContactAsync(int id)
        {
            var contact = await _context.Contacts.FindAsync(id);
            if (contact == null)
                return false;
            
            _context.Contacts.Remove(contact);
            await _context.SaveChangesAsync();
            
            return true;
        }
        
        public async Task<bool> ContactExistsByEmailAsync(string email, int? excludeId = null)
        {
            var query = _context.Contacts.Where(c => c.Email.ToLower() == email.ToLower());
            
            if (excludeId.HasValue)
                query = query.Where(c => c.Id != excludeId.Value);
            
            return await query.AnyAsync();
        }
        
        private static ContactResponseDto MapToResponseDto(Contact contact)
        {
            return new ContactResponseDto
            {
                Id = contact.Id,
                FirstName = contact.FirstName,
                LastName = contact.LastName,
                FullName = contact.FullName,
                Email = contact.Email,
                PhoneNumber = contact.PhoneNumber,
                Address = contact.Address,
                CreatedAt = contact.CreatedAt,
                UpdatedAt = contact.UpdatedAt
            };
        }
    }
}
```

### 10. สร้าง Controller
```bash
# สร้างไฟล์ ContactsController.cs ในโฟลเดอร์ Controllers
```

**เนื้อหาไฟล์ Controllers/ContactsController.cs:**
```csharp
using Microsoft.AspNetCore.Mvc;
using ContactAPI.DTOs;
using ContactAPI.Services;

namespace ContactAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Produces("application/json")]
    public class ContactsController : ControllerBase
    {
        private readonly IContactService _contactService;
        
        public ContactsController(IContactService contactService)
        {
            _contactService = contactService;
        }
        
        [HttpGet]
        [ProducesResponseType(typeof(IEnumerable<ContactResponseDto>), 200)]
        [ProducesResponseType(400)]
        public async Task<ActionResult<IEnumerable<ContactResponseDto>>> GetContacts(
            [FromQuery] string? search = null,
            [FromQuery] int page = 1,
            [FromQuery] int pageSize = 10)
        {
            if (page < 1)
                return BadRequest("Page number must be greater than 0");
            
            if (pageSize < 1 || pageSize > 100)
                return BadRequest("Page size must be between 1 and 100");
            
            var contacts = await _contactService.GetAllContactsAsync(search, page, pageSize);
            return Ok(contacts);
        }
        
        [HttpGet("{id}")]
        [ProducesResponseType(typeof(ContactResponseDto), 200)]
        [ProducesResponseType(404)]
        public async Task<ActionResult<ContactResponseDto>> GetContact(int id)
        {
            var contact = await _contactService.GetContactByIdAsync(id);
            
            if (contact == null)
                return NotFound($"Contact with ID {id} not found");
            
            return Ok(contact);
        }
        
        [HttpGet("email/{email}")]
        [ProducesResponseType(typeof(ContactResponseDto), 200)]
        [ProducesResponseType(404)]
        public async Task<ActionResult<ContactResponseDto>> GetContactByEmail(string email)
        {
            var contact = await _contactService.GetContactByEmailAsync(email);
            
            if (contact == null)
                return NotFound($"Contact with email '{email}' not found");
            
            return Ok(contact);
        }
        
        [HttpPost]
        [ProducesResponseType(typeof(ContactResponseDto), 201)]
        [ProducesResponseType(400)]
        [ProducesResponseType(409)]
        public async Task<ActionResult<ContactResponseDto>> CreateContact(CreateContactDto createContactDto)
        {
            try
            {
                var contact = await _contactService.CreateContactAsync(createContactDto);
                return CreatedAtAction(nameof(GetContact), new { id = contact.Id }, contact);
            }
            catch (InvalidOperationException ex)
            {
                return Conflict(ex.Message);
            }
        }
        
        [HttpPut("{id}")]
        [ProducesResponseType(typeof(ContactResponseDto), 200)]
        [ProducesResponseType(400)]
        [ProducesResponseType(404)]
        [ProducesResponseType(409)]
        public async Task<ActionResult<ContactResponseDto>> UpdateContact(int id, UpdateContactDto updateContactDto)
        {
            try
            {
                var contact = await _contactService.UpdateContactAsync(id, updateContactDto);
                
                if (contact == null)
                    return NotFound($"Contact with ID {id} not found");
                
                return Ok(contact);
            }
            catch (InvalidOperationException ex)
            {
                return Conflict(ex.Message);
            }
        }
        
        [HttpDelete("{id}")]
        [ProducesResponseType(204)]
        [ProducesResponseType(404)]
        public async Task<IActionResult> DeleteContact(int id)
        {
            var deleted = await _contactService.DeleteContactAsync(id);
            
            if (!deleted)
                return NotFound($"Contact with ID {id} not found");
            
            return NoContent();
        }
        
        [HttpGet("health")]
        [ProducesResponseType(200)]
        public ActionResult<string> Health()
        {
            return Ok("Contact API is running!");
        }
    }
}
```

### 11. ตั้งค่า Configuration
```bash
# แก้ไขไฟล์ appsettings.json
```

**เนื้อหาไฟล์ appsettings.json:**
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Data Source=ContactAPI.db"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

### 12. ตั้งค่า Program.cs
```bash
# แก้ไขไฟล์ Program.cs
```

**เนื้อหาไฟล์ Program.cs:**
```csharp
using Microsoft.EntityFrameworkCore;
using ContactAPI.Data;
using ContactAPI.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();

// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new Microsoft.OpenApi.Models.OpenApiInfo
    {
        Title = "Contact API",
        Version = "v1",
        Description = "A simple API for managing contacts",
        Contact = new Microsoft.OpenApi.Models.OpenApiContact
        {
            Name = "Contact API Support",
            Email = "support@contactapi.com"
        }
    });
});

// Add Entity Framework Core with SQLite
builder.Services.AddDbContext<ContactDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));

// Add services
builder.Services.AddScoped<IContactService, ContactService>();

// Add CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "Contact API V1");
        c.RoutePrefix = string.Empty; // Set Swagger UI at root URL
    });
}

app.UseHttpsRedirection();

// Use CORS
app.UseCors("AllowAll");

app.UseAuthorization();

app.MapControllers();

// Ensure database is created
using (var scope = app.Services.CreateScope())
{
    var context = scope.ServiceProvider.GetRequiredService<ContactDbContext>();
    context.Database.EnsureCreated();
}

app.Run();
```

### 13. ตั้งค่า Port และ Launch Settings
```bash
# แก้ไขไฟล์ Properties/launchSettings.json
```

**เนื้อหาไฟล์ Properties/launchSettings.json:**
```json
{
  "$schema": "http://json.schemastore.org/launchsettings.json",
  "iisSettings": {
    "windowsAuthentication": false,
    "anonymousAuthentication": true,
    "iisExpress": {
      "applicationUrl": "http://localhost:5001",
      "sslPort": 7001
    }
  },
  "profiles": {
    "ContactAPI": {
      "commandName": "Project",
      "dotnetRunMessages": true,
      "launchBrowser": true,
      "launchUrl": "",
      "applicationUrl": "https://localhost:7001;http://localhost:5001",
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      }
    },
    "IIS Express": {
      "commandName": "IISExpress",
      "launchBrowser": true,
      "launchUrl": "",
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      }
    }
  }
}
```

### 14. ทดสอบและรันโปรเจค
```bash
# Restore dependencies
dotnet restore

# Build project
dotnet build

# Run project
dotnet run
```

### 15. สร้างไฟล์เอกสาร
```bash
# สร้างไฟล์ README.md
# สร้างไฟล์ PROJECT_SUMMARY.md
# สร้างไฟล์ test-api.ps1
```

### 16. สร้าง Postman Collection และ Environment
```bash
# สร้างไฟล์ Postman-Collection/ContactAPI.postman_collection.json
# สร้างไฟล์ Postman-Collection/ContactAPI.postman_environment.json
# สร้างไฟล์ Postman-Collection/README.md
```

## 🚀 คำสั่งที่ใช้บ่อย

### การพัฒนา
```bash
# รันโปรเจค
dotnet run

# รันในโหมด watch (auto-reload)
dotnet watch run

# Build โปรเจค
dotnet build

# Clean โปรเจค
dotnet clean

# Restore packages
dotnet restore
```

### การจัดการ Database
```bash
# สร้าง migration
dotnet ef migrations add InitialCreate

# อัพเดท database
dotnet ef database update

# ลบ migration ล่าสุด
dotnet ef migrations remove

# ดูรายการ migrations
dotnet ef migrations list
```

### การทดสอบ
```bash
# รัน unit tests
dotnet test

# รันเฉพาะ test project
dotnet test --project Tests/ContactAPI.Tests
```

### การ Deploy
```bash
# Publish สำหรับ production
dotnet publish -c Release

# Publish สำหรับ specific runtime
dotnet publish -c Release -r win-x64 --self-contained
```

## 📁 โครงสร้างไฟล์สุดท้าย
```
ContactAPI/
├── Controllers/
│   └── ContactsController.cs
├── Data/
│   └── ContactDbContext.cs
├── DTOs/
│   └── ContactDto.cs
├── Models/
│   └── Contact.cs
├── Services/
│   ├── IContactService.cs
│   └── ContactService.cs
├── Postman-Collection/
│   ├── ContactAPI.postman_collection.json
│   ├── ContactAPI.postman_environment.json
│   └── README.md
├── Properties/
│   └── launchSettings.json
├── Program.cs
├── appsettings.json
├── ContactAPI.csproj
├── README.md
├── PROJECT_SUMMARY.md
├── test-api.ps1
└── Des-Code.md
```

## 🎯 สรุปขั้นตอนสำคัญ

1. **เตรียมเครื่องมือ** - ติดตั้ง .NET 8.0 SDK
2. **สร้างโปรเจค** - ใช้ `dotnet new webapi`
3. **ติดตั้ง Packages** - Entity Framework Core และ SQLite
4. **สร้าง Models** - Contact entity
5. **สร้าง DTOs** - Request/Response objects
6. **สร้าง Database Context** - EF Core configuration
7. **สร้าง Services** - Business logic layer
8. **สร้าง Controllers** - API endpoints
9. **ตั้งค่า Configuration** - Database connection
10. **ตั้งค่า Program.cs** - Dependency injection
11. **ตั้งค่า Port** - Launch settings
12. **ทดสอบ** - รันและทดสอบ API
13. **สร้างเอกสาร** - README และ guides
14. **สร้าง Postman Collection** - สำหรับทดสอบ

## 🔧 การแก้ไขปัญหา

### ปัญหาที่พบบ่อย
1. **SQL Server ไม่ติดตั้ง** - เปลี่ยนเป็น SQLite
2. **Port ถูกใช้งาน** - เปลี่ยน port ใน launchSettings.json
3. **Database ไม่สร้าง** - ตรวจสอบ connection string
4. **Swagger ไม่แสดง** - ตรวจสอบ Program.cs configuration

### คำสั่งแก้ไขปัญหา
```bash
# ลบ database และสร้างใหม่
rm ContactAPI.db
dotnet run

# Clear cache
dotnet clean
dotnet restore

# Reset EF Core
dotnet ef database drop
dotnet ef database update
```

---

**🎉 โปรเจค Contact API พร้อมใช้งาน!** 