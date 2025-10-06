"""
Legal Metrology Compliance Reporting and Alerting System

This module provides comprehensive reporting capabilities and alert management
for Legal Metrology compliance in e-commerce platforms.
"""

import json
import csv
import datetime
from typing import Dict, List, Any
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from compliance_checker import LegalMetrologyComplianceChecker, ViolationSeverity

class ComplianceReporter:
    """
    Generates various types of compliance reports and manages alerting
    """
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.checker = LegalMetrologyComplianceChecker()
        
    def generate_bulk_compliance_report(self, products: List[Dict[str, Any]], 
                                      report_format: str = "json") -> Dict[str, Any]:
        """
        Generate compliance report for multiple products
        
        Args:
            products: List of product dictionaries
            report_format: Output format ("json", "csv", "html")
            
        Returns:
            Summary report dictionary
        """
        results = []
        summary_stats = {
            "total_products": len(products),
            "compliant_products": 0,
            "non_compliant_products": 0,
            "critical_violations": 0,
            "high_violations": 0,
            "medium_violations": 0,
            "low_violations": 0,
            "violation_types": {}
        }
        
        for i, product in enumerate(products):
            product_id = product.get('id', f'product_{i+1}')
            violations = self.checker.check_product_listing(product)
            compliance_report = self.checker.generate_compliance_report(violations)
            
            result = {
                "product_id": product_id,
                "product_title": product.get('title', 'Unknown Product'),
                "compliance_status": compliance_report['status'],
                "total_violations": compliance_report['total_violations'],
                "violations": compliance_report['violations']
            }
            results.append(result)
            
            # Update summary statistics
            if compliance_report['status'] == 'COMPLIANT':
                summary_stats['compliant_products'] += 1
            else:
                summary_stats['non_compliant_products'] += 1
                
            # Count violations by severity
            for violation in violations:
                severity = violation.severity.value
                summary_stats[f'{severity}_violations'] += 1
                
                # Count violation types
                v_type = violation.violation_type
                if v_type not in summary_stats['violation_types']:
                    summary_stats['violation_types'][v_type] = 0
                summary_stats['violation_types'][v_type] += 1
        
        # Generate timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save report in requested format
        if report_format.lower() == "csv":
            self._save_csv_report(results, summary_stats, timestamp)
        elif report_format.lower() == "html":
            self._save_html_report(results, summary_stats, timestamp)
        else:
            self._save_json_report(results, summary_stats, timestamp)
            
        # Generate visualization
        self._generate_compliance_charts(summary_stats, timestamp)
        
        return {
            "summary": summary_stats,
            "detailed_results": results,
            "report_timestamp": timestamp,
            "files_generated": self._get_generated_files(timestamp, report_format)
        }
    
    def _save_json_report(self, results: List[Dict], summary: Dict, timestamp: str):
        """Save report as JSON"""
        report_data = {
            "report_metadata": {
                "generated_at": datetime.datetime.now().isoformat(),
                "report_type": "Legal Metrology Compliance Report",
                "total_products_analyzed": summary["total_products"]
            },
            "summary_statistics": summary,
            "detailed_results": results
        }
        
        filename = self.output_dir / f"compliance_report_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    def _save_csv_report(self, results: List[Dict], summary: Dict, timestamp: str):
        """Save report as CSV"""
        # Summary CSV
        summary_filename = self.output_dir / f"compliance_summary_{timestamp}.csv"
        with open(summary_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])
            for key, value in summary.items():
                if key != 'violation_types':
                    writer.writerow([key.replace('_', ' ').title(), value])
        
        # Detailed CSV
        details_filename = self.output_dir / f"compliance_details_{timestamp}.csv"
        if results:
            with open(details_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['product_id', 'product_title', 
                                                      'compliance_status', 'total_violations'])
                writer.writeheader()
                for result in results:
                    writer.writerow({
                        'product_id': result['product_id'],
                        'product_title': result['product_title'],
                        'compliance_status': result['compliance_status'],
                        'total_violations': result['total_violations']
                    })
    
    def _save_html_report(self, results: List[Dict], summary: Dict, timestamp: str):
        """Generate HTML compliance report"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Legal Metrology Compliance Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .summary {{ background-color: #e8f4f8; padding: 15px; margin: 20px 0; border-radius: 5px; }}
                .compliant {{ color: green; font-weight: bold; }}
                .non-compliant {{ color: red; font-weight: bold; }}
                .critical {{ background-color: #ffebee; }}
                .high {{ background-color: #fff3e0; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .violation {{ margin: 5px 0; padding: 5px; border-left: 3px solid #ccc; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Legal Metrology Compliance Report</h1>
                <p><strong>Generated:</strong> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p><strong>Total Products Analyzed:</strong> {summary['total_products']}</p>
            </div>
            
            <div class="summary">
                <h2>Summary Statistics</h2>
                <table>
                    <tr><td>Compliant Products</td><td class="compliant">{summary['compliant_products']}</td></tr>
                    <tr><td>Non-Compliant Products</td><td class="non-compliant">{summary['non_compliant_products']}</td></tr>
                    <tr><td>Critical Violations</td><td>{summary['critical_violations']}</td></tr>
                    <tr><td>High Violations</td><td>{summary['high_violations']}</td></tr>
                    <tr><td>Medium Violations</td><td>{summary['medium_violations']}</td></tr>
                    <tr><td>Low Violations</td><td>{summary['low_violations']}</td></tr>
                </table>
            </div>
            
            <h2>Product Details</h2>
            <table>
                <thead>
                    <tr>
                        <th>Product ID</th>
                        <th>Product Title</th>
                        <th>Compliance Status</th>
                        <th>Violations</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for result in results:
            status_class = "compliant" if result['compliance_status'] == 'COMPLIANT' else "non-compliant"
            row_class = "critical" if "CRITICAL" in result['compliance_status'] else ("high" if "HIGH" in result['compliance_status'] else "")
            
            html_content += f"""
                    <tr class="{row_class}">
                        <td>{result['product_id']}</td>
                        <td>{result['product_title']}</td>
                        <td class="{status_class}">{result['compliance_status']}</td>
                        <td>{result['total_violations']}</td>
                        <td>
            """
            
            for violation in result['violations']:
                html_content += f"""
                            <div class="violation">
                                <strong>{violation['type']}:</strong> {violation['description']}<br>
                                <small><strong>Fix:</strong> {violation['fix']}</small>
                            </div>
                """
            
            html_content += "</td></tr>"
        
        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """
        
        filename = self.output_dir / f"compliance_report_{timestamp}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _generate_compliance_charts(self, summary: Dict, timestamp: str):
        """Generate visualization charts"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Legal Metrology Compliance Analysis', fontsize=16)
        
        # Compliance Status Pie Chart
        compliance_data = [summary['compliant_products'], summary['non_compliant_products']]
        compliance_labels = ['Compliant', 'Non-Compliant']
        colors1 = ['#4CAF50', '#F44336']
        ax1.pie(compliance_data, labels=compliance_labels, autopct='%1.1f%%', colors=colors1)
        ax1.set_title('Compliance Status Distribution')
        
        # Violation Severity Bar Chart
        severities = ['Critical', 'High', 'Medium', 'Low']
        violation_counts = [
            summary['critical_violations'],
            summary['high_violations'], 
            summary['medium_violations'],
            summary['low_violations']
        ]
        colors2 = ['#D32F2F', '#FF9800', '#FFC107', '#4CAF50']
        ax2.bar(severities, violation_counts, color=colors2)
        ax2.set_title('Violations by Severity')
        ax2.set_ylabel('Number of Violations')
        
        # Top Violation Types
        if summary['violation_types']:
            top_violations = sorted(summary['violation_types'].items(), 
                                   key=lambda x: x[1], reverse=True)[:8]
            violation_names = [v[0].replace('_', ' ').title() for v in top_violations]
            violation_counts = [v[1] for v in top_violations]
            
            ax3.barh(violation_names, violation_counts, color='#2196F3')
            ax3.set_title('Most Common Violation Types')
            ax3.set_xlabel('Number of Occurrences')
        
        # Compliance Rate
        if summary['total_products'] > 0:
            compliance_rate = (summary['compliant_products'] / summary['total_products']) * 100
            ax4.bar(['Compliance Rate'], [compliance_rate], color='#4CAF50' if compliance_rate > 80 else '#FF9800')
            ax4.set_ylim(0, 100)
            ax4.set_ylabel('Percentage')
            ax4.set_title(f'Overall Compliance Rate: {compliance_rate:.1f}%')
            
            # Add text annotation
            ax4.text(0, compliance_rate + 5, f'{compliance_rate:.1f}%', 
                    ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        chart_filename = self.output_dir / f"compliance_charts_{timestamp}.png"
        plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _get_generated_files(self, timestamp: str, report_format: str) -> List[str]:
        """Get list of generated report files"""
        files = [f"compliance_charts_{timestamp}.png"]
        
        if report_format.lower() == "csv":
            files.extend([f"compliance_summary_{timestamp}.csv", 
                         f"compliance_details_{timestamp}.csv"])
        elif report_format.lower() == "html":
            files.append(f"compliance_report_{timestamp}.html")
        else:
            files.append(f"compliance_report_{timestamp}.json")
            
        return files
    
    def generate_alert_summary(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate alert summary for immediate attention items
        """
        critical_alerts = []
        high_priority_alerts = []
        
        for i, product in enumerate(products):
            product_id = product.get('id', f'product_{i+1}')
            violations = self.checker.check_product_listing(product)
            
            for violation in violations:
                alert_item = {
                    "product_id": product_id,
                    "product_title": product.get('title', 'Unknown Product'),
                    "violation_type": violation.violation_type,
                    "description": violation.description,
                    "penalty_risk": violation.penalty_info,
                    "recommended_action": violation.suggested_fix
                }
                
                if violation.severity == ViolationSeverity.CRITICAL:
                    critical_alerts.append(alert_item)
                elif violation.severity == ViolationSeverity.HIGH:
                    high_priority_alerts.append(alert_item)
        
        return {
            "critical_alerts": critical_alerts,
            "high_priority_alerts": high_priority_alerts,
            "total_critical": len(critical_alerts),
            "total_high_priority": len(high_priority_alerts),
            "requires_immediate_action": len(critical_alerts) > 0 or len(high_priority_alerts) > 0
        }

def bulk_compliance_check(products_file: str, output_format: str = "json") -> Dict[str, Any]:
    """
    Convenience function to perform bulk compliance checking from file
    
    Args:
        products_file: Path to JSON file containing product data
        output_format: Report format ("json", "csv", "html")
        
    Returns:
        Compliance report summary
    """
    try:
        with open(products_file, 'r', encoding='utf-8') as f:
            products = json.load(f)
    except Exception as e:
        return {"error": f"Failed to load products file: {str(e)}"}
    
    reporter = ComplianceReporter()
    return reporter.generate_bulk_compliance_report(products, output_format)

# Example usage
if __name__ == "__main__":
    # Sample products for testing
    sample_products = [
        {
            "id": "PROD001",
            "title": "Premium Basmati Rice",
            "weight": "5 kg",
            "dimensions": "30 x 20 x 10 cm",
            "price_per_unit": "₹200 per kg",
            "is_prepackaged": True,
            "net_quantity": "5 kg",
            "manufacturer_details": "ABC Foods Pvt Ltd"
        },
        {
            "id": "PROD002", 
            "title": "Organic Wheat Flour - 5 pounds",
            "weight": "5 lbs",
            "dimensions": "12 x 8 x 4 inches", 
            "price_per_unit": "₹150 per pound",
            "is_prepackaged": True,
            "net_quantity": "5 pounds"
        }
    ]
    
    # Generate reports
    reporter = ComplianceReporter()
    
    # Bulk compliance report
    bulk_report = reporter.generate_bulk_compliance_report(sample_products, "html")
    print("Bulk Compliance Report Generated:")
    print(f"- Total Products: {bulk_report['summary']['total_products']}")
    print(f"- Compliant: {bulk_report['summary']['compliant_products']}")
    print(f"- Non-Compliant: {bulk_report['summary']['non_compliant_products']}")
    
    # Alert summary
    alerts = reporter.generate_alert_summary(sample_products)
    print(f"\nAlert Summary:")
    print(f"- Critical Alerts: {alerts['total_critical']}")
    print(f"- High Priority Alerts: {alerts['total_high_priority']}")
    print(f"- Immediate Action Required: {alerts['requires_immediate_action']}")