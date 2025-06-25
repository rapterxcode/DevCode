using Microsoft.AspNetCore.Mvc;
using ContactAPI.DTOs;
using ContactAPI.Services;

namespace ContactAPI.Controllers
{
    /// <summary>
    /// Controller for managing contacts
    /// </summary>
    [ApiController]
    [Route("api/[controller]")]
    [Produces("application/json")]
    public class ContactsController : ControllerBase
    {
        private readonly IContactService _contactService;

        /// <summary>
        /// Constructor with contact service dependency injection
        /// </summary>
        /// <param name="contactService">Contact service</param>
        public ContactsController(IContactService contactService)
        {
            _contactService = contactService;
        }

        /// <summary>
        /// Get all contacts with optional search and pagination
        /// </summary>
        /// <param name="search">Optional search term to filter contacts</param>
        /// <param name="page">Page number (default: 1)</param>
        /// <param name="pageSize">Number of items per page (default: 10, max: 100)</param>
        /// <returns>List of contacts</returns>
        /// <response code="200">Returns the list of contacts</response>
        /// <response code="400">If page or pageSize parameters are invalid</response>
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

        /// <summary>
        /// Get a specific contact by ID
        /// </summary>
        /// <param name="id">Contact ID</param>
        /// <returns>Contact details</returns>
        /// <response code="200">Returns the contact</response>
        /// <response code="404">If the contact is not found</response>
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

        /// <summary>
        /// Get a contact by email address
        /// </summary>
        /// <param name="email">Email address</param>
        /// <returns>Contact details</returns>
        /// <response code="200">Returns the contact</response>
        /// <response code="404">If the contact is not found</response>
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

        /// <summary>
        /// Create a new contact
        /// </summary>
        /// <param name="createContactDto">Contact data</param>
        /// <returns>Created contact</returns>
        /// <response code="201">Contact created successfully</response>
        /// <response code="400">If the contact data is invalid</response>
        /// <response code="409">If a contact with the same email already exists</response>
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

        /// <summary>
        /// Update an existing contact
        /// </summary>
        /// <param name="id">Contact ID</param>
        /// <param name="updateContactDto">Updated contact data</param>
        /// <returns>Updated contact</returns>
        /// <response code="200">Contact updated successfully</response>
        /// <response code="400">If the contact data is invalid</response>
        /// <response code="404">If the contact is not found</response>
        /// <response code="409">If a contact with the same email already exists</response>
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

        /// <summary>
        /// Delete a contact
        /// </summary>
        /// <param name="id">Contact ID</param>
        /// <returns>No content</returns>
        /// <response code="204">Contact deleted successfully</response>
        /// <response code="404">If the contact is not found</response>
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

        /// <summary>
        /// Health check endpoint
        /// </summary>
        /// <returns>Health status</returns>
        /// <response code="200">API is healthy</response>
        [HttpGet("health")]
        [ProducesResponseType(200)]
        public ActionResult<string> Health()
        {
            return Ok("Contact API is running!");
        }
    }
} 