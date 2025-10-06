"""
Legal Metrology Compliance Web Application

A Flask-based web interface for checking e-commerce product listings
against Legal Metrology Act 2009 requirements.
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import json
import os
from werkzeug.utils import secure_filename
from compliance_checker import check_product_compliance, LegalMetrologyComplianceChecker
from reporting_system import ComplianceReporter
from legal_metrology_rules import get_compliance_rules_for_ecommerce, get_critical_sections_for_ecommerce

app = Flask(__name__)
app.secret_key = 'legal_metrology_compliance_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary directories
os.makedirs('uploads', exist_ok=True)
os.makedirs('reports', exist_ok=True)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/single-check')
def single_check():
    """Single product compliance check page"""
    return render_template('single_check.html')

@app.route('/bulk-check')
def bulk_check():
    """Bulk compliance check page"""
    return render_template('bulk_check.html')

@app.route('/api/check-single', methods=['POST'])
def api_check_single():
    """API endpoint for single product compliance check"""
    try:
        product_data = request.json
        if not product_data:
            return jsonify({"error": "No product data provided"}), 400
        
        # Perform compliance check
        compliance_report = check_product_compliance(product_data)
        
        return jsonify({
            "success": True,
            "compliance_report": compliance_report
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/check-bulk', methods=['POST'])
def api_check_bulk():
    """API endpoint for bulk compliance checking"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if file and file.filename.endswith('.json'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Load products data
            with open(filepath, 'r', encoding='utf-8') as f:
                products = json.load(f)
            
            # Get report format from request
            report_format = request.form.get('format', 'json')
            
            # Generate compliance report
            reporter = ComplianceReporter()
            bulk_report = reporter.generate_bulk_compliance_report(products, report_format)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                "success": True,
                "report": bulk_report
            })
        
        else:
            return jsonify({"error": "Invalid file format. Please upload a JSON file."}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/rules')
def api_rules():
    """API endpoint to get compliance rules"""
    try:
        rules = get_compliance_rules_for_ecommerce()
        critical_sections = get_critical_sections_for_ecommerce()
        
        return jsonify({
            "success": True,
            "rules": rules,
            "critical_sections": critical_sections
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/validate-product', methods=['POST'])
def api_validate_product():
    """API endpoint to validate product fields in real-time"""
    try:
        field_data = request.json
        field_name = field_data.get('field_name')
        field_value = field_data.get('field_value')
        
        if not field_name or not field_value:
            return jsonify({"error": "Field name and value are required"}), 400
        
        # Create temporary product data for validation
        temp_product = {field_name: field_value}
        
        # Check compliance
        checker = LegalMetrologyComplianceChecker()
        violations = checker.check_product_listing(temp_product)
        
        # Filter violations for this specific field
        field_violations = [v for v in violations if v.field_name == field_name]
        
        return jsonify({
            "success": True,
            "is_valid": len(field_violations) == 0,
            "violations": [
                {
                    "type": v.violation_type,
                    "description": v.description,
                    "suggested_fix": v.suggested_fix,
                    "severity": v.severity.value
                } for v in field_violations
            ]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download-report/<timestamp>')
def download_report(timestamp):
    """Download generated compliance reports"""
    try:
        report_files = [
            f"reports/compliance_report_{timestamp}.json",
            f"reports/compliance_report_{timestamp}.html",
            f"reports/compliance_summary_{timestamp}.csv",
            f"reports/compliance_details_{timestamp}.csv",
            f"reports/compliance_charts_{timestamp}.png"
        ]
        
        # Find the first existing file
        for file_path in report_files:
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True)
        
        return jsonify({"error": "Report file not found"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# HTML Templates (embedded for simplicity)
@app.route('/templates/<template_name>')
def get_template(template_name):
    """Serve HTML templates"""
    templates = {
        'index.html': '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Legal Metrology Compliance Checker</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; }
        .header { background-color: #2c3e50; color: white; padding: 20px 0; text-align: center; }
        .container { max-width: 1200px; margin: 20px auto; padding: 0 20px; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 30px; }
        .card { background: white; border-radius: 8px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; transition: transform 0.3s; }
        .card:hover { transform: translateY(-5px); }
        .card h3 { color: #2c3e50; margin-bottom: 15px; }
        .card p { color: #7f8c8d; margin-bottom: 20px; }
        .btn { display: inline-block; background-color: #3498db; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; transition: background-color 0.3s; }
        .btn:hover { background-color: #2980b9; }
        .info-section { background: white; border-radius: 8px; padding: 30px; margin-top: 30px; }
        .rules-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 20px; }
        .rule-item { background: #ecf0f1; padding: 15px; border-radius: 5px; border-left: 4px solid #e74c3c; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Legal Metrology Compliance Checker</h1>
        <p>Ensure your e-commerce products comply with Legal Metrology Act 2009</p>
    </div>
    
    <div class="container">
        <div class="dashboard">
            <div class="card">
                <h3>Single Product Check</h3>
                <p>Check compliance for individual product listings with real-time validation and detailed feedback.</p>
                <a href="/single-check" class="btn">Check Single Product</a>
            </div>
            
            <div class="card">
                <h3>Bulk Compliance Check</h3>
                <p>Upload multiple products and generate comprehensive compliance reports with visualizations.</p>
                <a href="/bulk-check" class="btn">Bulk Check Products</a>
            </div>
            
            <div class="card">
                <h3>Compliance Rules</h3>
                <p>View detailed Legal Metrology Act requirements and penalty structures for e-commerce.</p>
                <a href="#rules" class="btn">View Rules</a>
            </div>
        </div>
        
        <div class="info-section" id="rules">
            <h2>Key Legal Metrology Requirements for E-commerce</h2>
            <div class="rules-grid">
                <div class="rule-item">
                    <h4>Standard Units (Section 11)</h4>
                    <p>All weights, measures must use metric system: kg, g, mg for weight; m, cm, mm for length; l, ml for volume</p>
                </div>
                <div class="rule-item">
                    <h4>Pre-packaged Goods (Section 18)</h4>
                    <p>Must declare net quantity, manufacturer details, and standard quantities on packaging</p>
                </div>
                <div class="rule-item">
                    <h4>Pricing Compliance (Section 11)</h4>
                    <p>Price quotes and announcements must only use standard measurement units</p>
                </div>
                <div class="rule-item">
                    <h4>Penalties (Section 25-47)</h4>
                    <p>Violations can result in fines up to ₹1,00,000 and imprisonment up to 5 years</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
        ''',
        
        'single_check.html': '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Single Product Compliance Check</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; }
        .header { background-color: #2c3e50; color: white; padding: 15px 0; text-align: center; }
        .container { max-width: 800px; margin: 20px auto; padding: 0 20px; }
        .form-section { background: white; border-radius: 8px; padding: 30px; margin-bottom: 20px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #2c3e50; }
        input[type="text"], textarea, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
        textarea { height: 80px; resize: vertical; }
        .btn { background-color: #3498db; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        .btn:hover { background-color: #2980b9; }
        .results { background: white; border-radius: 8px; padding: 30px; margin-top: 20px; display: none; }
        .compliant { color: #27ae60; font-weight: bold; }
        .non-compliant { color: #e74c3c; font-weight: bold; }
        .violation { background: #ffebee; border-left: 4px solid #f44336; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .violation.medium { background: #fff3e0; border-left-color: #ff9800; }
        .violation.low { background: #f3e5f5; border-left-color: #9c27b0; }
        .back-btn { display: inline-block; background-color: #95a5a6; color: white; padding: 8px 16px; text-decoration: none; border-radius: 3px; margin-bottom: 20px; }
        .validation-feedback { font-size: 12px; margin-top: 5px; }
        .valid { color: #27ae60; }
        .invalid { color: #e74c3c; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Single Product Compliance Check</h1>
    </div>
    
    <div class="container">
        <a href="/" class="back-btn">← Back to Dashboard</a>
        
        <div class="form-section">
            <h2>Product Information</h2>
            <form id="productForm">
                <div class="form-group">
                    <label for="title">Product Title</label>
                    <input type="text" id="title" name="title" placeholder="e.g., Premium Basmati Rice">
                    <div class="validation-feedback" id="title-feedback"></div>
                </div>
                
                <div class="form-group">
                    <label for="description">Description</label>
                    <textarea id="description" name="description" placeholder="Detailed product description"></textarea>
                    <div class="validation-feedback" id="description-feedback"></div>
                </div>
                
                <div class="form-group">
                    <label for="weight">Weight</label>
                    <input type="text" id="weight" name="weight" placeholder="e.g., 5 kg">
                    <div class="validation-feedback" id="weight-feedback"></div>
                </div>
                
                <div class="form-group">
                    <label for="dimensions">Dimensions</label>
                    <input type="text" id="dimensions" name="dimensions" placeholder="e.g., 30 x 20 x 10 cm">
                    <div class="validation-feedback" id="dimensions-feedback"></div>
                </div>
                
                <div class="form-group">
                    <label for="volume">Volume (if applicable)</label>
                    <input type="text" id="volume" name="volume" placeholder="e.g., 1 l">
                    <div class="validation-feedback" id="volume-feedback"></div>
                </div>
                
                <div class="form-group">
                    <label for="price_per_unit">Price per Unit</label>
                    <input type="text" id="price_per_unit" name="price_per_unit" placeholder="e.g., ₹200 per kg">
                    <div class="validation-feedback" id="price_per_unit-feedback"></div>
                </div>
                
                <div class="form-group">
                    <label for="is_prepackaged">Is Pre-packaged?</label>
                    <select id="is_prepackaged" name="is_prepackaged">
                        <option value="false">No</option>
                        <option value="true">Yes</option>
                    </select>
                </div>
                
                <div class="form-group" id="prepackaged-fields" style="display: none;">
                    <label for="net_quantity">Net Quantity</label>
                    <input type="text" id="net_quantity" name="net_quantity" placeholder="e.g., 5 kg">
                    <div class="validation-feedback" id="net_quantity-feedback"></div>
                    
                    <label for="manufacturer_details" style="margin-top: 15px;">Manufacturer Details</label>
                    <input type="text" id="manufacturer_details" name="manufacturer_details" placeholder="Manufacturer name and address">
                    <div class="validation-feedback" id="manufacturer_details-feedback"></div>
                </div>
                
                <button type="submit" class="btn">Check Compliance</button>
            </form>
        </div>
        
        <div class="results" id="results">
            <h2>Compliance Results</h2>
            <div id="results-content"></div>
        </div>
    </div>

    <script>
        // Real-time validation
        const fields = ['title', 'description', 'weight', 'dimensions', 'volume', 'price_per_unit', 'net_quantity'];
        
        fields.forEach(field => {
            const input = document.getElementById(field);
            if (input) {
                input.addEventListener('blur', () => validateField(field, input.value));
            }
        });
        
        // Show/hide prepackaged fields
        document.getElementById('is_prepackaged').addEventListener('change', function() {
            const prepackagedFields = document.getElementById('prepackaged-fields');
            prepackagedFields.style.display = this.value === 'true' ? 'block' : 'none';
        });
        
        async function validateField(fieldName, fieldValue) {
            if (!fieldValue.trim()) return;
            
            try {
                const response = await fetch('/api/validate-product', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ field_name: fieldName, field_value: fieldValue })
                });
                
                const result = await response.json();
                const feedback = document.getElementById(fieldName + '-feedback');
                
                if (result.success) {
                    if (result.is_valid) {
                        feedback.textContent = '✓ Valid';
                        feedback.className = 'validation-feedback valid';
                    } else {
                        const violation = result.violations[0];
                        feedback.textContent = '✗ ' + violation.description;
                        feedback.className = 'validation-feedback invalid';
                    }
                }
            } catch (error) {
                console.error('Validation error:', error);
            }
        }
        
        // Form submission
        document.getElementById('productForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const productData = {};
            
            formData.forEach((value, key) => {
                if (value.trim()) {
                    if (key === 'is_prepackaged') {
                        productData[key] = value === 'true';
                    } else {
                        productData[key] = value;
                    }
                }
            });
            
            try {
                const response = await fetch('/api/check-single', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(productData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    displayResults(result.compliance_report);
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Error checking compliance: ' + error.message);
            }
        });
        
        function displayResults(report) {
            const resultsDiv = document.getElementById('results');
            const contentDiv = document.getElementById('results-content');
            
            let statusClass = report.status === 'COMPLIANT' ? 'compliant' : 'non-compliant';
            let statusText = report.status.replace(/_/g, ' ');
            
            let html = `<p class="${statusClass}">Status: ${statusText}</p>`;
            html += `<p>Total Violations: ${report.total_violations}</p>`;
            
            if (report.violations.length > 0) {
                html += '<h3>Violations Found:</h3>';
                report.violations.forEach(violation => {
                    html += `<div class="violation ${violation.severity}">
                        <strong>${violation.type.replace(/_/g, ' ').toUpperCase()}</strong><br>
                        ${violation.description}<br>
                        <strong>Section:</strong> ${violation.section}<br>
                        <strong>Penalty:</strong> ${violation.penalty}<br>
                        <strong>Recommended Fix:</strong> ${violation.fix}
                    </div>`;
                });
            }
            
            if (report.recommendations.length > 0) {
                html += '<h3>Recommendations:</h3><ul>';
                report.recommendations.forEach(rec => {
                    html += `<li>${rec}</li>`;
                });
                html += '</ul>';
            }
            
            contentDiv.innerHTML = html;
            resultsDiv.style.display = 'block';
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }
    </script>
</body>
</html>
        ''',
        
        'bulk_check.html': '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bulk Compliance Check</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; }
        .header { background-color: #2c3e50; color: white; padding: 15px 0; text-align: center; }
        .container { max-width: 800px; margin: 20px auto; padding: 0 20px; }
        .form-section { background: white; border-radius: 8px; padding: 30px; margin-bottom: 20px; }
        .upload-area { border: 2px dashed #ddd; border-radius: 10px; padding: 40px; text-align: center; margin: 20px 0; }
        .upload-area.dragover { border-color: #3498db; background-color: #f8f9fa; }
        .btn { background-color: #3498db; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin: 10px; }
        .btn:hover { background-color: #2980b9; }
        .results { background: white; border-radius: 8px; padding: 30px; margin-top: 20px; display: none; }
        .back-btn { display: inline-block; background-color: #95a5a6; color: white; padding: 8px 16px; text-decoration: none; border-radius: 3px; margin-bottom: 20px; }
        .progress { width: 100%; height: 20px; background-color: #ecf0f1; border-radius: 10px; overflow: hidden; margin: 20px 0; display: none; }
        .progress-bar { height: 100%; background-color: #3498db; width: 0%; transition: width 0.3s; }
        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .summary-card { background: #ecf0f1; padding: 20px; border-radius: 5px; text-align: center; }
        .download-links { margin-top: 20px; }
        .download-links a { display: inline-block; background-color: #27ae60; color: white; padding: 8px 16px; text-decoration: none; border-radius: 3px; margin: 5px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Bulk Compliance Check</h1>
    </div>
    
    <div class="container">
        <a href="/" class="back-btn">← Back to Dashboard</a>
        
        <div class="form-section">
            <h2>Upload Products File</h2>
            <p>Upload a JSON file containing your product listings for bulk compliance checking.</p>
            
            <div class="upload-area" id="uploadArea">
                <p>Drag & drop your JSON file here or click to browse</p>
                <input type="file" id="fileInput" accept=".json" style="display: none;">
                <button type="button" class="btn" onclick="document.getElementById('fileInput').click()">Choose File</button>
            </div>
            
            <div style="margin-top: 20px;">
                <label>Report Format:</label>
                <select id="reportFormat">
                    <option value="json">JSON</option>
                    <option value="html">HTML</option>
                    <option value="csv">CSV</option>
                </select>
                
                <button type="button" class="btn" id="checkBtn" disabled>Check Compliance</button>
            </div>
            
            <div class="progress" id="progress">
                <div class="progress-bar" id="progressBar"></div>
            </div>
        </div>
        
        <div class="results" id="results">
            <h2>Bulk Compliance Results</h2>
            <div id="results-content"></div>
        </div>
    </div>

    <script>
        let selectedFile = null;
        
        // File upload handling
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const checkBtn = document.getElementById('checkBtn');
        
        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', function(e) {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0 && files[0].name.endsWith('.json')) {
                handleFileSelect(files[0]);
            } else {
                alert('Please select a valid JSON file');
            }
        });
        
        fileInput.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                handleFileSelect(e.target.files[0]);
            }
        });
        
        function handleFileSelect(file) {
            selectedFile = file;
            uploadArea.innerHTML = `<p>Selected: ${file.name}</p><p>Size: ${(file.size/1024).toFixed(1)} KB</p>`;
            checkBtn.disabled = false;
        }
        
        // Bulk compliance check
        checkBtn.addEventListener('click', async function() {
            if (!selectedFile) return;
            
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('format', document.getElementById('reportFormat').value);
            
            // Show progress
            document.getElementById('progress').style.display = 'block';
            const progressBar = document.getElementById('progressBar');
            progressBar.style.width = '20%';
            
            try {
                const response = await fetch('/api/check-bulk', {
                    method: 'POST',
                    body: formData
                });
                
                progressBar.style.width = '80%';
                
                const result = await response.json();
                
                progressBar.style.width = '100%';
                
                if (result.success) {
                    displayBulkResults(result.report);
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Error processing file: ' + error.message);
            } finally {
                setTimeout(() => {
                    document.getElementById('progress').style.display = 'none';
                    progressBar.style.width = '0%';
                }, 1000);
            }
        });
        
        function displayBulkResults(report) {
            const resultsDiv = document.getElementById('results');
            const contentDiv = document.getElementById('results-content');
            
            const summary = report.summary;
            
            let html = '<h3>Summary Statistics</h3>';
            html += '<div class="summary-grid">';
            html += `<div class="summary-card"><h4>${summary.total_products}</h4><p>Total Products</p></div>`;
            html += `<div class="summary-card"><h4>${summary.compliant_products}</h4><p>Compliant</p></div>`;
            html += `<div class="summary-card"><h4>${summary.non_compliant_products}</h4><p>Non-Compliant</p></div>`;
            html += `<div class="summary-card"><h4>${summary.critical_violations}</h4><p>Critical Issues</p></div>`;
            html += '</div>';
            
            // Compliance rate
            const complianceRate = summary.total_products > 0 ? 
                ((summary.compliant_products / summary.total_products) * 100).toFixed(1) : 0;
            
            html += `<h3>Overall Compliance Rate: ${complianceRate}%</h3>`;
            
            // Download links
            html += '<div class="download-links">';
            html += '<h4>Download Reports:</h4>';
            report.files_generated.forEach(file => {
                html += `<a href="/download-report/${report.report_timestamp}" download="${file}">${file}</a>`;
            });
            html += '</div>';
            
            // Top violation types
            if (Object.keys(summary.violation_types).length > 0) {
                html += '<h3>Most Common Violations:</h3><ul>';
                const sortedViolations = Object.entries(summary.violation_types)
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, 5);
                
                sortedViolations.forEach(([type, count]) => {
                    html += `<li>${type.replace(/_/g, ' ').toUpperCase()}: ${count} occurrences</li>`;
                });
                html += '</ul>';
            }
            
            contentDiv.innerHTML = html;
            resultsDiv.style.display = 'block';
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }
    </script>
</body>
</html>
        '''
    }
    
    if template_name in templates:
        return templates[template_name]
    else:
        return "Template not found", 404

# Create Flask templates directory and files
def create_templates():
    """Create template files if they don't exist"""
    import os
    os.makedirs('templates', exist_ok=True)
    
    templates = {
        'templates/index.html': get_template('index.html'),
        'templates/single_check.html': get_template('single_check.html'),
        'templates/bulk_check.html': get_template('bulk_check.html')
    }
    
    for filepath, content in templates.items():
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    # Create templates directory and files
    create_templates()
    
    print("Starting Legal Metrology Compliance Web Application...")
    print("Open http://localhost:5000 in your browser")
    print("\nAvailable endpoints:")
    print("- / : Main dashboard")
    print("- /single-check : Single product compliance check")  
    print("- /bulk-check : Bulk compliance checking")
    print("- /api/check-single : API for single product check")
    print("- /api/check-bulk : API for bulk checking")
    print("- /api/rules : Get compliance rules")
    
    app.run(debug=True, host='0.0.0.0', port=5000)