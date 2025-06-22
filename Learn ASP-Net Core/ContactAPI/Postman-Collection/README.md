# 📮 Postman Setup Guide for Contact API

This guide explains how to set up and use the Postman collection and environment for testing the Contact API.

## 🚀 Quick Setup

### 1. Import Environment
1. Open Postman
2. Click **Import** button
3. Select **`ContactAPI.postman_environment.json`**
4. Click **Import**

### 2. Import Collection
1. Click **Import** button again
2. Select **`ContactAPI.postman_collection.json`**
3. Click **Import**

### 3. Select Environment
1. In the top-right corner, select **"Contact API Environment"** from the dropdown
2. Verify the environment is active (should show a checkmark)

## 🔧 Environment Variables

The environment includes the following variables:

### Base Configuration
- **`baseUrl`**: `https://localhost:7001` - API base URL
- **`apiVersion`**: `v1` - API version
- **`contentType`**: `application/json` - Content type for requests

### Sample Data
- **`contactId`**: `1` - Default contact ID for testing
- **`sampleEmail`**: `john.doe@example.com` - Sample email
- **`sampleFirstName`**: `John` - Sample first name
- **`sampleLastName`**: `Doe` - Sample last name
- **`samplePhoneNumber`**: `+1234567890` - Sample phone number
- **`sampleAddress`**: `123 Main St, City, State 12345` - Sample address

### Test Data
- **`testEmail`**: `test.user@example.com` - Test email
- **`testFirstName`**: `Test` - Test first name
- **`testLastName`**: `User` - Test last name
- **`testPhoneNumber`**: `+1234567890` - Test phone number
- **`testAddress`**: `123 Test St, Test City, TS 12345` - Test address

### Pagination
- **`searchTerm`**: `john` - Default search term
- **`pageNumber`**: `1` - Default page number
- **`pageSize`**: `10` - Default page size

### Dynamic Variables
- **`createdContactId`**: Empty - Will be populated after creating a contact
- **`authToken`**: Empty - For future authentication (disabled)

## 📋 Available Requests

### Health & Status
- **Health Check** - Verify API is running

### Read Operations
- **Get All Contacts** - Retrieve all contacts
- **Get All Contacts with Search** - Search with pagination
- **Get Contact by ID** - Get specific contact
- **Get Contact by Email** - Get contact by email

### Create Operations
- **Create Contact** - Create with all fields
- **Create Contact (Minimal)** - Create with required fields only

### Update Operations
- **Update Contact (Full)** - Update all fields
- **Update Contact (Partial)** - Update specific fields only

### Delete Operations
- **Delete Contact** - Delete a contact

### Error Testing
- **Create Contact - Invalid Email** - Test validation
- **Create Contact - Duplicate Email** - Test conflicts
- **Get Contact - Not Found** - Test 404 errors

## 🧪 Testing Workflow

### 1. Health Check
Start by running the **Health Check** to ensure the API is running.

### 2. Get Existing Data
Run **Get All Contacts** to see the seeded sample data.

### 3. Create New Contact
Use **Create Contact** or **Create Contact (Minimal)** to add new contacts.

### 4. Read Operations
Test **Get Contact by ID** and **Get Contact by Email** with the created data.

### 5. Update Operations
Use **Update Contact** requests to modify existing contacts.

### 6. Search & Pagination
Test **Get All Contacts with Search** to see filtering and pagination.

### 7. Delete Operations
Finally, test **Delete Contact** to remove contacts.

### 8. Error Scenarios
Run the error test requests to verify proper error handling.

## 🔄 Dynamic Variable Usage

### Setting Created Contact ID
After creating a contact, you can manually set the `createdContactId` variable:

1. Run a **Create Contact** request
2. Copy the returned `id` from the response
3. Go to **Environments** → **Contact API Environment**
4. Set `createdContactId` to the copied value
5. Use `{{createdContactId}}` in subsequent requests

### Example Response
```json
{
  "id": 3,
  "firstName": "Test",
  "lastName": "User",
  "fullName": "Test User",
  "email": "test.user@example.com",
  "phoneNumber": "+1234567890",
  "address": "123 Test St, Test City, TS 12345",
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-01-01T00:00:00.000Z"
}
```

## 🎯 Tips for Testing

### 1. Environment Selection
Always ensure the **"Contact API Environment"** is selected before running requests.

### 2. Variable Updates
Update environment variables as needed for different test scenarios.

### 3. Response Validation
Check response status codes and body content for proper API behavior.

### 4. Error Handling
Verify that error requests return appropriate HTTP status codes and error messages.

### 5. Data Consistency
Ensure that created, updated, and deleted data is consistent across requests.

## 🚨 Troubleshooting

### Common Issues

1. **Connection Refused**
   - Ensure the API is running on `https://localhost:7001`
   - Check if the port is correct in the environment

2. **Variable Not Found**
   - Verify the environment is selected
   - Check variable names for typos

3. **SSL Certificate Issues**
   - Accept the self-signed certificate in your browser first
   - Or use `http://localhost:5001` for HTTP testing

4. **Database Issues**
   - Ensure the SQLite database is created
   - Check if sample data is seeded

## 📞 Support

If you encounter issues:
1. Check the API logs for errors
2. Verify the environment variables
3. Ensure the API is running
4. Test with Swagger UI as an alternative

---

**Happy Testing! 🎉** 