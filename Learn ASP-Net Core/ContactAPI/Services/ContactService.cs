using Microsoft.EntityFrameworkCore;
using ContactAPI.Data;
using ContactAPI.DTOs;
using ContactAPI.Models;

namespace ContactAPI.Services
{
    /// <summary>
    /// Service for managing contact operations
    /// </summary>
    public class ContactService : IContactService
    {
        private readonly ContactDbContext _context;

        /// <summary>
        /// Constructor with database context dependency injection
        /// </summary>
        /// <param name="context">Database context</param>
        public ContactService(ContactDbContext context)
        {
            _context = context;
        }

        /// <summary>
        /// Get all contacts with optional search and pagination
        /// </summary>
        public async Task<IEnumerable<ContactResponseDto>> GetAllContactsAsync(string? searchTerm = null, int page = 1, int pageSize = 10)
        {
            var query = _context.Contacts.AsQueryable();

            // Apply search filter if provided
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

            // Apply pagination
            var skip = (page - 1) * pageSize;
            var contacts = await query
                .OrderBy(c => c.FirstName)
                .ThenBy(c => c.LastName)
                .Skip(skip)
                .Take(pageSize)
                .ToListAsync();

            return contacts.Select(MapToResponseDto);
        }

        /// <summary>
        /// Get a contact by its ID
        /// </summary>
        public async Task<ContactResponseDto?> GetContactByIdAsync(int id)
        {
            var contact = await _context.Contacts.FindAsync(id);
            return contact != null ? MapToResponseDto(contact) : null;
        }

        /// <summary>
        /// Get a contact by email address
        /// </summary>
        public async Task<ContactResponseDto?> GetContactByEmailAsync(string email)
        {
            var contact = await _context.Contacts
                .FirstOrDefaultAsync(c => c.Email.ToLower() == email.ToLower());
            return contact != null ? MapToResponseDto(contact) : null;
        }

        /// <summary>
        /// Create a new contact
        /// </summary>
        public async Task<ContactResponseDto> CreateContactAsync(CreateContactDto createContactDto)
        {
            // Check if email already exists
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

        /// <summary>
        /// Update an existing contact
        /// </summary>
        public async Task<ContactResponseDto?> UpdateContactAsync(int id, UpdateContactDto updateContactDto)
        {
            var contact = await _context.Contacts.FindAsync(id);
            if (contact == null)
                return null;

            // Check if email already exists (excluding current contact)
            if (!string.IsNullOrEmpty(updateContactDto.Email) && 
                await ContactExistsByEmailAsync(updateContactDto.Email, id))
            {
                throw new InvalidOperationException($"Contact with email '{updateContactDto.Email}' already exists.");
            }

            // Update only provided fields
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

        /// <summary>
        /// Delete a contact
        /// </summary>
        public async Task<bool> DeleteContactAsync(int id)
        {
            var contact = await _context.Contacts.FindAsync(id);
            if (contact == null)
                return false;

            _context.Contacts.Remove(contact);
            await _context.SaveChangesAsync();

            return true;
        }

        /// <summary>
        /// Check if a contact exists by email
        /// </summary>
        public async Task<bool> ContactExistsByEmailAsync(string email, int? excludeId = null)
        {
            var query = _context.Contacts.Where(c => c.Email.ToLower() == email.ToLower());
            
            if (excludeId.HasValue)
                query = query.Where(c => c.Id != excludeId.Value);

            return await query.AnyAsync();
        }

        /// <summary>
        /// Map Contact entity to ContactResponseDto
        /// </summary>
        /// <param name="contact">Contact entity</param>
        /// <returns>ContactResponseDto</returns>
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