# Contact API Test Script
# This script tests the Contact API endpoints

Write-Host "🚀 Testing Contact API..." -ForegroundColor Green
Write-Host ""

# Base URL
$baseUrl = "https://localhost:7001"

# Test 1: Health Check
Write-Host "1. Testing Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/contacts/health" -Method GET
    Write-Host "   ✅ Health Check: $response" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Health Check Failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 2: Get All Contacts
Write-Host "2. Testing Get All Contacts..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/contacts" -Method GET
    Write-Host "   ✅ Get All Contacts: Found $($response.Count) contacts" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Get All Contacts Failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 3: Create Contact
Write-Host "3. Testing Create Contact..." -ForegroundColor Yellow
$newContact = @{
    firstName = "Test"
    lastName = "User"
    email = "test.user@example.com"
    phoneNumber = "+1234567890"
    address = "123 Test St, Test City, TS 12345"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/contacts" -Method POST -Body $newContact -ContentType "application/json"
    Write-Host "   ✅ Create Contact: Created contact with ID $($response.id)" -ForegroundColor Green
    $contactId = $response.id
} catch {
    Write-Host "   ❌ Create Contact Failed: $($_.Exception.Message)" -ForegroundColor Red
    $contactId = 1  # Use default ID for subsequent tests
}
Write-Host ""

# Test 4: Get Contact by ID
Write-Host "4. Testing Get Contact by ID..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/contacts/$contactId" -Method GET
    Write-Host "   ✅ Get Contact by ID: $($response.firstName) $($response.lastName)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Get Contact by ID Failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 5: Update Contact
Write-Host "5. Testing Update Contact..." -ForegroundColor Yellow
$updateContact = @{
    firstName = "Updated"
    lastName = "User"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/contacts/$contactId" -Method PUT -Body $updateContact -ContentType "application/json"
    Write-Host "   ✅ Update Contact: Updated to $($response.firstName) $($response.lastName)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Update Contact Failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 6: Search Contacts
Write-Host "6. Testing Search Contacts..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/contacts?search=test&page=1&pageSize=5" -Method GET
    Write-Host "   ✅ Search Contacts: Found $($response.Count) contacts matching 'test'" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Search Contacts Failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 7: Delete Contact
Write-Host "7. Testing Delete Contact..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/contacts/$contactId" -Method DELETE
    Write-Host "   ✅ Delete Contact: Successfully deleted contact $contactId" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Delete Contact Failed: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

Write-Host "🎉 API Testing Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📖 To view the API documentation, visit: $baseUrl" -ForegroundColor Cyan
Write-Host "📋 To import Postman collection, use: Postman-Collection/ContactAPI.postman_collection.json" -ForegroundColor Cyan 