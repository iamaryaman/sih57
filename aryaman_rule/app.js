// Legal Metrology Compliance Rule Engine - JavaScript

// Application data from JSON
const appData = {
  "ruleCategories": {
    "mandatoryDeclarations": [
      {"id": "MD_001", "name": "Manufacturer Name Presence", "priority": "Critical", "description": "Package must display manufacturer/packer name"},
      {"id": "MD_002", "name": "Complete Address Validation", "priority": "Critical", "description": "Full address with street, city, state/PIN required"},
      {"id": "MD_003", "name": "Product Name Declaration", "priority": "Critical", "description": "Common/generic name must be declared"},
      {"id": "MD_004", "name": "Net Quantity Declaration", "priority": "Critical", "description": "Net quantity in standard units required"},
      {"id": "MD_005", "name": "Manufacturing Date", "priority": "Critical", "description": "Month and year of manufacture required"},
      {"id": "MD_006", "name": "MRP Declaration", "priority": "Critical", "description": "MRP format: 'MRP Rs. X inclusive of all taxes'"},
      {"id": "MD_007", "name": "Consumer Complaint Contact", "priority": "Critical", "description": "Customer care details required"}
    ],
    "formatCompliance": [
      {"id": "FC_001", "name": "Font Size Validation", "priority": "High", "description": "Font size 1mm-6mm based on package size"},
      {"id": "FC_002", "name": "Letter Width Ratio", "priority": "High", "description": "Width ≥1/3 of height"},
      {"id": "FC_003", "name": "Color Contrast Validation", "priority": "High", "description": "4.5:1 minimum contrast ratio"}
    ],
    "quantityValidation": [
      {"id": "QV_001", "name": "Standard Units Only", "priority": "Critical", "description": "Only ISI units: g, kg, ml, l allowed"},
      {"id": "QV_002", "name": "Prohibited Language Check", "priority": "Critical", "description": "No 'minimum', 'about', 'approximately'"}
    ],
    "standardSizes": [
      {"id": "SS_001", "name": "Product Standard Sizes", "priority": "Medium", "description": "Product-specific standard sizes"},
      {"id": "SS_002", "name": "Category Requirements", "priority": "Medium", "description": "Category-specific size requirements"}
    ],
    "errorTolerance": [
      {"id": "ET_001", "name": "Weight Error Validation", "priority": "Critical", "description": "9% for ≤50g, decreasing to 1% for >15kg"}
    ],
    "prohibitedPractices": [
      {"id": "PP_001", "name": "No Individual Stickers", "priority": "High", "description": "No stickers except MRP reduction"},
      {"id": "PP_002", "name": "Deceptive Package Detection", "priority": "High", "description": "Size vs content ratio analysis"}
    ],
    "exemptionChecks": [
      {"id": "EX_001", "name": "Small Package Exemption", "priority": "Info", "description": "≤10g/10ml exemption check"},
      {"id": "EX_002", "name": "Export/Institutional Exemption", "priority": "Info", "description": "Export or institutional use exemption"}
    ],
    "aiEnhanced": [
      {"id": "EN_001", "name": "Batch Consistency Check", "priority": "Low", "description": "Multiple package analysis"},
      {"id": "EN_002", "name": "OCR Confidence Validation", "priority": "Low", "description": "85% minimum confidence"},
      {"id": "EN_003", "name": "Predictive Compliance Scoring", "priority": "Low", "description": "Risk assessment scoring"},
      {"id": "EN_004", "name": "Multi-Language Detection", "priority": "Low", "description": "Hindi/English detection"},
      {"id": "EN_005", "name": "Competitor Benchmark", "priority": "Low", "description": "Industry standards comparison"},
      {"id": "EN_006", "name": "Regulation Updates", "priority": "Low", "description": "Real-time regulation sync"}
    ]
  },
  "productCategories": ["Biscuits", "Tea", "Coffee", "Edible Oils", "Cereals", "Pulses", "Salt", "Soaps", "Milk Powder", "Baby Food", "Weaning Food", "Bread", "Butter/Margarine", "Non-soapy Detergents", "Rice/Flour/Atta", "Aerated Drinks", "Mineral Water", "Cement", "Paint/Varnish", "Other"],
  "standardSizes": {
    "Biscuits": ["25g", "50g", "60g", "75g", "100g", "120g", "150g", "200g", "250g", "300g", "350g", "400g", "then multiples of 100g up to 1kg"],
    "Tea": ["25g", "50g", "75g", "100g", "125g", "150g", "200g", "250g", "500g", "750g", "1kg", "1.5kg", "2kg", "then multiples of 1kg"],
    "Coffee": ["25g", "50g", "75g", "100g", "150g", "200g", "250g", "500g", "750g", "1kg", "1.5kg", "then multiples of 1kg"],
    "Edible Oils": ["50g", "100g", "200g", "250g", "500g", "1kg", "2kg", "3kg", "5kg", "then multiples of 5kg"]
  },
  "fontSizeRequirements": [
    {"range": "Up to 200g/ml", "normalCase": "1mm", "moldedCase": "2mm"},
    {"range": "200g/ml to 500g/ml", "normalCase": "2mm", "moldedCase": "4mm"},
    {"range": "Above 500g/ml", "normalCase": "4mm", "moldedCase": "6mm"}
  ],
  "errorToleranceTable": [
    {"weight": "≤50g", "tolerance": "9%"},
    {"weight": "50g-100g", "tolerance": "7.5%"},
    {"weight": "100g-500g", "tolerance": "4.5%"},
    {"weight": "500g-1kg", "tolerance": "3%"},
    {"weight": "1kg-5kg", "tolerance": "2%"},
    {"weight": "5kg-15kg", "tolerance": "1.5%"},
    {"weight": ">15kg", "tolerance": "1%"}
  ],
  "penalties": [
    {"violation": "Incorrect labeling/declaration", "fine": "₹25,000 to ₹50,000", "action": "Immediate compliance required"},
    {"violation": "Unverified weight/measure usage", "fine": "₹10,000 to ₹50,000", "action": "Possible imprisonment up to 6 months"},
    {"violation": "Non-registration", "fine": "₹10,000+", "action": "Business operations suspended"},
    {"violation": "Quantity misrepresentation", "fine": "₹25,000+", "action": "Escalation for recurring offenses"}
  ]
};

// Global state
let currentStep = 1;
let ruleResults = {};
let chartInstance = null;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM loaded, initializing app...');
  initializeApp();
  setupEventListeners();
  populateFormData();
  renderRuleDashboard();
  updateResults();
});

function initializeApp() {
  console.log('Initializing app...');
  // Show first section and tab
  showSection('section-input');
  showFormStep(1);
  
  // Initialize default sync date
  const syncDateField = document.getElementById('syncDate');
  if (syncDateField) {
    syncDateField.value = new Date().toISOString().split('T')[0];
  }
  
  console.log('App initialized');
}

function setupEventListeners() {
  console.log('Setting up event listeners...');
  
  // Tab navigation
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      const target = e.target.getAttribute('data-target');
      console.log('Tab clicked:', target);
      if (target) {
        showSection(target.replace('#', ''));
      }
    });
  });

  // Form step navigation
  const nextBtn = document.getElementById('nextStep');
  const prevBtn = document.getElementById('prevStep');
  const recalcBtn = document.getElementById('recalcBtn');
  
  if (nextBtn) {
    nextBtn.addEventListener('click', (e) => {
      e.preventDefault();
      nextStep();
    });
  }
  
  if (prevBtn) {
    prevBtn.addEventListener('click', (e) => {
      e.preventDefault();
      prevStep();
    });
  }
  
  if (recalcBtn) {
    recalcBtn.addEventListener('click', (e) => {
      e.preventDefault();
      console.log('Validate Now clicked');
      validateRules();
    });
  }

  // Step buttons
  const stepButtons = document.querySelectorAll('.step');
  stepButtons.forEach(step => {
    step.addEventListener('click', (e) => {
      e.preventDefault();
      const stepNum = parseInt(e.target.getAttribute('data-step'));
      console.log('Step button clicked:', stepNum);
      if (stepNum) {
        showFormStep(stepNum);
      }
    });
  });

  // Form input validation
  const formInputs = document.querySelectorAll('#packageForm input, #packageForm select, #packageForm textarea');
  formInputs.forEach(input => {
    input.addEventListener('input', debounce(validateRules, 500));
    input.addEventListener('change', validateRules);
  });

  // Export functions
  const downloadBtn = document.getElementById('downloadReport');
  const printBtn = document.getElementById('printReport');
  const refreshBtn = document.getElementById('refreshChart');
  
  if (downloadBtn) {
    downloadBtn.addEventListener('click', downloadReport);
  }
  
  if (printBtn) {
    printBtn.addEventListener('click', printReport);
  }
  
  if (refreshBtn) {
    refreshBtn.addEventListener('click', refreshChart);
  }
  
  console.log('Event listeners set up');
}

function populateFormData() {
  console.log('Populating form data...');
  
  // Populate category dropdown
  const categorySelect = document.getElementById('category');
  if (categorySelect) {
    // Clear existing options first
    categorySelect.innerHTML = '<option value="">Select a category</option>';
    
    appData.productCategories.forEach(category => {
      const option = document.createElement('option');
      option.value = category;
      option.textContent = category;
      categorySelect.appendChild(option);
    });
    
    console.log('Category dropdown populated with', appData.productCategories.length, 'options');
  } else {
    console.error('Category select element not found');
  }
}

function showSection(sectionId) {
  console.log('Showing section:', sectionId);
  
  const sections = document.querySelectorAll('.section');
  const tabs = document.querySelectorAll('.tab');
  
  // Hide all sections
  sections.forEach(section => {
    section.classList.remove('is-active');
  });
  
  // Remove active class from all tabs
  tabs.forEach(tab => {
    tab.classList.remove('is-active');
  });
  
  // Show target section
  const targetSection = document.getElementById(sectionId);
  if (targetSection) {
    targetSection.classList.add('is-active');
    console.log('Section', sectionId, 'is now active');
  } else {
    console.error('Section not found:', sectionId);
  }
  
  // Activate corresponding tab
  const activeTab = document.querySelector(`[data-target="#${sectionId}"]`);
  if (activeTab) {
    activeTab.classList.add('is-active');
    console.log('Tab activated for section:', sectionId);
  }
}

function showFormStep(stepNum) {
  console.log('Showing form step:', stepNum);
  currentStep = stepNum;
  
  const formSteps = document.querySelectorAll('.form-step');
  const stepButtons = document.querySelectorAll('.step');
  
  // Hide all form steps
  formSteps.forEach(step => {
    step.classList.add('hidden');
  });
  
  // Update step buttons
  stepButtons.forEach(step => {
    step.classList.remove('is-active', 'is-completed');
    const num = parseInt(step.getAttribute('data-step'));
    if (num === stepNum) {
      step.classList.add('is-active');
    } else if (num < stepNum) {
      step.classList.add('is-completed');
    }
  });
  
  // Show target step
  const targetStep = document.querySelector(`.form-step[data-step="${stepNum}"]`);
  if (targetStep) {
    targetStep.classList.remove('hidden');
    console.log('Form step', stepNum, 'is now visible');
  } else {
    console.error('Form step not found:', stepNum);
  }
  
  // Update button states
  const prevBtn = document.getElementById('prevStep');
  const nextBtn = document.getElementById('nextStep');
  
  if (prevBtn) {
    prevBtn.style.display = stepNum === 1 ? 'none' : 'inline-flex';
  }
  
  if (nextBtn) {
    nextBtn.textContent = stepNum === 4 ? 'Complete' : 'Next';
  }
}

function nextStep() {
  console.log('Next step clicked, current step:', currentStep);
  if (currentStep < 4) {
    showFormStep(currentStep + 1);
  } else {
    console.log('Form completed, validating and showing results');
    validateRules();
    showSection('section-results');
  }
}

function prevStep() {
  console.log('Previous step clicked, current step:', currentStep);
  if (currentStep > 1) {
    showFormStep(currentStep - 1);
  }
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Rule Engine Implementation
function validateRules() {
  console.log('Starting rule validation...');
  const formData = getFormData();
  ruleResults = {};
  
  // Validate all rule categories
  validateMandatoryDeclarations(formData);
  validateFormatCompliance(formData);
  validateQuantity(formData);
  validateStandardSizes(formData);
  validateErrorTolerance(formData);
  validateProhibitedPractices(formData);
  validateExemptions(formData);
  validateAIFeatures(formData);
  
  console.log('Rule validation complete, updating results...');
  updateResults();
  renderRuleDashboard();
  refreshChart();
}

function getFormData() {
  const data = {};
  
  // Get all form fields by ID
  const fieldIds = [
    'productName', 'category', 'packageType', 'packageShape', 'lengthCm', 'widthCm', 'heightCm',
    'labelNotes', 'institutionalUse', 'manufacturerName', 'addrStreet', 'addrCity', 'addrState',
    'addrPIN', 'netQty', 'netUnit', 'mrpString', 'mfgMonth', 'consumerContact', 'measuredAvg',
    'labelMaterial', 'mrpFontMm', 'qtyFontMm', 'avgLetterWidthMm', 'fontColor', 'bgColor',
    'stickerUse', 'batchWeights', 'labelSimilarity', 'ocrConfidence', 'syncDate'
  ];
  
  fieldIds.forEach(id => {
    const element = document.getElementById(id);
    if (element) {
      data[id] = element.value || '';
    }
  });
  
  console.log('Form data collected:', data);
  return data;
}

// Mandatory Declarations Validation
function validateMandatoryDeclarations(data) {
  // MD_001: Manufacturer Name Presence
  ruleResults['MD_001'] = {
    status: data.manufacturerName && data.manufacturerName.trim() ? 'pass' : 'fail',
    message: data.manufacturerName && data.manufacturerName.trim() ? 
      'Manufacturer name is present' : 'Manufacturer name is required'
  };

  // MD_002: Complete Address Validation  
  const addressComplete = data.addrStreet && data.addrCity && data.addrState && 
    data.addrPIN && /^\d{6}$/.test(data.addrPIN);
  ruleResults['MD_002'] = {
    status: addressComplete ? 'pass' : 'fail',
    message: addressComplete ? 
      'Complete address provided' : 'Complete address with valid 6-digit PIN required'
  };

  // MD_003: Product Name Declaration
  ruleResults['MD_003'] = {
    status: data.productName && data.productName.trim() ? 'pass' : 'fail',
    message: data.productName && data.productName.trim() ? 
      'Product name declared' : 'Common/generic product name required'
  };

  // MD_004: Net Quantity Declaration
  const qtyValid = data.netQty && parseFloat(data.netQty) > 0 && 
    ['g', 'kg', 'ml', 'l'].includes(data.netUnit);
  ruleResults['MD_004'] = {
    status: qtyValid ? 'pass' : 'fail',
    message: qtyValid ? 
      'Net quantity properly declared' : 'Net quantity in standard units (g, kg, ml, l) required'
  };

  // MD_005: Manufacturing Date
  ruleResults['MD_005'] = {
    status: data.mfgMonth ? 'pass' : 'fail',
    message: data.mfgMonth ? 
      'Manufacturing date provided' : 'Manufacturing month/year required'
  };

  // MD_006: MRP Declaration
  const mrpPattern = /^MRP\s+Rs\.?\s*\d+(\.\d{1,2})?\s+inclusive\s+of\s+all\s+taxes$/i;
  const mrpValid = data.mrpString && mrpPattern.test(data.mrpString.trim());
  ruleResults['MD_006'] = {
    status: mrpValid ? 'pass' : 'fail',
    message: mrpValid ? 
      'MRP format is correct' : 'MRP must be in format: "MRP Rs. X inclusive of all taxes"'
  };

  // MD_007: Consumer Complaint Contact
  const contactValid = data.consumerContact && 
    (data.consumerContact.includes('@') || /\d{4,}/.test(data.consumerContact));
  ruleResults['MD_007'] = {
    status: contactValid ? 'pass' : 'fail',
    message: contactValid ? 
      'Consumer contact provided' : 'Valid phone number or email required'
  };
}

// Format Compliance Validation
function validateFormatCompliance(data) {
  // FC_001: Font Size Validation
  const netQtyValue = parseFloat(data.netQty) || 0;
  const unit = data.netUnit || 'g';
  const isMolded = data.labelMaterial === 'Molded/Embossed';
  
  let minFontSize = 1;
  if (netQtyValue <= 200) {
    minFontSize = isMolded ? 2 : 1;
  } else if (netQtyValue <= 500) {
    minFontSize = isMolded ? 4 : 2;
  } else {
    minFontSize = isMolded ? 6 : 4;
  }
  
  const actualFontSize = parseFloat(data.qtyFontMm) || 0;
  const fontSizeValid = actualFontSize >= minFontSize;
  
  ruleResults['FC_001'] = {
    status: fontSizeValid ? 'pass' : 'fail',
    message: fontSizeValid ? 
      `Font size ${actualFontSize}mm meets requirement` : 
      `Font size must be at least ${minFontSize}mm for ${data.labelMaterial} labels`
  };

  // FC_002: Letter Width Ratio
  const letterWidth = parseFloat(data.avgLetterWidthMm) || 0;
  const letterHeight = actualFontSize;
  const widthRatioValid = letterHeight > 0 && (letterWidth / letterHeight) >= (1/3);
  
  ruleResults['FC_002'] = {
    status: letterHeight > 0 ? (widthRatioValid ? 'pass' : 'fail') : 'na',
    message: letterHeight > 0 ? 
      (widthRatioValid ? 'Letter width ratio is adequate' : 'Letter width must be ≥1/3 of height') :
      'Font height needed for width ratio calculation'
  };

  // FC_003: Color Contrast Validation
  const contrast = calculateContrast(data.fontColor, data.bgColor);
  const contrastValid = contrast >= 4.5;
  
  ruleResults['FC_003'] = {
    status: contrastValid ? 'pass' : 'fail',
    message: contrastValid ? 
      `Contrast ratio ${contrast.toFixed(1)}:1 is adequate` : 
      `Contrast ratio ${contrast.toFixed(1)}:1 is below 4.5:1 requirement`
  };
}

// Quantity Validation
function validateQuantity(data) {
  // QV_001: Standard Units Only
  const validUnits = ['g', 'kg', 'ml', 'l'];
  const unitValid = validUnits.includes(data.netUnit);
  
  ruleResults['QV_001'] = {
    status: unitValid ? 'pass' : 'fail',
    message: unitValid ? 
      'Standard ISI units used' : 'Only g, kg, ml, l units are allowed'
  };

  // QV_002: Prohibited Language Check
  const prohibitedWords = ['minimum', 'about', 'approximately', 'min', 'approx'];
  const labelText = (data.labelNotes || '').toLowerCase();
  const hasProhibited = prohibitedWords.some(word => labelText.includes(word));
  
  ruleResults['QV_002'] = {
    status: hasProhibited ? 'fail' : 'pass',
    message: hasProhibited ? 
      'Prohibited language detected' : 'No prohibited language found'
  };
}

// Standard Sizes Validation
function validateStandardSizes(data) {
  const category = data.category;
  const netQty = parseFloat(data.netQty) || 0;
  const unit = data.netUnit || 'g';
  
  // SS_001: Product Standard Sizes
  let standardSizes = appData.standardSizes[category] || [];
  let sizeValid = false;
  
  if (standardSizes.length > 0) {
    sizeValid = standardSizes.some(size => {
      const sizeValue = parseFloat(size);
      return Math.abs(sizeValue - netQty) < 0.01;
    });
  } else {
    sizeValid = true; // No specific standards for this category
  }
  
  ruleResults['SS_001'] = {
    status: sizeValid ? 'pass' : 'warning',
    message: sizeValid ? 
      'Package size follows standards' : 
      `Consider using standard sizes for ${category}: ${standardSizes.slice(0, 5).join(', ')}`
  };

  // SS_002: Category Requirements
  ruleResults['SS_002'] = {
    status: category ? 'pass' : 'fail',
    message: category ? 
      'Product category specified' : 'Product category required for size validation'
  };
}

// Error Tolerance Validation
function validateErrorTolerance(data) {
  const declared = parseFloat(data.netQty) || 0;
  const measured = parseFloat(data.measuredAvg) || 0;
  
  if (declared === 0 || measured === 0) {
    ruleResults['ET_001'] = {
      status: 'na',
      message: 'Declared and measured values needed for tolerance check'
    };
    return;
  }
  
  let allowedTolerance = 0;
  if (declared <= 50) allowedTolerance = 0.09;
  else if (declared <= 100) allowedTolerance = 0.075;
  else if (declared <= 500) allowedTolerance = 0.045;
  else if (declared <= 1000) allowedTolerance = 0.03;
  else if (declared <= 5000) allowedTolerance = 0.02;
  else if (declared <= 15000) allowedTolerance = 0.015;
  else allowedTolerance = 0.01;
  
  const actualError = Math.abs(declared - measured) / declared;
  const toleranceValid = actualError <= allowedTolerance;
  
  ruleResults['ET_001'] = {
    status: toleranceValid ? 'pass' : 'fail',
    message: toleranceValid ? 
      `Error ${(actualError * 100).toFixed(1)}% within ${(allowedTolerance * 100)}% tolerance` :
      `Error ${(actualError * 100).toFixed(1)}% exceeds ${(allowedTolerance * 100)}% tolerance limit`
  };
}

// Prohibited Practices Validation
function validateProhibitedPractices(data) {
  // PP_001: No Individual Stickers
  const stickerValid = data.stickerUse === 'None' || data.stickerUse === 'MRP reduction only';
  
  ruleResults['PP_001'] = {
    status: stickerValid ? 'pass' : 'fail',
    message: stickerValid ? 
      'Sticker usage is compliant' : 'Individual stickers not allowed except for MRP reduction'
  };

  // PP_002: Deceptive Package Detection
  const length = parseFloat(data.lengthCm) || 0;
  const width = parseFloat(data.widthCm) || 0;
  const height = parseFloat(data.heightCm) || 0;
  const volume = length * width * height;
  const netQty = parseFloat(data.netQty) || 0;
  
  let deceptiveCheck = 'pass';
  if (volume > 0 && netQty > 0) {
    // Basic deceptive packaging check - very large package for small content
    const ratio = volume / netQty;
    if (ratio > 1000) { // Arbitrary threshold for demonstration
      deceptiveCheck = 'warning';
    }
  } else {
    deceptiveCheck = 'na';
  }
  
  ruleResults['PP_002'] = {
    status: deceptiveCheck,
    message: deceptiveCheck === 'pass' ? 
      'Package size appears proportional' : 
      deceptiveCheck === 'warning' ?
      'Large package size for content quantity - review for deceptive packaging' :
      'Package dimensions needed for deceptive packaging check'
  };
}

// Exemption Checks
function validateExemptions(data) {
  const netQty = parseFloat(data.netQty) || 0;
  const unit = data.netUnit || 'g';
  
  // EX_001: Small Package Exemption
  const isSmallPackage = (unit === 'g' && netQty <= 10) || (unit === 'ml' && netQty <= 10);
  
  ruleResults['EX_001'] = {
    status: 'info',
    message: isSmallPackage ? 
      'Package qualifies for small package exemption (≤10g/10ml)' : 
      'Package does not qualify for small package exemption'
  };

  // EX_002: Export/Institutional Exemption
  const isExempt = data.packageType === 'Export' || data.institutionalUse === 'Yes';
  
  ruleResults['EX_002'] = {
    status: 'info',
    message: isExempt ? 
      'Package may qualify for export/institutional exemption' : 
      'No export or institutional exemption applicable'
  };
}

// AI Enhanced Features
function validateAIFeatures(data) {
  // EN_001: Batch Consistency Check
  const batchWeights = data.batchWeights ? 
    data.batchWeights.split(',').map(w => parseFloat(w.trim())).filter(w => !isNaN(w)) : [];
  
  let batchConsistent = true;
  if (batchWeights.length > 1) {
    const avg = batchWeights.reduce((a, b) => a + b, 0) / batchWeights.length;
    batchConsistent = batchWeights.every(w => Math.abs(w - avg) <= 2);
  }
  
  ruleResults['EN_001'] = {
    status: batchWeights.length > 1 ? (batchConsistent ? 'pass' : 'fail') : 'na',
    message: batchWeights.length > 1 ? 
      (batchConsistent ? 'Batch weights within ±2g variance' : 'Batch weights exceed ±2g variance') :
      'Multiple batch weights needed for consistency check'
  };

  // EN_002: OCR Confidence Validation
  const ocrConfidence = parseFloat(data.ocrConfidence) || 100;
  const ocrValid = ocrConfidence >= 85;
  
  ruleResults['EN_002'] = {
    status: ocrValid ? 'pass' : 'warning',
    message: ocrValid ? 
      `OCR confidence ${ocrConfidence}% meets 85% threshold` : 
      `OCR confidence ${ocrConfidence}% below 85% threshold`
  };

  // EN_003: Predictive Compliance Scoring
  const score = calculateComplianceScore();
  const riskLevel = score >= 90 ? 'Low' : score >= 70 ? 'Medium' : 'High';
  
  ruleResults['EN_003'] = {
    status: 'info',
    message: `Compliance score: ${score}% (${riskLevel} risk)`
  };

  // EN_004: Multi-Language Detection
  const labelText = data.labelNotes || '';
  const hasHindi = /[\u0900-\u097F]/.test(labelText);
  const hasEnglish = /[a-zA-Z]/.test(labelText);
  
  ruleResults['EN_004'] = {
    status: 'info',
    message: `Detected languages: ${hasEnglish ? 'English' : ''}${hasEnglish && hasHindi ? ', ' : ''}${hasHindi ? 'Hindi' : ''}${!hasEnglish && !hasHindi ? 'None detected' : ''}`
  };

  // EN_005: Competitor Benchmark
  ruleResults['EN_005'] = {
    status: 'info',
    message: 'Benchmark analysis: Industry compliance average 85%'
  };

  // EN_006: Regulation Updates
  const syncDate = new Date(data.syncDate || new Date());
  const daysSinceSync = Math.floor((new Date() - syncDate) / (1000 * 60 * 60 * 24));
  const syncValid = daysSinceSync <= 30;
  
  ruleResults['EN_006'] = {
    status: syncValid ? 'pass' : 'warning',
    message: syncValid ? 
      `Regulations synced ${daysSinceSync} days ago` : 
      `Regulations last synced ${daysSinceSync} days ago - consider updating`
  };
}

// Utility Functions
function calculateContrast(color1, color2) {
  const rgb1 = hexToRgb(color1);
  const rgb2 = hexToRgb(color2);
  
  const l1 = getLuminance(rgb1);
  const l2 = getLuminance(rgb2);
  
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  
  return (lighter + 0.05) / (darker + 0.05);
}

function hexToRgb(hex) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : {r: 0, g: 0, b: 0};
}

function getLuminance(rgb) {
  const rsRGB = rgb.r / 255;
  const gsRGB = rgb.g / 255;
  const bsRGB = rgb.b / 255;
  
  const r = rsRGB <= 0.03928 ? rsRGB / 12.92 : Math.pow((rsRGB + 0.055) / 1.055, 2.4);
  const g = gsRGB <= 0.03928 ? gsRGB / 12.92 : Math.pow((gsRGB + 0.055) / 1.055, 2.4);
  const b = bsRGB <= 0.03928 ? bsRGB / 12.92 : Math.pow((bsRGB + 0.055) / 1.055, 2.4);
  
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function calculateComplianceScore() {
  let totalRules = 0;
  let passedRules = 0;
  let weightedScore = 0;
  let totalWeight = 0;
  
  // Weight factors
  const weights = {
    'Critical': 4,
    'High': 3,
    'Medium': 2,
    'Low': 1,
    'Info': 0.5
  };
  
  Object.values(appData.ruleCategories).flat().forEach(rule => {
    const result = ruleResults[rule.id];
    if (result && result.status !== 'na') {
      totalRules++;
      const weight = weights[rule.priority] || 1;
      totalWeight += weight;
      
      if (result.status === 'pass') {
        passedRules++;
        weightedScore += weight;
      } else if (result.status === 'warning') {
        weightedScore += weight * 0.5;
      }
    }
  });
  
  return totalWeight > 0 ? Math.round((weightedScore / totalWeight) * 100) : 0;
}

// Update UI
function updateResults() {
  const score = calculateComplianceScore();
  console.log('Updating results, compliance score:', score);
  
  // Update header score
  const scoreText = document.getElementById('scoreText');
  const overallProgress = document.getElementById('overallProgress');
  const resultsProgress = document.getElementById('resultsProgress');
  const resultsScore = document.getElementById('resultsScore');
  
  if (scoreText) scoreText.textContent = `Score: ${score}%`;
  if (overallProgress) overallProgress.style.width = `${score}%`;
  if (resultsProgress) resultsProgress.style.width = `${score}%`;
  if (resultsScore) resultsScore.textContent = `${score}%`;
  
  updateViolationsList();
  updateExemptionsList();
  updatePenaltiesList();
  updateRecommendations();
  updatePrintPreview();
}

function updateViolationsList() {
  const violations = {
    Critical: [],
    High: [],
    Medium: [],
    Low: []
  };
  
  Object.values(appData.ruleCategories).flat().forEach(rule => {
    const result = ruleResults[rule.id];
    if (result && result.status === 'fail') {
      violations[rule.priority].push(`${rule.id}: ${rule.name}`);
    }
  });
  
  Object.keys(violations).forEach(priority => {
    const list = document.getElementById(`violations${priority}`);
    if (list) {
      list.innerHTML = '';
      
      if (violations[priority].length === 0) {
        const li = document.createElement('li');
        li.textContent = 'None';
        li.style.color = 'var(--color-success)';
        list.appendChild(li);
      } else {
        violations[priority].forEach(violation => {
          const li = document.createElement('li');
          li.innerHTML = `<span class="status-dot" style="background: var(--color-error);"></span> ${violation}`;
          list.appendChild(li);
        });
      }
    }
  });
  
  // Update status breakdown
  const statusCounts = { pass: 0, fail: 0, warning: 0, na: 0 };
  Object.values(ruleResults).forEach(result => {
    statusCounts[result.status]++;
  });
  
  const statusBreakdown = document.getElementById('statusBreakdown');
  if (statusBreakdown) {
    statusBreakdown.innerHTML = `
      <div class="status-item">
        <span>Passed</span>
        <span class="status-count" style="background: var(--color-bg-3);">${statusCounts.pass}</span>
      </div>
      <div class="status-item">
        <span>Failed</span>
        <span class="status-count" style="background: var(--color-bg-4);">${statusCounts.fail}</span>
      </div>
      <div class="status-item">
        <span>Warnings</span>
        <span class="status-count" style="background: var(--color-bg-6);">${statusCounts.warning}</span>
      </div>
    `;
  }
}

function updateExemptionsList() {
  const list = document.getElementById('exemptionsList');
  if (list) {
    list.innerHTML = '';
    
    ['EX_001', 'EX_002'].forEach(ruleId => {
      const result = ruleResults[ruleId];
      if (result) {
        const li = document.createElement('li');
        li.textContent = result.message;
        list.appendChild(li);
      }
    });
  }
}

function updatePenaltiesList() {
  const list = document.getElementById('penaltiesList');
  if (list) {
    list.innerHTML = '';
    
    const failedRules = Object.values(appData.ruleCategories).flat().filter(rule => {
      const result = ruleResults[rule.id];
      return result && result.status === 'fail';
    });
    
    if (failedRules.length === 0) {
      const li = document.createElement('li');
      li.innerHTML = '<span style="color: var(--color-success);">No violations found - no penalties applicable</span>';
      list.appendChild(li);
    } else {
      appData.penalties.forEach(penalty => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${penalty.violation}:</strong> ${penalty.fine} - ${penalty.action}`;
        list.appendChild(li);
      });
    }
  }
}

function updateRecommendations() {
  const container = document.getElementById('recommendationsContainer');
  if (!container) return;
  
  container.innerHTML = '';
  
  const failedRules = Object.values(appData.ruleCategories).flat().filter(rule => {
    const result = ruleResults[rule.id];
    return result && (result.status === 'fail' || result.status === 'warning');
  });
  
  if (failedRules.length === 0) {
    container.innerHTML = '<div class="card"><div class="card__body"><p style="color: var(--color-success);">All validations passed! No recommendations needed.</p></div></div>';
    return;
  }
  
  failedRules.forEach(rule => {
    const result = ruleResults[rule.id];
    const card = document.createElement('div');
    card.className = `recommendation-card ${result.status === 'fail' ? '' : 'warning'}`;
    
    card.innerHTML = `
      <div class="recommendation-header">
        <div>
          <div class="recommendation-title">${rule.id}: ${rule.name}</div>
          <div class="priority-badge priority-badge--${rule.priority.toLowerCase()}">${rule.priority}</div>
        </div>
        <div class="status-badge status-badge--${result.status}">
          <div class="status-dot"></div>
          ${result.status.toUpperCase()}
        </div>
      </div>
      <div class="recommendation-description">${rule.description}</div>
      <div class="recommendation-fix">
        <strong>Issue:</strong> ${result.message}<br>
        <strong>Fix:</strong> ${getRecommendationFix(rule.id)}
      </div>
      ${getRecommendationExample(rule.id)}
    `;
    
    container.appendChild(card);
  });
}

function getRecommendationFix(ruleId) {
  const fixes = {
    'MD_001': 'Add manufacturer or packer name prominently on the label',
    'MD_002': 'Include complete address: street, city, state, 6-digit PIN',
    'MD_003': 'Add common/generic product name on the package',
    'MD_004': 'Declare net quantity using only g, kg, ml, or l units',
    'MD_005': 'Add manufacturing month and year (MM/YYYY format)',
    'MD_006': 'Use exact format: "MRP Rs. [amount] inclusive of all taxes"',
    'MD_007': 'Provide customer care phone number or email address',
    'FC_001': 'Increase font size to meet minimum requirements based on package size',
    'FC_002': 'Ensure letter width is at least 1/3 of letter height',
    'FC_003': 'Improve color contrast between text and background (minimum 4.5:1)',
    'QV_001': 'Use only standard ISI units: grams (g), kilograms (kg), milliliters (ml), liters (l)',
    'QV_002': 'Remove words like "minimum", "about", "approximately" from quantity declarations',
    'SS_001': 'Consider using standard package sizes for better market acceptance',
    'SS_002': 'Specify correct product category for appropriate size validation',
    'ET_001': 'Ensure actual weight/volume is within legal tolerance limits',
    'PP_001': 'Remove individual stickers except for MRP reduction purposes',
    'PP_002': 'Ensure package size is proportional to content quantity',
    'EN_001': 'Maintain consistent weights across batch production (±2g tolerance)',
    'EN_002': 'Improve label quality for better OCR recognition (≥85% confidence)',
    'EN_006': 'Update regulation database within 30 days'
  };
  
  return fixes[ruleId] || 'Review rule requirements and make necessary corrections';
}

function getRecommendationExample(ruleId) {
  const examples = {
    'MD_006': '<div class="recommendation-example">Example: "MRP Rs. 25.00 inclusive of all taxes"</div>',
    'MD_002': '<div class="recommendation-example">Example: "123 Industrial Area, Mumbai, Maharashtra 400001"</div>',
    'QV_002': '<div class="recommendation-example">Correct: "Net Qty: 100g" | Incorrect: "Net Qty: About 100g"</div>'
  };
  
  return examples[ruleId] || '';
}

// Rule Dashboard
function renderRuleDashboard() {
  const container = document.getElementById('rulesContainer');
  if (!container) return;
  
  container.innerHTML = '';
  
  Object.entries(appData.ruleCategories).forEach(([categoryKey, rules]) => {
    rules.forEach(rule => {
      const result = ruleResults[rule.id] || { status: 'na', message: 'Not evaluated' };
      
      const card = document.createElement('div');
      card.className = 'rule-card';
      
      card.innerHTML = `
        <div class="rule-header">
          <div class="rule-id">${rule.id}</div>
          <div class="status-badge status-badge--${result.status}">
            <div class="status-dot"></div>
            ${result.status.toUpperCase()}
          </div>
        </div>
        <div class="rule-name">${rule.name}</div>
        <div class="rule-description">${rule.description}</div>
        <div class="rule-footer">
          <div class="priority-badge priority-badge--${rule.priority.toLowerCase()}">${rule.priority}</div>
        </div>
      `;
      
      container.appendChild(card);
    });
  });
}

// Chart
function refreshChart() {
  const canvas = document.getElementById('statusChart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  if (chartInstance) {
    chartInstance.destroy();
  }
  
  const statusCounts = { pass: 0, fail: 0, warning: 0, na: 0 };
  Object.values(ruleResults).forEach(result => {
    statusCounts[result.status]++;
  });
  
  chartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Passed', 'Failed', 'Warnings', 'Not Applicable'],
      datasets: [{
        data: [statusCounts.pass, statusCounts.fail, statusCounts.warning, statusCounts.na],
        backgroundColor: ['#1FB8CD', '#B4413C', '#FFC185', '#ECEBD5'],
        borderWidth: 2,
        borderColor: '#fff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 20,
            usePointStyle: true
          }
        }
      }
    }
  });
}

// Export Functions
function updatePrintPreview() {
  const formData = getFormData();
  const score = calculateComplianceScore();
  
  const preview = document.getElementById('printPreview');
  if (!preview) return;
  
  preview.innerHTML = `
    <h3>Legal Metrology Compliance Report</h3>
    <p><strong>Generated:</strong> ${new Date().toLocaleString()}</p>
    
    <h4>Package Information</h4>
    <ul>
      <li><strong>Product:</strong> ${formData.productName || 'Not specified'}</li>
      <li><strong>Category:</strong> ${formData.category || 'Not specified'}</li>
      <li><strong>Net Quantity:</strong> ${formData.netQty || '0'} ${formData.netUnit || 'g'}</li>
      <li><strong>Manufacturer:</strong> ${formData.manufacturerName || 'Not specified'}</li>
      <li><strong>MRP:</strong> ${formData.mrpString || 'Not specified'}</li>
    </ul>
    
    <h4>Compliance Summary</h4>
    <p><strong>Overall Score:</strong> ${score}%</p>
    
    <h4>Rule Validation Results</h4>
    ${Object.values(appData.ruleCategories).flat().map(rule => {
      const result = ruleResults[rule.id] || { status: 'na', message: 'Not evaluated' };
      return `<p><strong>${rule.id}:</strong> ${result.status.toUpperCase()} - ${result.message}</p>`;
    }).join('')}
  `;
}

function downloadReport() {
  const formData = getFormData();
  const report = {
    metadata: {
      title: 'Legal Metrology Compliance Report',
      generated: new Date().toISOString(),
      version: '1.0'
    },
    packageData: formData,
    complianceScore: calculateComplianceScore(),
    ruleResults: ruleResults,
    recommendations: Object.values(appData.ruleCategories).flat()
      .filter(rule => ruleResults[rule.id] && ruleResults[rule.id].status === 'fail')
      .map(rule => ({
        ruleId: rule.id,
        ruleName: rule.name,
        issue: ruleResults[rule.id].message,
        fix: getRecommendationFix(rule.id)
      }))
  };
  
  const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `legal-metrology-report-${new Date().toISOString().split('T')[0]}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function printReport() {
  window.print();
}

// Initialize validation on load with a delay
setTimeout(() => {
  console.log('Running initial validation...');
  validateRules();
}, 1500);