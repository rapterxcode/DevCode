using Microsoft.EntityFrameworkCore;
using ContactAPI.Models;

namespace ContactAPI.Data
{
    /// <summary>
    /// Database context for Contact API
    /// </summary>
    public class ContactDbContext : DbContext
    {
        /// <summary>
        /// Constructor with DbContext options
        /// </summary>
        /// <param name="options">Database context options</param>
        public ContactDbContext(DbContextOptions<ContactDbContext> options) : base(options)
        {
        }

        /// <summary>
        /// Contacts table in the database
        /// </summary>
        public DbSet<Contact> Contacts { get; set; }

        /// <summary>
        /// Configure the model when it's being created
        /// </summary>
        /// <param name="modelBuilder">Model builder instance</param>
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configure Contact entity
            modelBuilder.Entity<Contact>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Id).ValueGeneratedOnAdd();
                
                // Make email unique
                entity.HasIndex(e => e.Email).IsUnique();
                
                // Configure required fields
                entity.Property(e => e.FirstName).IsRequired().HasMaxLength(50);
                entity.Property(e => e.LastName).IsRequired().HasMaxLength(50);
                entity.Property(e => e.Email).IsRequired().HasMaxLength(100);
                entity.Property(e => e.PhoneNumber).IsRequired().HasMaxLength(20);
                entity.Property(e => e.Address).HasMaxLength(200);
                
                // Configure timestamps for SQLite
                entity.Property(e => e.CreatedAt).HasDefaultValueSql("CURRENT_TIMESTAMP");
                entity.Property(e => e.UpdatedAt).HasDefaultValueSql("CURRENT_TIMESTAMP");
            });

            // Seed some initial data
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