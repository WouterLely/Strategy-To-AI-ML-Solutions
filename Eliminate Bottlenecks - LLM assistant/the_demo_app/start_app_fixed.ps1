# TechAdvance Solutions - PowerShell Startup Script
# Automatically sets up environment and starts the application

Write-Host "TechAdvance Solutions - Automated Startup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Check if virtual environment exists
if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& ".venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Green
python -m pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# OpenAI Configuration Setup
Write-Host "Checking OpenAI Configuration..." -ForegroundColor Cyan

# Check for OpenAI credentials in .venv directory (secure local storage)
$venvConfigFile = ".venv\openai_config.txt"
$envFile = ".env"

# Function to prompt for OpenAI credentials
function Get-OpenAICredentials {
    Write-Host ""
    Write-Host "OpenAI API Setup Required" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "To use OpenAI GPT for intelligent responses, you need an API key." -ForegroundColor White
    Write-Host "Get your API key from: https://platform.openai.com/api-keys" -ForegroundColor Cyan
    Write-Host ""
    
    # Prompt for API key
    do {
        $apiKey = Read-Host "Enter your OpenAI API Key (starts with 'sk-')"
        if ($apiKey -and $apiKey.StartsWith("sk-") -and $apiKey.Length -gt 20) {
            break
        } else {
            Write-Host "Invalid API key format. Please enter a valid OpenAI API key." -ForegroundColor Red
        }
    } while ($true)
    
    # Prompt for model (with default)
    Write-Host ""
    Write-Host "Available models:" -ForegroundColor White
    Write-Host "1. gpt-3.5-turbo (faster, cheaper)" -ForegroundColor Gray
    Write-Host "2. gpt-4 (more capable, higher cost)" -ForegroundColor Gray
    Write-Host "3. gpt-4-turbo (latest, balanced)" -ForegroundColor Gray
    
    $modelChoice = Read-Host "Choose model (1-3, or press Enter for default)"
    
    switch ($modelChoice) {
        "2" { $model = "gpt-4" }
        "3" { $model = "gpt-4-turbo" }
        default { $model = "gpt-3.5-turbo" }
    }
    
    return @{
        ApiKey = $apiKey
        Model = $model
    }
}

# Check if credentials exist in .venv (preferred method)
if (Test-Path $venvConfigFile) {
    Write-Host "Found OpenAI config in .venv directory" -ForegroundColor Green
    $configContent = Get-Content $venvConfigFile
    $apiKey = ($configContent | Where-Object { $_ -like "OPENAI_API_KEY=*" }) -replace "OPENAI_API_KEY=", ""
    $model = ($configContent | Where-Object { $_ -like "OPENAI_MODEL=*" }) -replace "OPENAI_MODEL=", ""
    
    if (-not $model) { $model = "gpt-3.5-turbo" }
}
# Check if .env file exists and has valid credentials
elseif (Test-Path $envFile) {
    $envContent = Get-Content $envFile
    $apiKey = ($envContent | Where-Object { $_ -like "OPENAI_API_KEY=*" }) -replace "OPENAI_API_KEY=", ""
    $model = ($envContent | Where-Object { $_ -like "OPENAI_MODEL=*" }) -replace "OPENAI_MODEL=", ""
    
    if ($apiKey -and $apiKey -ne "your_openai_api_key_here" -and $apiKey.StartsWith("sk-")) {
        Write-Host "Found OpenAI config in .env file" -ForegroundColor Green
        # Migrate to .venv for better security
        @"
OPENAI_API_KEY=$apiKey
OPENAI_MODEL=$model
"@ | Out-File -FilePath $venvConfigFile -Encoding UTF8
        Write-Host "Migrated config to .venv directory for better security" -ForegroundColor Green
    } else {
        $apiKey = $null
    }
}

# If no valid credentials found, prompt user
if (-not $apiKey -or $apiKey -eq "your_openai_api_key_here" -or -not $apiKey.StartsWith("sk-")) {
    $credentials = Get-OpenAICredentials
    $apiKey = $credentials.ApiKey
    $model = $credentials.Model
    
    # Save to .venv directory (more secure than .env)
    @"
OPENAI_API_KEY=$apiKey
OPENAI_MODEL=$model
"@ | Out-File -FilePath $venvConfigFile -Encoding UTF8
    
    Write-Host "OpenAI credentials saved securely in .venv directory" -ForegroundColor Green
}

# Set environment variables for the current session
$env:OPENAI_API_KEY = $apiKey
$env:OPENAI_MODEL = $model
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $apiKey, 'Process')
[System.Environment]::SetEnvironmentVariable('OPENAI_MODEL', $model, 'Process')

Write-Host "OpenAI configured: $model" -ForegroundColor Green

# Create or update .env file for compatibility
@"
# OpenAI Configuration (managed by start_app.ps1)
OPENAI_API_KEY=$apiKey
OPENAI_MODEL=$model

# This file is auto-generated. To update credentials, delete .venv\openai_config.txt and restart.
"@ | Out-File -FilePath $envFile -Encoding UTF8

# Check if database exists, create if it doesn't
if (!(Test-Path "data\database\company.db")) {
    Write-Host "Creating database..." -ForegroundColor Yellow
    python scripts/create_database.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Database created successfully!" -ForegroundColor Green
    } else {
        Write-Host "Database creation failed" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Database already exists" -ForegroundColor Green
}

# Start the application
Write-Host "Starting TechAdvance Solutions platform..." -ForegroundColor Cyan
Write-Host "Application will be available at: http://localhost:8501" -ForegroundColor Yellow
Write-Host "OpenAI GPT integration enabled" -ForegroundColor Green
Write-Host ""

streamlit run app/enterprise_app.py

