# Installation Guide - Legal Metrology Compliance System

## Quick Installation (Windows)

### Prerequisites
- **Python 3.7+** installed on your system
- **pip** package manager (comes with Python)

### Option 1: One-Command Installation
```powershell
pip install Flask pandas matplotlib numpy requests
```

### Option 2: Using Requirements File
```powershell
pip install -r requirements.txt
```

### Option 3: Run Installation Script
**For PowerShell:**
```powershell
.\install.ps1
```

**For Command Prompt:**
```cmd
install.bat
```

## Verification

Test if everything is installed correctly:

```powershell
python -c "import flask, pandas, matplotlib, numpy; print('✅ All libraries installed successfully!')"
```

## Quick Start

1. **Install dependencies** (using any option above)
2. **Run the demo:**
   ```powershell
   python demo.py
   ```
3. **Start the web application:**
   ```powershell
   python web_app.py
   ```
4. **Open your browser** to: http://localhost:5000

## Required Libraries

### Core Dependencies (Essential)
- **Flask** - Web framework for the user interface
- **pandas** - Data processing and analysis
- **matplotlib** - Chart generation and visualization  
- **numpy** - Numerical computing support
- **requests** - HTTP client for API functionality

### Optional Libraries
- **jsonschema** - JSON data validation
- **python-dateutil** - Date/time handling
- **colorama** - Colored console output
- **openpyxl** - Excel file support

## Troubleshooting

### Common Issues

**1. "Python is not recognized"**
- Install Python from https://python.org
- Make sure to check "Add Python to PATH" during installation

**2. "pip is not recognized"**
- Reinstall Python with pip included
- Or run: `python -m ensurepip --upgrade`

**3. Permission Errors**
- Run PowerShell/Command Prompt as Administrator
- Or use: `pip install --user <package_name>`

**4. Package Installation Fails**
- Update pip: `python -m pip install --upgrade pip`
- Try installing packages individually:
  ```powershell
  pip install Flask
  pip install pandas
  pip install matplotlib
  pip install numpy
  pip install requests
  ```

### Virtual Environment (Recommended)

For better dependency management:

```powershell
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# To deactivate later
deactivate
```

## System Requirements

- **OS**: Windows 7/8/10/11
- **Python**: 3.7 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB for dependencies

## Alternative Installation Methods

### Using conda (if you have Anaconda/Miniconda)
```bash
conda install flask pandas matplotlib numpy requests
```

### Using pip with specific versions (for compatibility)
```powershell
pip install Flask==3.1.2 pandas==2.3.1 matplotlib==3.10.6 numpy==2.2.6 requests==2.32.5
```

## Directory Structure After Installation

```
legalrules/
├── legal_metrology_rules.py      # Rules extraction
├── compliance_checker.py         # Compliance engine  
├── reporting_system.py           # Report generation
├── web_app.py                    # Web interface
├── demo.py                       # Demo script
├── sample_products.json          # Test data
├── requirements.txt              # Dependencies
├── README.md                     # Documentation
├── INSTALL.md                    # This file
├── install.ps1                   # PowerShell installer
├── install.bat                   # Batch installer
├── reports/                      # Generated reports
├── uploads/                      # Uploaded files
└── templates/                    # HTML templates
```

## Next Steps

After successful installation:

1. **📖 Read the documentation**: `README.md`
2. **🚀 Run the demo**: `python demo.py`
3. **🌐 Try the web interface**: `python web_app.py`
4. **📊 Test with sample data**: Use `sample_products.json`

## Support

If you encounter any issues:

1. Check that Python 3.7+ is installed: `python --version`
2. Verify pip is working: `pip --version`
3. Try the troubleshooting steps above
4. Check the demo output for any error messages

## Success Indicators

✅ **Installation Successful** if you see:
- `python demo.py` runs without errors
- Web interface starts at `http://localhost:5000`
- Sample compliance checks show violations detected

---

**Ready to use!** The Legal Metrology Compliance System is now installed and ready for e-commerce compliance checking.