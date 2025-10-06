# Legal Metrology Compliance System - Installation Script for Windows
# Run this script in PowerShell as Administrator if needed

Write-Host "🏛️  Legal Metrology Compliance System - Installation Script" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# Check if Python is installed
Write-Host "📋 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://python.org" -ForegroundColor Red
    exit 1
}

# Check if pip is installed
Write-Host "📋 Checking pip installation..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>$null
    Write-Host "✅ pip found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip is not installed" -ForegroundColor Red
    Write-Host "Installing pip..." -ForegroundColor Yellow
    python -m ensurepip --upgrade
}

# Create virtual environment (recommended)
Write-Host "📋 Setting up virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "✅ Virtual environment created." -ForegroundColor Green
}

# Activate virtual environment
Write-Host "📋 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "📋 Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install required packages
Write-Host "📋 Installing required packages from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All packages installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Some packages failed to install. Trying alternative approach..." -ForegroundColor Red
    
    # Install core packages individually
    Write-Host "Installing core packages individually..." -ForegroundColor Yellow
    
    $corePackages = @(
        "Flask",
        "pandas",
        "matplotlib", 
        "numpy",
        "requests",
        "jsonschema",
        "python-dateutil",
        "colorama"
    )
    
    foreach ($package in $corePackages) {
        Write-Host "Installing $package..." -ForegroundColor Cyan
        pip install $package
    }
}

# Check if all required directories exist
Write-Host "📋 Creating required directories..." -ForegroundColor Yellow
$directories = @("reports", "uploads", "templates")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir
        Write-Host "✅ Created directory: $dir" -ForegroundColor Green
    }
}

# Test the installation
Write-Host "📋 Testing installation..." -ForegroundColor Yellow
try {
    python -c "
import flask
import pandas as pd
import matplotlib.pyplot as plt
import json
import re
from pathlib import Path
print('✅ All core libraries imported successfully!')
"
    Write-Host "✅ Installation test passed!" -ForegroundColor Green
} catch {
    Write-Host "❌ Installation test failed. Some libraries may be missing." -ForegroundColor Red
}

Write-Host ""
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "🎉 Installation Complete!" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Run the demo: python demo.py" -ForegroundColor White
Write-Host "2. Start web interface: python web_app.py" -ForegroundColor White
Write-Host "3. Open browser to: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "📖 Documentation: README.md" -ForegroundColor Cyan
Write-Host "🔧 Virtual environment: .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan