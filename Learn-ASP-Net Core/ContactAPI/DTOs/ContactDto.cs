using System.ComponentModel.DataAnnotations;

namespace ContactAPI.DTOs
{
    /// <summary>
    /// Data Transfer Object for creating a new contact
    /// </summary>
    public class CreateContactDto
    {
        /// <summary>
        /// First name of the contact
        /// </summary>
        [Required(ErrorMessage = "First name is required")]
        [StringLength(50, ErrorMessage = "First name cannot exceed 50 characters")]
        public string FirstName { get; set; } = string.Empty;

        /// <summary>
        /// Last name of the contact
        /// </summary>
        [Required(ErrorMessage = "Last name is required")]
        [StringLength(50, ErrorMessage = "Last name cannot exceed 50 characters")]
        public string LastName { get; set; } = string.Empty;

        /// <summary>
        /// Email address of the contact
        /// </summary>
        [Required(ErrorMessage = "Email is required")]
        [EmailAddress(ErrorMessage = "Invalid email format")]
        [StringLength(100, ErrorMessage = "Email cannot exceed 100 characters")]
        public string Email { get; set; } = string.Empty;

        /// <summary>
        /// Phone number of the contact
        /// </summary>
        [Required(ErrorMessage = "Phone number is required")]
        [Phone(ErrorMessage = "Invalid phone number format")]
        [StringLength(20, ErrorMessage = "Phone number cannot exceed 20 characters")]
        public string PhoneNumber { get; set; } = string.Empty;

        /// <summary>
        /// Address of the contact (optional)
        /// </summary>
        [StringLength(200, ErrorMessage = "Address cannot exceed 200 characters")]
        public string? Address { get; set; }
    }

    /// <summary>
    /// Data Transfer Object for updating an existing contact
    /// </summary>
    public class UpdateContactDto
    {
        /// <summary>
        /// First name of the contact
        /// </summary>
        [StringLength(50, ErrorMessage = "First name cannot exceed 50 characters")]
        public string? FirstName { get; set; }

        /// <summary>
        /// Last name of the contact
        /// </summary>
        [StringLength(50, ErrorMessage = "Last name cannot exceed 50 characters")]
        public string? LastName { get; set; }

        /// <summary>
        /// Email address of the contact
        /// </summary>
        [EmailAddress(ErrorMessage = "Invalid email format")]
        [StringLength(100, ErrorMessage = "Email cannot exceed 100 characters")]
        public string? Email { get; set; }

        /// <summary>
        /// Phone number of the contact
        /// </summary>
        [Phone(ErrorMessage = "Invalid phone number format")]
        [StringLength(20, ErrorMessage = "Phone number cannot exceed 20 characters")]
        public string? PhoneNumber { get; set; }

        /// <summary>
        /// Address of the contact
        /// </summary>
        [StringLength(200, ErrorMessage = "Address cannot exceed 200 characters")]
        public string? Address { get; set; }
    }

    /// <summary>
    /// Data Transfer Object for contact response
    /// </summary>
    public class ContactResponseDto
    {
        /// <summary>
        /// Unique identifier for the contact
        /// </summary>
        public int Id { get; set; }

        /// <summary>
        /// First name of the contact
        /// </summary>
        public string FirstName { get; set; } = string.Empty;

        /// <summary>
        /// Last name of the contact
        /// </summary>
        public string LastName { get; set; } = string.Empty;

        /// <summary>
        /// Full name of the contact
        /// </summary>
        public string FullName { get; set; } = string.Empty;

        /// <summary>
        /// Email address of the contact
        /// </summary>
        public string Email { get; set; } = string.Empty;

        /// <summary>
        /// Phone number of the contact
        /// </summary>
        public string PhoneNumber { get; set; } = string.Empty;

        /// <summary>
        /// Address of the contact
        /// </summary>
        public string? Address { get; set; }

        /// <summary>
        /// Date when the contact was created
        /// </summary>
        public DateTime CreatedAt { get; set; }

        /// <summary>
        /// Date when the contact was last updated
        /// </summary>
        public DateTime UpdatedAt { get; set; }
    }
} 