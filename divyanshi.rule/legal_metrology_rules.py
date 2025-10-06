"""
Legal Metrology Act 2009 - Key Rules Extraction for E-commerce Compliance

This module contains the extracted rules and requirements from the Legal Metrology Act 2009
that are relevant for e-commerce platforms and online retailers.
"""

# Standard Units and Measurements (Sections 4-12)
STANDARD_UNITS = {
    "base_units": {
        "length": "metre",
        "mass": "kilogram", 
        "time": "second",
        "electric_current": "ampere",
        "temperature": "kelvin",
        "luminous_intensity": "candela",
        "amount_of_substance": "mole"
    },
    "numeration": "international form of Indian numerals (decimal system)",
    "system": "metric system based on international system of units"
}

# Pre-packaged Commodity Requirements (Section 18)
PREPACKAGED_REQUIREMENTS = {
    "mandatory_declarations": [
        "net_quantity",
        "standard_quantities_or_number",
        "prescribed_particulars",
        "prescribed_manner_of_display"
    ],
    "advertising_requirements": [
        "retail_sale_price_declaration",
        "net_quantity_declaration",
        "prescribed_form_and_manner"
    ]
}

# Prohibited Practices (Sections 11, 25-47)
PROHIBITED_PRACTICES = {
    "quotation_violations": {
        "section": 11,
        "description": "Using non-standard units in price quotes, announcements, invoices, advertisements",
        "penalty": "Fine up to ₹10,000, imprisonment up to 1 year for repeat offenses"
    },
    "non_standard_weights": {
        "section": 25,
        "description": "Using non-standard weights or measures",
        "penalty": "Fine up to ₹25,000, imprisonment up to 6 months for repeat offenses"
    },
    "transaction_violations": {
        "section": 30,
        "description": "Short delivery, excess billing, fraudulent transactions",
        "penalty": "Fine up to ₹10,000, imprisonment up to 1 year for repeat offenses"
    },
    "prepackaged_violations": {
        "section": 36,
        "description": "Non-compliant pre-packaged commodities",
        "penalty": "Fine up to ₹1,00,000, imprisonment up to 1 year for repeat offenses"
    }
}

# E-commerce Specific Compliance Requirements
ECOMMERCE_COMPLIANCE = {
    "product_listings": {
        "weight_declaration": "Must use standard metric units (kg, g, mg)",
        "dimension_declaration": "Must use standard metric units (m, cm, mm)",
        "volume_declaration": "Must use standard metric units (l, ml)",
        "quantity_declaration": "Must use decimal system for numbering"
    },
    "pricing": {
        "unit_price_display": "Must quote prices in standard units only",
        "bulk_pricing": "Must use standard weights/measures for bulk offers",
        "comparison_pricing": "All price comparisons must use standard units"
    },
    "advertising": {
        "promotional_content": "Must not use non-standard units in advertisements",
        "sale_announcements": "Must declare net quantity in standard units",
        "discount_offers": "Must calculate discounts based on standard measures"
    }
}

# Penalties and Fines Structure
PENALTY_STRUCTURE = {
    "minor_violations": {
        "range": "₹2,000 - ₹25,000",
        "examples": ["Non-standard unit usage", "Documentation errors"]
    },
    "major_violations": {
        "range": "₹25,000 - ₹1,00,000",
        "imprisonment": "Up to 1 year",
        "examples": ["Fraudulent transactions", "Prepackaged commodity violations"]
    },
    "repeat_offenses": {
        "imprisonment": "6 months to 5 years",
        "additional_penalties": "Publication of company name and violations"
    }
}

# Verification Requirements (Sections 24, 33)
VERIFICATION_REQUIREMENTS = {
    "weighing_instruments": {
        "mandatory_verification": True,
        "verification_authority": "Controller of Legal Metrology",
        "penalty_for_unverified": "Fine ₹2,000 - ₹10,000, imprisonment up to 1 year"
    },
    "measuring_instruments": {
        "mandatory_verification": True,
        "verification_authority": "Government approved Test Centre",
        "penalty_for_unverified": "Fine ₹2,000 - ₹10,000, imprisonment up to 1 year"
    }
}

# Registration Requirements (Section 19)
REGISTRATION_REQUIREMENTS = {
    "importers": {
        "mandatory_registration": True,
        "authority": "Director of Legal Metrology",
        "penalty_for_non_registration": "Fine up to ₹25,000, imprisonment up to 6 months"
    },
    "manufacturers": {
        "license_required": True,
        "authority": "Controller of Legal Metrology",
        "penalty_for_unlicensed": "Fine up to ₹20,000, imprisonment up to 1 year"
    }
}

def get_compliance_rules_for_ecommerce():
    """
    Returns a comprehensive set of compliance rules specifically for e-commerce platforms
    """
    return {
        "standard_units": STANDARD_UNITS,
        "prepackaged_requirements": PREPACKAGED_REQUIREMENTS,
        "prohibited_practices": PROHIBITED_PRACTICES,
        "ecommerce_compliance": ECOMMERCE_COMPLIANCE,
        "penalty_structure": PENALTY_STRUCTURE,
        "verification_requirements": VERIFICATION_REQUIREMENTS,
        "registration_requirements": REGISTRATION_REQUIREMENTS
    }

def get_critical_sections_for_ecommerce():
    """
    Returns the most critical sections of the Legal Metrology Act for e-commerce compliance
    """
    return {
        "Section 11": "Prohibition of non-standard units in pricing and advertising",
        "Section 18": "Pre-packaged commodity declaration requirements", 
        "Section 25": "Penalty for using non-standard weights/measures",
        "Section 30": "Penalty for fraudulent transactions",
        "Section 36": "Penalty for non-compliant packaging",
        "Section 41": "Penalty for false information/returns"
    }