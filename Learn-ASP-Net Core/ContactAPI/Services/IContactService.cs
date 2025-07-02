using ContactAPI.DTOs;
using ContactAPI.Models;

namespace ContactAPI.Services
{
    /// <summary>
    /// Interface for contact management operations
    /// </summary>
    public interface IContactService
    {
        /// <summary>
        /// Get all contacts with optional search and pagination
        /// </summary>
        /// <param name="searchTerm">Optional search term for filtering contacts</param>
        /// <param name="page">Page number for pagination</param>
        /// <param name="pageSize">Number of items per page</param>
        /// <returns>List of contacts</returns>
        Task<IEnumerable<ContactResponseDto>> GetAllContactsAsync(string? searchTerm = null, int page = 1, int pageSize = 10);

        /// <summary>
        /// Get a contact by its ID
        /// </summary>
        /// <param name="id">Contact ID</param>
        /// <returns>Contact if found, null otherwise</returns>
        Task<ContactResponseDto?> GetContactByIdAsync(int id);

        /// <summary>
        /// Get a contact by email address
        /// </summary>
        /// <param name="email">Email address</param>
        /// <returns>Contact if found, null otherwise</returns>
        Task<ContactResponseDto?> GetContactByEmailAsync(string email);

        /// <summary>
        /// Create a new contact
        /// </summary>
        /// <param name="createContactDto">Contact data</param>
        /// <returns>Created contact</returns>
        Task<ContactResponseDto> CreateContactAsync(CreateContactDto createContactDto);

        /// <summary>
        /// Update an existing contact
        /// </summary>
        /// <param name="id">Contact ID</param>
        /// <param name="updateContactDto">Updated contact data</param>
        /// <returns>Updated contact if found, null otherwise</returns>
        Task<ContactResponseDto?> UpdateContactAsync(int id, UpdateContactDto updateContactDto);

        /// <summary>
        /// Delete a contact
        /// </summary>
        /// <param name="id">Contact ID</param>
        /// <returns>True if deleted, false if not found</returns>
        Task<bool> DeleteContactAsync(int id);

        /// <summary>
        /// Check if a contact exists by email
        /// </summary>
        /// <param name="email">Email address</param>
        /// <param name="excludeId">Contact ID to exclude from check (for updates)</param>
        /// <returns>True if contact exists, false otherwise</returns>
        Task<bool> ContactExistsByEmailAsync(string email, int? excludeId = null);
    }
} 