# FastAPI Test Client - PowerShell Script
# This script allows you to easily test GET and POST requests against your FastAPI server

# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

param (
    [Parameter(Mandatory=$false)]
    [string]$Method = "",

    [Parameter(Mandatory=$false)]
    [string]$Endpoint = "",

    [Parameter(Mandatory=$false)]
    [string]$Id = ""
)

# Configuration
$baseUrl = "http://localhost:8000"
$apiVersion = "v1"

# Build the URL
$url = $baseUrl
if ($apiVersion) {
    $url += "/$apiVersion"
}
if ($Endpoint) {
    $url += "/$Endpoint"
}
if ($Id) {
    $url += "/$Id"
}

# Change this to your desired POST body
# $PostBody = @{
#     user_name = "another_user"
#     full_name = "Another User"
#     email = "myemail@aa.com"
#     password = "mypassword"
# }

$PostBody = @{
    name = "ps5"
    description = "playstation 5"
    price = 499.99
}

# Function to make a GET request
function GetReq {
    Write-Host "Making GET request to: $url" -ForegroundColor Cyan
    
    try {
        $response = Invoke-RestMethod -Uri $url -Method Get -ContentType "application/json"
        # $response = Invoke-RestMethod -Uri $url -Method Get -Headers $Headers -ContentType "application/json"
        Write-Host "SUCCESS! Status: 200" -ForegroundColor Green
        return $response
    }
    catch {
        Write-Host "ERROR! Status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
        Write-Host $_.Exception.Message
        if ($_.ErrorDetails.Message) {
            Write-Host "Response: $($_.ErrorDetails.Message)" -ForegroundColor Red
        }
    }
}


# Function to make a POST request
function PostReq {
    # Convert body to JSON
    $jsonBody = $PostBody | ConvertTo-Json -Depth 10
    
    Write-Host "Making POST request to: $url" -ForegroundColor Cyan
    Write-Host "Body: $jsonBody" -ForegroundColor Magenta
    
    try {
        $response = Invoke-RestMethod -Uri $url -Method Post -Body $jsonBody -ContentType "application/json"
        # $response = Invoke-RestMethod -Uri $url -Method Post -Body $jsonBody -Headers $Headers -ContentType "application/json"
        Write-Host "SUCCESS! Status: 201" -ForegroundColor Green
        return $response
    }
    catch {
        Write-Host "ERROR! Status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
        Write-Host $_.Exception.Message
        if ($_.ErrorDetails.Message) {
            Write-Host "Response: $($_.ErrorDetails.Message)" -ForegroundColor Red
        }
    }
}

if ($Method -eq "GET") {
    GetReq
} elseif ($Method -eq "POST") {
    PostReq
} else {
    Write-Host "PowerShell Script to test REST API on LocalHost" -ForegroundColor Yellow
    Write-Host "=================" -ForegroundColor Yellow
    Write-Host "Arguments:" -ForegroundColor Yellow
    Write-Host "- Method: GET or POST" -ForegroundColor White
    Write-Host "- Endpoint: The API endpoint to call (e.g., 'items', 'users', 'orders')" -ForegroundColor White
    Write-Host "- ItemId: Optional ID for specific item (e.g., '1')" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yello
    Write-Host "- Get all items: -Method GET -Endpoint 'items'" -ForegroundColor White
    Write-Host "- Get single item: -Method GET -Endpoint 'items' -Id 1" -ForegroundColor White
    Write-Host "- Create item (method 1): -Method POST -Endpoint 'items' -Body @{ name = 'New Item'; description = 'This is a test item'; owner_id = 1 }" -ForegroundColor White
    Write-Host "- Create item (method 2): -Method POST -Endpoint 'items' -BodyScript { @{ name = 'New Item'; description = 'This is a test item'; owner_id = 1 } }" -ForegroundColor White
    Write-Host ""
}

