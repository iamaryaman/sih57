"""
Legal Metrology Compliance System - Quick Demo

This script demonstrates the key capabilities of the compliance checking system.
"""

import json
from compliance_checker import check_product_compliance, LegalMetrologyComplianceChecker
from reporting_system import ComplianceReporter
from legal_metrology_rules import get_compliance_rules_for_ecommerce

def demo_single_product_check():
    """Demo single product compliance checking"""
    print("=" * 60)
    print("DEMO 1: Single Product Compliance Check")
    print("=" * 60)
    
    # Compliant product
    compliant_product = {
        "title": "Premium Basmati Rice",
        "description": "High quality basmati rice, 5 kg package",
        "weight": "5 kg",
        "dimensions": "30 x 20 x 10 cm",
        "price_per_unit": "₹200 per kg",
        "is_prepackaged": True,
        "net_quantity": "5 kg",
        "manufacturer_details": "ABC Foods Pvt Ltd, Delhi",
        "package_date": "2023-01-15"
    }
    
    print("✅ CHECKING COMPLIANT PRODUCT:")
    print(f"Product: {compliant_product['title']}")
    
    report = check_product_compliance(compliant_product)
    print(f"Status: {report['status']}")
    print(f"Violations: {report['total_violations']}")
    print()
    
    # Non-compliant product
    non_compliant_product = {
        "title": "Organic Wheat Flour - 5 pounds bag",
        "description": "Fresh wheat flour, 5 lb package",
        "weight": "5 lbs",
        "dimensions": "12 x 8 x 4 inches",
        "price_per_unit": "₹150 per pound",
        "is_prepackaged": True,
        "net_quantity": "5 pounds"
    }
    
    print("❌ CHECKING NON-COMPLIANT PRODUCT:")
    print(f"Product: {non_compliant_product['title']}")
    
    report = check_product_compliance(non_compliant_product)
    print(f"Status: {report['status']}")
    print(f"Total Violations: {report['total_violations']}")
    
    print("\nViolations Found:")
    for i, violation in enumerate(report['violations'][:3], 1):  # Show first 3
        print(f"  {i}. {violation['type'].replace('_', ' ').upper()}")
        print(f"     Field: {violation['field']} = '{violation['detected_value']}'")
        print(f"     Fix: {violation['fix']}")
        print(f"     Penalty: {violation['penalty']}")
        print()

def demo_violation_detection():
    """Demo different types of violations"""
    print("=" * 60)
    print("DEMO 2: Violation Detection Examples")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "Imperial Weight Units",
            "product": {"weight": "5 lbs", "title": "Test Product"},
            "expected": "non_standard_weight_unit"
        },
        {
            "name": "Imperial Length Units", 
            "product": {"dimensions": "12 x 8 x 4 inches", "title": "Test Product"},
            "expected": "non_standard_length_unit"
        },
        {
            "name": "Traditional Indian Units",
            "product": {"weight": "1 ser", "title": "Test Product"},
            "expected": "non_standard_weight_unit"
        },
        {
            "name": "Volume Units",
            "product": {"volume": "1 gallon", "title": "Test Product"},
            "expected": "non_standard_volume_unit"
        },
        {
            "name": "Pricing Violations",
            "product": {"price_per_unit": "₹200 per pound", "title": "Test Product"},
            "expected": "non_standard_unit_in_pricing"
        }
    ]
    
    checker = LegalMetrologyComplianceChecker()
    
    for test in test_cases:
        print(f"Testing: {test['name']}")
        violations = checker.check_product_listing(test['product'])
        
        found_expected = any(v.violation_type == test['expected'] for v in violations)
        status = "✅ DETECTED" if found_expected else "❌ MISSED"
        
        print(f"  Result: {status}")
        if violations:
            print(f"  Violation: {violations[0].description}")
        print()

def demo_bulk_compliance():
    """Demo bulk compliance checking"""
    print("=" * 60)
    print("DEMO 3: Bulk Compliance Analysis")
    print("=" * 60)
    
    # Load sample products
    try:
        with open('sample_products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
    except FileNotFoundError:
        print("❌ sample_products.json not found. Skipping bulk demo.")
        return
    
    print(f"Analyzing {len(products)} sample products...")
    
    # Generate bulk report
    reporter = ComplianceReporter()
    bulk_report = reporter.generate_bulk_compliance_report(products[:5], 'json')  # First 5 products
    
    summary = bulk_report['summary']
    
    print(f"\n📊 COMPLIANCE SUMMARY:")
    print(f"Total Products: {summary['total_products']}")
    print(f"Compliant: {summary['compliant_products']} ({summary['compliant_products']/summary['total_products']*100:.1f}%)")
    print(f"Non-Compliant: {summary['non_compliant_products']} ({summary['non_compliant_products']/summary['total_products']*100:.1f}%)")
    
    print(f"\n🚨 VIOLATIONS BY SEVERITY:")
    print(f"Critical: {summary['critical_violations']}")
    print(f"High: {summary['high_violations']}")
    print(f"Medium: {summary['medium_violations']}")
    print(f"Low: {summary['low_violations']}")
    
    # Most common violations
    if summary['violation_types']:
        print(f"\n📋 TOP VIOLATION TYPES:")
        sorted_violations = sorted(summary['violation_types'].items(), key=lambda x: x[1], reverse=True)
        for violation_type, count in sorted_violations[:5]:
            print(f"  • {violation_type.replace('_', ' ').title()}: {count} occurrences")
    
    # Generate alerts
    alerts = reporter.generate_alert_summary(products[:5])
    print(f"\n⚠️  ALERT SUMMARY:")
    print(f"Critical Alerts: {alerts['total_critical']}")
    print(f"High Priority Alerts: {alerts['total_high_priority']}")
    print(f"Immediate Action Required: {'YES' if alerts['requires_immediate_action'] else 'NO'}")

def demo_legal_rules():
    """Demo extracted legal rules"""
    print("=" * 60)
    print("DEMO 4: Legal Metrology Rules Extract")
    print("=" * 60)
    
    rules = get_compliance_rules_for_ecommerce()
    
    print("📜 STANDARD UNITS REQUIREMENTS:")
    for unit_type, unit_name in rules['standard_units']['base_units'].items():
        print(f"  • {unit_type.title()}: {unit_name}")
    
    print(f"\n📦 PRE-PACKAGED COMMODITY REQUIREMENTS:")
    for req in rules['prepackaged_requirements']['mandatory_declarations']:
        print(f"  • {req.replace('_', ' ').title()}")
    
    print(f"\n💰 PENALTY STRUCTURE:")
    for severity, details in rules['penalty_structure'].items():
        print(f"  • {severity.replace('_', ' ').title()}:")
        print(f"    - Range: {details['range']}")
        if 'imprisonment' in details:
            print(f"    - Imprisonment: {details['imprisonment']}")
        if 'examples' in details:
            print(f"    - Examples: {', '.join(details['examples'])}")
        print()

def main():
    """Run all demos"""
    print("🏛️  LEGAL METROLOGY COMPLIANCE SYSTEM DEMO")
    print("📋 Extracting features from Legal Metrology Act 2009 for E-commerce")
    print()
    
    try:
        demo_single_product_check()
        print()
        
        demo_violation_detection()
        print()
        
        demo_bulk_compliance()
        print()
        
        demo_legal_rules()
        print()
        
        print("=" * 60)
        print("✅ DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("🌐 To use the web interface, run: python web_app.py")
        print("📖 For detailed documentation, see: README.md")
        print("📊 For bulk analysis, see generated reports in: /reports")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {str(e)}")
        print("Please ensure all required files are present and dependencies are installed.")

if __name__ == "__main__":
    main()