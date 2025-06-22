using System.ComponentModel.DataAnnotations;

namespace ContactAPI.Models
{
    /// <summary>
    /// Represents a contact in the address book
    /// </summary>
    public class Contact
    {
        /// <summary>
        /// Unique identifier for the contact
        /// </summary>
        public int Id { get; set; }

        /// <summary>
        /// First name of the contact
        /// </summary>
        [Required]
        [StringLength(50)]
        public string FirstName { get; set; } = string.Empty;

        /// <summary>
        /// Last name of the contact
        /// </summary>
        [Required]
        [StringLength(50)]
        public string LastName { get; set; } = string.Empty;

        /// <summary>
        /// Email address of the contact
        /// </summary>
        [Required]
        [EmailAddress]
        [StringLength(100)]
        public string Email { get; set; } = string.Empty;

        /// <summary>
        /// Phone number of the contact
        /// </summary>
        [Required]
        [Phone]
        [StringLength(20)]
        public string PhoneNumber { get; set; } = string.Empty;

        /// <summary>
        /// Address of the contact (optional)
        /// </summary>
        [StringLength(200)]
        public string? Address { get; set; }

        /// <summary>
        /// Date when the contact was created
        /// </summary>
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Date when the contact was last updated
        /// </summary>
        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

        /// <summary>
        /// Full name of the contact (computed property)
        /// </summary>
        public string FullName => $"{FirstName} {LastName}".Trim();
    }
} 