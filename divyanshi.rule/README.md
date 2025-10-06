# Legal Metrology Compliance System for E-commerce

A comprehensive software solution to extract important features from the Legal Metrology Act 2009 and check e-commerce product listings for compliance violations.

## Features

### 🔍 **Compliance Checking**
- **Single Product Check**: Validate individual product listings with real-time feedback
- **Bulk Compliance Check**: Process multiple products from JSON files
- **Real-time Validation**: Instant feedback as you enter product information

### 📋 **Rule Extraction**
- Comprehensive extraction of Legal Metrology Act 2009 requirements
- E-commerce specific compliance rules
- Penalty structures and violation severity classification

### 📊 **Reporting & Analytics**
- Detailed compliance reports (JSON, CSV, HTML formats)
- Visual analytics with charts and graphs
- Alert system for critical violations
- Downloadable reports for auditing

### 🌐 **Web Interface**
- User-friendly dashboard
- Drag-and-drop file uploads
- Interactive compliance checking
- Mobile-responsive design

## Key Legal Metrology Requirements Covered

### Standard Units (Section 11)
- ✅ Weight: kg, g, mg (metric only)
- ✅ Length: m, cm, mm (metric only)  
- ✅ Volume: l, ml (metric only)
- ❌ Imperial units: lbs, inches, gallons (flagged as violations)

### Pre-packaged Commodities (Section 18)
- Net quantity declarations
- Manufacturer details
- Package date information
- Standard quantity requirements

### Pricing Compliance (Section 11)
- Price quotes must use standard units only
- Unit pricing validation
- Bulk pricing compliance

### Penalties
- Fine ranges from ₹2,000 to ₹1,00,000
- Imprisonment: 6 months to 5 years for repeat offenses
- Company name publication for violations

## Installation & Setup

### Quick Installation (Windows)

**Option 1 - One Command:**
```powershell
pip install Flask pandas matplotlib numpy requests
```

**Option 2 - Using Requirements File:**
```powershell
pip install -r requirements.txt
```

**Option 3 - Run Installation Script:**
```powershell
# PowerShell
.\install.ps1

# Command Prompt
install.bat
```

### Verification
Test if everything works:
```powershell
python setup_test.py
```

### Prerequisites
- Python 3.7+ installed
- pip package manager
- Windows 7/8/10/11

### Files Structure
```
legalrules/
├── legal_metrology_rules.py      # Extracted rules and requirements
├── compliance_checker.py         # Core compliance checking engine  
├── reporting_system.py           # Report generation and analytics
├── web_app.py                    # Flask web interface
├── sample_products.json          # Sample data for testing
├── legalmetrology_act_2009.pdf   # Source legal document
└── README.md                     # This file
```

## Usage

### 1. Command Line Interface

**Single Product Check:**
```python
from compliance_checker import check_product_compliance

product = {
    "title": "Premium Rice",
    "weight": "5 kg",
    "dimensions": "30 x 20 x 10 cm", 
    "price_per_unit": "₹200 per kg",
    "is_prepackaged": True,
    "net_quantity": "5 kg",
    "manufacturer_details": "ABC Foods"
}

report = check_product_compliance(product)
print(f"Status: {report['status']}")
print(f"Violations: {report['total_violations']}")
```

**Bulk Check:**
```python
from reporting_system import bulk_compliance_check

# Check products from JSON file
report = bulk_compliance_check('sample_products.json', 'html')
print(f"Compliant: {report['summary']['compliant_products']}")
print(f"Non-compliant: {report['summary']['non_compliant_products']}")
```

### 2. Web Interface

**Start the web application:**
```bash
python web_app.py
```

Then open http://localhost:5000 in your browser.

**Available endpoints:**
- `/` - Main dashboard
- `/single-check` - Single product compliance check
- `/bulk-check` - Bulk compliance checking
- `/api/check-single` - API for single product check
- `/api/check-bulk` - API for bulk checking

## Sample Test Results

Using the provided `sample_products.json`:

### Compliance Summary
- **Total Products**: 10
- **Compliant**: 2 (20%)
- **Non-Compliant**: 8 (80%)
- **Critical Violations**: 6
- **High Priority**: 12

### Common Violations Found
1. **Non-standard weight units**: lbs, pounds, ser (traditional Indian unit)
2. **Non-standard length units**: inches, feet
3. **Non-standard volume units**: gallons, fl oz
4. **Missing pre-packaged declarations**: manufacturer details, package date
5. **Non-standard units in pricing**: "per pound", "per gallon"

## API Reference

### Single Product Check API
```http
POST /api/check-single
Content-Type: application/json

{
  "title": "Product Name",
  "weight": "5 kg",
  "dimensions": "30 x 20 x 10 cm",
  "price_per_unit": "₹200 per kg",
  "is_prepackaged": true,
  "net_quantity": "5 kg",
  "manufacturer_details": "Company Name"
}
```

**Response:**
```json
{
  "success": true,
  "compliance_report": {
    "status": "COMPLIANT|NON_COMPLIANT_MINOR|NON_COMPLIANT_HIGH|NON_COMPLIANT_CRITICAL",
    "total_violations": 0,
    "violations": [],
    "recommendations": []
  }
}
```

### Bulk Check API
```http
POST /api/check-bulk
Content-Type: multipart/form-data

file: [JSON file with product array]
format: json|html|csv
```

## Violation Severity Levels

| Severity | Description | Fine Range | Examples |
|----------|-------------|------------|----------|
| **Critical** | Pricing violations, fraudulent practices | ₹10,000 - ₹1,00,000 | Non-standard units in pricing |
| **High** | Unit violations, missing declarations | ₹2,000 - ₹25,000 | Imperial units, missing manufacturer info |
| **Medium** | Description violations | ₹2,000 - ₹10,000 | Non-standard units in product descriptions |
| **Low** | Minor formatting issues | ₹2,000 - ₹5,000 | Minor labeling inconsistencies |

## Legal Compliance Features

### Automated Detection
- ✅ Imperial to Metric unit violations
- ✅ Traditional Indian units (ser, maund, tola)
- ✅ Informal units (cups, spoons, pieces)
- ✅ Missing pre-packaged commodity declarations
- ✅ Non-standard pricing quotations

### Reporting Capabilities
- **JSON**: Structured data for API integration
- **CSV**: Excel-compatible for data analysis  
- **HTML**: Professional reports for presentations
- **Charts**: Visual compliance analytics

### Real-time Validation
- Field-level validation as you type
- Instant feedback on compliance status
- Suggested fixes for violations
- Penalty risk assessment

## Integration Examples

### E-commerce Platform Integration
```python
# Shopify/WooCommerce integration example
def validate_product_before_publish(product_data):
    report = check_product_compliance(product_data)
    
    if report['status'] != 'COMPLIANT':
        # Block publication and show violations
        return {
            'allow_publish': False,
            'violations': report['violations'],
            'recommendations': report['recommendations']
        }
    
    return {'allow_publish': True}
```

### Inventory Management Integration
```python
# Bulk validate existing inventory
def audit_inventory(inventory_file):
    reporter = ComplianceReporter()
    report = reporter.generate_bulk_compliance_report(
        load_products(inventory_file), 
        'html'
    )
    
    # Generate alerts for non-compliant products
    alerts = reporter.generate_alert_summary(load_products(inventory_file))
    
    return report, alerts
```

## Customization

### Adding New Rules
Extend `legal_metrology_rules.py`:
```python
CUSTOM_RULES = {
    "new_requirement": {
        "description": "Custom requirement description",
        "penalty": "Fine structure",
        "compliance_check": "Validation logic"
    }
}
```

### Custom Violation Types
Extend `compliance_checker.py`:
```python
def _check_custom_compliance(self, product_data):
    violations = []
    # Add custom validation logic
    return violations
```

## Legal Disclaimer

This software is designed to assist with Legal Metrology Act 2009 compliance but does not constitute legal advice. Users should:

- Consult with legal experts for complex compliance issues
- Stay updated with latest amendments to the Act
- Validate compliance with relevant authorities
- Use this tool as a supplementary compliance aid

## Support & Contribution

For questions, bug reports, or feature requests:
- Review the Legal Metrology Act 2009 document included
- Check sample products for usage examples
- Refer to penalty structures in `legal_metrology_rules.py`

## License

This project is created for educational and compliance assistance purposes. Please ensure you comply with all applicable laws and regulations in your jurisdiction.

---

**Note**: This system covers major e-commerce compliance requirements from the Legal Metrology Act 2009. For comprehensive legal compliance, consult with qualified legal professionals.