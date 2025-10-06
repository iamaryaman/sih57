"""
Legal Metrology Compliance Checker for E-commerce Platforms

This module provides functionality to check e-commerce product listings
for compliance with the Legal Metrology Act 2009.
"""

import re
import json
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from legal_metrology_rules import get_compliance_rules_for_ecommerce, get_critical_sections_for_ecommerce

class ViolationSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ComplianceViolation:
    violation_type: str
    severity: ViolationSeverity
    description: str
    section_reference: str
    penalty_info: str
    suggested_fix: str
    field_name: str
    detected_value: str

class LegalMetrologyComplianceChecker:
    """
    Main class for checking e-commerce product listings against Legal Metrology Act requirements
    """
    
    def __init__(self):
        self.rules = get_compliance_rules_for_ecommerce()
        self.critical_sections = get_critical_sections_for_ecommerce()
        self.standard_units = self._load_standard_units()
        self.non_standard_patterns = self._load_non_standard_patterns()
        
    def _load_standard_units(self) -> Dict[str, List[str]]:
        """Load standard unit patterns for different measurement types"""
        return {
            "weight": ["kg", "kilogram", "kilograms", "g", "gram", "grams", "mg", "milligram", "milligrams"],
            "length": ["m", "meter", "metre", "meters", "metres", "cm", "centimeter", "centimetre", 
                      "centimeters", "centimetres", "mm", "millimeter", "millimetre", "millimeters", "millimetres"],
            "volume": ["l", "liter", "litre", "liters", "litres", "ml", "milliliter", "millilitre", 
                      "milliliters", "millilitres", "cc", "cubic centimeter", "cubic centimetre"],
            "area": ["sq m", "square meter", "square metre", "sq cm", "square centimeter", "square centimetre",
                    "sq mm", "square millimeter", "square millimetre"],
            "temperature": ["°c", "celsius", "k", "kelvin"]
        }
    
    def _load_non_standard_patterns(self) -> List[str]:
        """Load patterns for non-standard units commonly found in e-commerce"""
        return [
            # Weight
            r'\b(lb|lbs|pound|pounds|ounce|ounces|oz)\b',
            r'\b(stone|stones|ton|tons|tonne|tonnes)\b',
            # Length
            r'\b(ft|foot|feet|inch|inches|in|yard|yards|yd|mile|miles)\b',
            # Volume
            r'\b(gallon|gallons|gal|quart|quarts|qt|pint|pints|pt|fl oz|fluid ounce|fluid ounces)\b',
            # Traditional Indian units
            r'\b(ser|seer|maund|tola|ratti|chatak|pau|adhak|kos)\b',
            # Informal units
            r'\b(cup|cups|spoon|spoons|tablespoon|tablespoons|teaspoon|teaspoons|tbsp|tsp)\b',
            r'\b(piece|pieces|pcs|nos|number|numbers|dozen|gross)\b'
        ]
    
    def check_product_listing(self, product_data: Dict[str, Any]) -> List[ComplianceViolation]:
        """
        Check a single product listing for Legal Metrology compliance violations
        
        Args:
            product_data: Dictionary containing product information with keys like:
                - title, description, weight, dimensions, price, etc.
        
        Returns:
            List of ComplianceViolation objects
        """
        violations = []
        
        # Check weight/mass declarations
        violations.extend(self._check_weight_compliance(product_data))
        
        # Check dimension declarations
        violations.extend(self._check_dimension_compliance(product_data))
        
        # Check volume declarations
        violations.extend(self._check_volume_compliance(product_data))
        
        # Check pricing compliance
        violations.extend(self._check_pricing_compliance(product_data))
        
        # Check pre-packaged commodity requirements
        violations.extend(self._check_prepackaged_compliance(product_data))
        
        # Check advertising/description compliance
        violations.extend(self._check_description_compliance(product_data))
        
        return violations
    
    def _check_weight_compliance(self, product_data: Dict[str, Any]) -> List[ComplianceViolation]:
        """Check weight-related compliance"""
        violations = []
        weight_fields = ['weight', 'net_weight', 'gross_weight', 'package_weight']
        
        for field in weight_fields:
            if field in product_data and product_data[field]:
                weight_value = str(product_data[field]).lower()
                
                # Check for non-standard weight units
                if not self._contains_standard_unit(weight_value, 'weight'):
                    for pattern in self.non_standard_patterns:
                        if re.search(pattern, weight_value, re.IGNORECASE):
                            violations.append(ComplianceViolation(
                                violation_type="non_standard_weight_unit",
                                severity=ViolationSeverity.HIGH,
                                description=f"Non-standard weight unit detected in {field}",
                                section_reference="Section 11, 25",
                                penalty_info="Fine up to ₹25,000, imprisonment up to 6 months for repeat offenses",
                                suggested_fix="Use standard metric units: kg, g, mg",
                                field_name=field,
                                detected_value=product_data[field]
                            ))
                            break
        
        return violations
    
    def _check_dimension_compliance(self, product_data: Dict[str, Any]) -> List[ComplianceViolation]:
        """Check dimension-related compliance"""
        violations = []
        dimension_fields = ['length', 'width', 'height', 'dimensions', 'size']
        
        for field in dimension_fields:
            if field in product_data and product_data[field]:
                dimension_value = str(product_data[field]).lower()
                
                if not self._contains_standard_unit(dimension_value, 'length'):
                    for pattern in self.non_standard_patterns:
                        if re.search(pattern, dimension_value, re.IGNORECASE):
                            violations.append(ComplianceViolation(
                                violation_type="non_standard_length_unit",
                                severity=ViolationSeverity.HIGH,
                                description=f"Non-standard length unit detected in {field}",
                                section_reference="Section 11, 25",
                                penalty_info="Fine up to ₹25,000, imprisonment up to 6 months for repeat offenses",
                                suggested_fix="Use standard metric units: m, cm, mm",
                                field_name=field,
                                detected_value=product_data[field]
                            ))
                            break
        
        return violations
    
    def _check_volume_compliance(self, product_data: Dict[str, Any]) -> List[ComplianceViolation]:
        """Check volume-related compliance"""
        violations = []
        volume_fields = ['volume', 'capacity', 'contents', 'liquid_volume']
        
        for field in volume_fields:
            if field in product_data and product_data[field]:
                volume_value = str(product_data[field]).lower()
                
                if not self._contains_standard_unit(volume_value, 'volume'):
                    for pattern in self.non_standard_patterns:
                        if re.search(pattern, volume_value, re.IGNORECASE):
                            violations.append(ComplianceViolation(
                                violation_type="non_standard_volume_unit",
                                severity=ViolationSeverity.HIGH,
                                description=f"Non-standard volume unit detected in {field}",
                                section_reference="Section 11, 25",
                                penalty_info="Fine up to ₹25,000, imprisonment up to 6 months for repeat offenses",
                                suggested_fix="Use standard metric units: l, ml",
                                field_name=field,
                                detected_value=product_data[field]
                            ))
                            break
        
        return violations
    
    def _check_pricing_compliance(self, product_data: Dict[str, Any]) -> List[ComplianceViolation]:
        """Check pricing-related compliance"""
        violations = []
        
        # Check unit pricing
        if 'price_per_unit' in product_data:
            price_text = str(product_data['price_per_unit']).lower()
            
            # Check if price mentions non-standard units
            for pattern in self.non_standard_patterns:
                if re.search(pattern, price_text, re.IGNORECASE):
                    violations.append(ComplianceViolation(
                        violation_type="non_standard_unit_in_pricing",
                        severity=ViolationSeverity.CRITICAL,
                        description="Price per unit uses non-standard measurement units",
                        section_reference="Section 11",
                        penalty_info="Fine up to ₹10,000, imprisonment up to 1 year for repeat offenses",
                        suggested_fix="Quote prices only in standard metric units",
                        field_name="price_per_unit",
                        detected_value=product_data['price_per_unit']
                    ))
                    break
        
        return violations
    
    def _check_prepackaged_compliance(self, product_data: Dict[str, Any]) -> List[ComplianceViolation]:
        """Check pre-packaged commodity compliance"""
        violations = []
        
        # Check if product is pre-packaged
        is_prepackaged = product_data.get('is_prepackaged', False) or \
                        product_data.get('package_type') in ['box', 'bottle', 'can', 'packet', 'pouch']
        
        if is_prepackaged:
            required_fields = ['net_quantity', 'manufacturer_details', 'package_date']
            
            for field in required_fields:
                if field not in product_data or not product_data[field]:
                    violations.append(ComplianceViolation(
                        violation_type="missing_prepackaged_declaration",
                        severity=ViolationSeverity.HIGH,
                        description=f"Missing required declaration: {field}",
                        section_reference="Section 18",
                        penalty_info="Fine up to ₹1,00,000, imprisonment up to 1 year for repeat offenses",
                        suggested_fix=f"Add {field} to product listing",
                        field_name=field,
                        detected_value="Missing"
                    ))
        
        return violations
    
    def _check_description_compliance(self, product_data: Dict[str, Any]) -> List[ComplianceViolation]:
        """Check product description for non-standard units"""
        violations = []
        description_fields = ['title', 'description', 'features', 'specifications']
        
        for field in description_fields:
            if field in product_data and product_data[field]:
                text = str(product_data[field]).lower()
                
                # Check for non-standard units in descriptive text
                for pattern in self.non_standard_patterns:
                    if re.search(pattern, text, re.IGNORECASE):
                        violations.append(ComplianceViolation(
                            violation_type="non_standard_unit_in_description",
                            severity=ViolationSeverity.MEDIUM,
                            description=f"Non-standard units found in {field}",
                            section_reference="Section 11",
                            penalty_info="Fine up to ₹10,000, imprisonment up to 1 year for repeat offenses",
                            suggested_fix="Replace with standard metric units in product descriptions",
                            field_name=field,
                            detected_value=product_data[field]
                        ))
                        break
        
        return violations
    
    def _contains_standard_unit(self, text: str, unit_type: str) -> bool:
        """Check if text contains standard units of specified type"""
        if unit_type not in self.standard_units:
            return False
            
        standard_units = self.standard_units[unit_type]
        text_lower = text.lower()
        
        for unit in standard_units:
            if unit in text_lower:
                return True
        
        return False
    
    def generate_compliance_report(self, violations: List[ComplianceViolation]) -> Dict[str, Any]:
        """Generate a comprehensive compliance report"""
        if not violations:
            return {
                "status": "COMPLIANT",
                "total_violations": 0,
                "severity_breakdown": {},
                "violations": [],
                "recommendations": ["Product listing appears to be compliant with Legal Metrology Act 2009"]
            }
        
        # Count violations by severity
        severity_counts = {}
        for violation in violations:
            severity = violation.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Determine overall compliance status
        has_critical = any(v.severity == ViolationSeverity.CRITICAL for v in violations)
        has_high = any(v.severity == ViolationSeverity.HIGH for v in violations)
        
        if has_critical:
            status = "NON_COMPLIANT_CRITICAL"
        elif has_high:
            status = "NON_COMPLIANT_HIGH"
        else:
            status = "NON_COMPLIANT_MINOR"
        
        # Generate recommendations
        recommendations = []
        unique_violation_types = set(v.violation_type for v in violations)
        
        if "non_standard_weight_unit" in unique_violation_types:
            recommendations.append("Convert all weight measurements to metric units (kg, g, mg)")
        if "non_standard_length_unit" in unique_violation_types:
            recommendations.append("Convert all length measurements to metric units (m, cm, mm)")
        if "non_standard_volume_unit" in unique_violation_types:
            recommendations.append("Convert all volume measurements to metric units (l, ml)")
        if "missing_prepackaged_declaration" in unique_violation_types:
            recommendations.append("Add all required pre-packaged commodity declarations")
        
        return {
            "status": status,
            "total_violations": len(violations),
            "severity_breakdown": severity_counts,
            "violations": [
                {
                    "type": v.violation_type,
                    "severity": v.severity.value,
                    "description": v.description,
                    "section": v.section_reference,
                    "penalty": v.penalty_info,
                    "fix": v.suggested_fix,
                    "field": v.field_name,
                    "detected_value": v.detected_value
                } for v in violations
            ],
            "recommendations": recommendations
        }

def check_product_compliance(product_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to check a single product for compliance
    
    Args:
        product_data: Dictionary containing product information
        
    Returns:
        Compliance report dictionary
    """
    checker = LegalMetrologyComplianceChecker()
    violations = checker.check_product_listing(product_data)
    return checker.generate_compliance_report(violations)

# Example usage
if __name__ == "__main__":
    # Sample product data for testing
    sample_product = {
        "title": "Premium Rice - 5 pounds bag",
        "description": "High quality basmati rice, 5 lb package",
        "weight": "5 lbs",
        "dimensions": "12 x 8 x 4 inches",
        "price_per_unit": "₹200 per pound",
        "is_prepackaged": True,
        "net_quantity": "5 pounds"
    }
    
    # Check compliance
    report = check_product_compliance(sample_product)
    print(json.dumps(report, indent=2))