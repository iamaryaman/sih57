import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Parse the data
data = {
    "categories": ["Mandatory Declarations", "Format Compliance", "Quantity Validation", "Standard Sizes", "Error Tolerance", "Prohibited Practices", "Exemption Checks", "AI-Enhanced Features"],
    "rules": [
        {"id": "MD_001", "name": "Manufacturer Name Presence", "category": "Mandatory Declarations", "priority": "Critical"},
        {"id": "MD_002", "name": "Complete Address Validation", "category": "Mandatory Declarations", "priority": "Critical"},
        {"id": "MD_003", "name": "Product Name Declaration", "category": "Mandatory Declarations", "priority": "Critical"},
        {"id": "MD_004", "name": "Net Quantity Declaration", "category": "Mandatory Declarations", "priority": "Critical"},
        {"id": "MD_005", "name": "Manufacturing Date", "category": "Mandatory Declarations", "priority": "Critical"},
        {"id": "MD_006", "name": "MRP Declaration", "category": "Mandatory Declarations", "priority": "Critical"},
        {"id": "MD_007", "name": "Consumer Complaint Contact", "category": "Mandatory Declarations", "priority": "Critical"},
        {"id": "FC_001", "name": "Font Size Validation", "category": "Format Compliance", "priority": "High"},
        {"id": "FC_002", "name": "Letter Width Ratio", "category": "Format Compliance", "priority": "High"},
        {"id": "FC_003", "name": "Color Contrast Validation", "category": "Format Compliance", "priority": "High"},
        {"id": "QV_001", "name": "Standard Units Only", "category": "Quantity Validation", "priority": "Critical"},
        {"id": "QV_002", "name": "Prohibited Language Check", "category": "Quantity Validation", "priority": "Critical"},
        {"id": "SS_001", "name": "Product Standard Sizes", "category": "Standard Sizes", "priority": "Medium"},
        {"id": "SS_002", "name": "Category Requirements", "category": "Standard Sizes", "priority": "Medium"},
        {"id": "ET_001", "name": "Weight Error Validation", "category": "Error Tolerance", "priority": "Critical"},
        {"id": "PP_001", "name": "No Individual Stickers", "category": "Prohibited Practices", "priority": "High"},
        {"id": "PP_002", "name": "Deceptive Package Detection", "category": "Prohibited Practices", "priority": "High"},
        {"id": "EX_001", "name": "Small Package Exemption", "category": "Exemption Checks", "priority": "Info"},
        {"id": "EX_002", "name": "Export/Institutional Exemption", "category": "Exemption Checks", "priority": "Info"},
        {"id": "EN_001", "name": "Batch Consistency Check", "category": "AI-Enhanced Features", "priority": "Low"},
        {"id": "EN_002", "name": "OCR Confidence Validation", "category": "AI-Enhanced Features", "priority": "Low"},
        {"id": "EN_003", "name": "Predictive Compliance Scoring", "category": "AI-Enhanced Features", "priority": "Low"},
        {"id": "EN_004", "name": "Multi-Language Detection", "category": "AI-Enhanced Features", "priority": "Low"},
        {"id": "EN_005", "name": "Competitor Benchmark", "category": "AI-Enhanced Features", "priority": "Low"},
        {"id": "EN_006", "name": "Regulation Updates", "category": "AI-Enhanced Features", "priority": "Low"}
    ],
    "priorityColors": {"Critical": "#DC2626", "High": "#EA580C", "Medium": "#CA8A04", "Info": "#2563EB", "Low": "#16A34A"}
}

# Create figure
fig = go.Figure()

# Define positions for flowchart layout
# Input at top
input_x, input_y = 0.5, 0.95
output_x, output_y = 0.5, 0.05

# Categories in middle rows
category_positions = {
    "Mandatory Declarations": (0.15, 0.75),
    "Format Compliance": (0.35, 0.75),
    "Quantity Validation": (0.55, 0.75),
    "Error Tolerance": (0.75, 0.75),
    "Prohibited Practices": (0.85, 0.75),
    "Standard Sizes": (0.25, 0.55),
    "Exemption Checks": (0.45, 0.55),
    "AI-Enhanced Features": (0.75, 0.55)
}

# Organize rules by category
category_rules = {}
for rule in data["rules"]:
    cat = rule["category"]
    if cat not in category_rules:
        category_rules[cat] = []
    category_rules[cat].append(rule)

# Add input node
fig.add_trace(go.Scatter(
    x=[input_x], y=[input_y],
    mode='markers+text',
    marker=dict(size=60, color='#6B7280', line=dict(width=2, color='white')),
    text=['Package Data<br>Input'],
    textposition='middle center',
    textfont=dict(size=10, color='white'),
    name='Input',
    showlegend=False
))

# Add output node
fig.add_trace(go.Scatter(
    x=[output_x], y=[output_y],
    mode='markers+text',
    marker=dict(size=60, color='#059669', line=dict(width=2, color='white')),
    text=['Compliance<br>Score Output'],
    textposition='middle center',
    textfont=dict(size=10, color='white'),
    name='Output',
    showlegend=False
))

# Add category nodes and their rules
for category, (cat_x, cat_y) in category_positions.items():
    rules = category_rules[category]
    priority = rules[0]["priority"]
    color = data["priorityColors"][priority]
    
    # Abbreviate category name
    cat_short = category.replace(" ", "<br>")[:15]
    if len(category) > 15:
        cat_short = category[:12] + "..."
    
    # Add category node
    fig.add_trace(go.Scatter(
        x=[cat_x], y=[cat_y],
        mode='markers+text',
        marker=dict(size=50, color=color, line=dict(width=2, color='white')),
        text=[f'{cat_short}<br>{len(rules)} rules<br>{priority}'],
        textposition='middle center',
        textfont=dict(size=8, color='white'),
        name=category,
        showlegend=False
    ))
    
    # Add arrows from input to categories
    fig.add_annotation(
        x=cat_x, y=cat_y + 0.03,
        ax=input_x, ay=input_y - 0.03,
        arrowhead=2, arrowsize=1, arrowwidth=1.5,
        arrowcolor='#374151',
        showarrow=True
    )
    
    # Add arrows from categories to output
    fig.add_annotation(
        x=output_x, y=output_y + 0.03,
        ax=cat_x, ay=cat_y - 0.03,
        arrowhead=2, arrowsize=1, arrowwidth=1.5,
        arrowcolor='#374151',
        showarrow=True
    )
    
    # Add individual rules around category
    rule_count = len(rules)
    if rule_count > 0:
        # Calculate positions for rules around the category
        angles = np.linspace(0, 2*np.pi, rule_count, endpoint=False)
        radius = 0.08
        
        for i, rule in enumerate(rules):
            rule_x = cat_x + radius * np.cos(angles[i])
            rule_y = cat_y + radius * np.sin(angles[i])
            
            # Abbreviate rule name
            rule_name = rule["name"][:12] + "..." if len(rule["name"]) > 12 else rule["name"]
            
            fig.add_trace(go.Scatter(
                x=[rule_x], y=[rule_y],
                mode='markers+text',
                marker=dict(size=25, color=color, line=dict(width=1, color='white')),
                text=[f'{rule["id"]}<br>{rule_name}'],
                textposition='middle center',
                textfont=dict(size=6, color='white'),
                name=f'{rule["id"]}',
                showlegend=False
            ))
            
            # Add small arrows from category to rule
            fig.add_annotation(
                x=rule_x, y=rule_y,
                ax=cat_x, ay=cat_y,
                arrowhead=1, arrowsize=0.5, arrowwidth=1,
                arrowcolor=color,
                showarrow=True
            )

# Add priority legend
legend_y_positions = [0.35, 0.30, 0.25, 0.20, 0.15]
priorities = ["Critical", "High", "Medium", "Info", "Low"]

for i, priority in enumerate(priorities):
    fig.add_trace(go.Scatter(
        x=[0.02], y=[legend_y_positions[i]],
        mode='markers+text',
        marker=dict(size=20, color=data["priorityColors"][priority]),
        text=[priority],
        textposition='middle right',
        textfont=dict(size=10),
        name=priority,
        showlegend=False
    ))

# Update layout
fig.update_layout(
    title="Legal Metrology Rule Engine - 25 Rules Structure",
    showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.05, 1.05]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Save the chart
fig.write_image("legal_metrology_flowchart.png")
fig.write_image("legal_metrology_flowchart.svg", format="svg")

print("Flowchart saved successfully!")