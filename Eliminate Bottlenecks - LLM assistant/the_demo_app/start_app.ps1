# TechAdvance Solutions - PowerShell Startup Script
# Automatically sets up environment and starts the application

Write-Host "🌟 TechAdvance Solutions - Automated Startup" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Check if virtual environment exists
if (!(Test-Path ".venv")) {
    Write-Host "🔧 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Green
& ".venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Green
python -m pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Check if .env file exists, create template if it doesn't
if (!(Test-Path ".env")) {
    Write-Host "🔧 Creating .env template..." -ForegroundColor Yellow
    @"
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Instructions:
# 1. Get your API key from: https://platform.openai.com/api-keys
# 2. Replace 'your_openai_api_key_here' with your actual API key
# 3. Save this file and restart the application
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ .env template created!" -ForegroundColor Green
    Write-Host "📝 Please edit .env file and add your OpenAI API key" -ForegroundColor Yellow
    Write-Host "🔗 Get your API key from: https://platform.openai.com/api-keys" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Press any key to continue after adding your API key..." -ForegroundColor Magenta
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Check if database exists, create if it doesn't
if (!(Test-Path "data\database\company.db")) {
    Write-Host "🔧 Creating database..." -ForegroundColor Yellow
    python scripts/create_database.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Database created successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Database creation failed" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ Database already exists" -ForegroundColor Green
}

# Start the application
Write-Host "🚀 Starting TechAdvance Solutions platform..." -ForegroundColor Cyan
Write-Host "📍 Application will be available at: http://localhost:8501" -ForegroundColor Yellow
Write-Host "🤖 OpenAI GPT integration enabled" -ForegroundColor Green
Write-Host ""

streamlit run app/enterprise_app.py
