"""
Legal Metrology Compliance System - Setup Verification Script

Run this script to verify that everything is installed correctly
and test all system components.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required libraries can be imported"""
    print("🔍 Testing library imports...")
    
    required_libs = {
        'flask': 'Flask web framework',
        'pandas': 'Data processing',
        'matplotlib': 'Visualization',
        'numpy': 'Numerical computing',
        'requests': 'HTTP client',
        'json': 'JSON processing (built-in)',
        're': 'Regular expressions (built-in)',
        'pathlib': 'Path handling (built-in)',
        'datetime': 'Date/time handling (built-in)'
    }
    
    failed_imports = []
    
    for lib, description in required_libs.items():
        try:
            __import__(lib)
            print(f"  ✅ {lib} - {description}")
        except ImportError as e:
            print(f"  ❌ {lib} - {description} - Error: {str(e)}")
            failed_imports.append(lib)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Run: pip install Flask pandas matplotlib numpy requests")
        return False
    else:
        print("✅ All required libraries imported successfully!")
        return True

def test_directories():
    """Test if all required directories exist"""
    print("\n🔍 Testing directory structure...")
    
    required_dirs = ['reports', 'uploads', 'templates']
    missing_dirs = []
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"  ✅ {dir_name}/ directory exists")
        else:
            print(f"  ⚠️  {dir_name}/ directory missing - creating...")
            try:
                dir_path.mkdir(exist_ok=True)
                print(f"  ✅ Created {dir_name}/ directory")
            except Exception as e:
                print(f"  ❌ Failed to create {dir_name}/ - Error: {str(e)}")
                missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"\n❌ Failed to create directories: {', '.join(missing_dirs)}")
        return False
    else:
        print("✅ All required directories are available!")
        return True

def test_core_files():
    """Test if all core system files exist"""
    print("\n🔍 Testing core system files...")
    
    required_files = {
        'legal_metrology_rules.py': 'Legal rules extraction',
        'compliance_checker.py': 'Compliance checking engine',
        'reporting_system.py': 'Report generation system',
        'web_app.py': 'Web interface',
        'sample_products.json': 'Sample test data',
        'README.md': 'Documentation'
    }
    
    missing_files = []
    
    for filename, description in required_files.items():
        if Path(filename).exists():
            print(f"  ✅ {filename} - {description}")
        else:
            print(f"  ❌ {filename} - {description} - MISSING!")
            missing_files.append(filename)
    
    if missing_files:
        print(f"\n❌ Missing core files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All core system files are present!")
        return True

def test_compliance_engine():
    """Test the compliance checking functionality"""
    print("\n🔍 Testing compliance checking engine...")
    
    try:
        from compliance_checker import check_product_compliance
        
        # Test with a simple compliant product
        test_product = {
            "title": "Test Rice",
            "weight": "5 kg",
            "dimensions": "30 x 20 x 10 cm",
            "price_per_unit": "₹200 per kg"
        }
        
        report = check_product_compliance(test_product)
        
        if 'status' in report and 'violations' in report:
            print("  ✅ Compliance checker working correctly")
            print(f"  📊 Test result: {report['status']} ({report['total_violations']} violations)")
            return True
        else:
            print("  ❌ Compliance checker returned invalid format")
            return False
            
    except Exception as e:
        print(f"  ❌ Compliance checker failed: {str(e)}")
        return False

def test_web_imports():
    """Test web application imports"""
    print("\n🔍 Testing web application components...")
    
    try:
        from web_app import app
        print("  ✅ Flask web application imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ Web application import failed: {str(e)}")
        return False

def test_sample_data():
    """Test sample data loading"""
    print("\n🔍 Testing sample data...")
    
    try:
        import json
        with open('sample_products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        if isinstance(products, list) and len(products) > 0:
            print(f"  ✅ Sample data loaded: {len(products)} products")
            return True
        else:
            print("  ❌ Sample data is empty or invalid format")
            return False
            
    except FileNotFoundError:
        print("  ❌ sample_products.json not found")
        return False
    except Exception as e:
        print(f"  ❌ Failed to load sample data: {str(e)}")
        return False

def run_full_test():
    """Run complete system test"""
    print("🏛️  LEGAL METROLOGY COMPLIANCE SYSTEM - SETUP VERIFICATION")
    print("=" * 70)
    
    tests = [
        ("Library Imports", test_imports),
        ("Directory Structure", test_directories),
        ("Core System Files", test_core_files),
        ("Compliance Engine", test_compliance_engine),
        ("Web Application", test_web_imports),
        ("Sample Data", test_sample_data)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {str(e)}")
    
    print("\n" + "=" * 70)
    print(f"📊 TEST RESULTS: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! System is ready to use.")
        print("\n🚀 Next steps:")
        print("  1. Run demo: python demo.py")
        print("  2. Start web app: python web_app.py")
        print("  3. Open browser: http://localhost:5000")
        return True
    else:
        print("⚠️  Some tests failed. Please resolve issues before using the system.")
        print("\n🔧 Troubleshooting:")
        print("  1. Install missing libraries: pip install Flask pandas matplotlib numpy requests")
        print("  2. Check file permissions and paths")
        print("  3. Ensure all system files are present")
        return False

def install_missing_dependencies():
    """Install missing dependencies"""
    print("\n🔧 Installing missing dependencies...")
    
    import subprocess
    
    required_packages = ['Flask', 'pandas', 'matplotlib', 'numpy', 'requests']
    
    for package in required_packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")

def main():
    """Main setup verification function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--install':
        install_missing_dependencies()
        print("\nRe-running tests after installation...")
    
    success = run_full_test()
    
    if not success and '--install' not in sys.argv:
        print("\n💡 To auto-install missing dependencies, run:")
        print("   python setup_test.py --install")

if __name__ == "__main__":
    main()