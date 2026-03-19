#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PowerTable Demo

This demo shows how to create and customize PowerTable components, which are
advanced tables with features like sorting, filtering, and expandable rows.
"""

# Standard Library Imports
import sys
import random
from pathlib import Path
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import the tts_html_utils package
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Teamtools Studio Imports
from tts_html_utils.core.compiler import HtmlCompiler
from tts_html_utils.core.components.table import PowerTable
from tts_html_utils.core.components.text import Heading1, Heading2, Paragraph
from tts_html_utils.core.components.misc import Div, HorizontalBreak, Style

def generate_sample_data(num_rows=20):
    """Generate sample data for the demo tables."""
    # Sample data for a mission operations table
    mission_data = []
    
    # Create some realistic-looking mission data
    spacecraft_names = ["Voyager", "Perseverance", "Curiosity", "Cassini", "New Horizons"]
    status_options = ["Nominal", "Warning", "Critical", "Standby", "Maintenance"]
    subsystem_names = ["Power", "Propulsion", "Comms", "Payload", "Thermal", "ADCS"]
    
    # Base date for timestamps
    base_date = datetime.now()
    
    for i in range(num_rows):
        spacecraft = random.choice(spacecraft_names)
        status = random.choice(status_options)
        # Assign appropriate status class
        status_class = {
            "Nominal": "status-green",
            "Warning": "status-yellow",
            "Critical": "status-red",
            "Standby": "status-blue",
            "Maintenance": "status-gray"
        }[status]
        
        # Generate a timestamp within the last 30 days
        days_ago = random.randint(0, 30)
        timestamp = (base_date - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Create the row data
        row = {
            "id": f"event-{i+1}",
            "timestamp": timestamp,
            "spacecraft": spacecraft,
            "subsystem": random.choice(subsystem_names),
            "status": status,
            "status_class": status_class,
            "message": f"{'ERROR: ' if status == 'Critical' else ''}Event detected in {spacecraft} {random.choice(subsystem_names).lower()} subsystem."
        }
        
        mission_data.append(row)
    
    # Sort by timestamp (newest first)
    mission_data.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return mission_data

def create_basic_table():
    """Create a basic PowerTable."""
    # Define column fields
    column_fields = ["id", "timestamp", "spacecraft", "subsystem", "status", "message"]
    
    # Generate sample data
    row_data = generate_sample_data(10)
    
    # Create the PowerTable
    table = PowerTable(
        column_fields=column_fields,
        row_data=row_data,
        extra_class_name="demo-table",
        add_filters='local',
        add_sorting='local',
    )
    table.add_header()
    
    return table

def create_styled_table():
    """Create a styled PowerTable with custom CSS classes."""
    # Define column fields
    column_fields = ["id", "timestamp", "spacecraft", "subsystem", "status", "message"]
    
    # Generate sample data
    row_data = generate_sample_data(15)
    
    # Create cell classes for status column
    cell_classes = []
    for row in row_data:
        classes = {
            "status": row["status_class"]
        }
        cell_classes.append(classes)
    
    # Create the PowerTable with styling
    table = PowerTable(
        column_fields=column_fields,
        row_data=row_data,
        extra_class_name="demo-table striped",
        cell_classes=cell_classes
    )
    
    return table

def create_expandable_table():
    """Create a PowerTable with expandable rows."""
    # Define column fields
    column_fields = ["id", "timestamp", "spacecraft", "subsystem", "status", "message"]
    
    # Generate sample data
    base_data = generate_sample_data(8)
    
    # Create expandable rows with details
    row_data = []
    for item in base_data:
        # Create detail content for expandable row
        detail_html = f"""
        <div class="detail-container">
            <h4>Event Details for {item['id']}</h4>
            <div class="detail-grid">
                <div class="detail-label">Spacecraft:</div>
                <div class="detail-value">{item['spacecraft']}</div>
                
                <div class="detail-label">Subsystem:</div>
                <div class="detail-value">{item['subsystem']}</div>
                
                <div class="detail-label">Status:</div>
                <div class="detail-value {item['status_class']}">{item['status']}</div>
                
                <div class="detail-label">Timestamp:</div>
                <div class="detail-value">{item['timestamp']}</div>
                
                <div class="detail-label">Full Message:</div>
                <div class="detail-value">{item['message']}</div>
                
                <div class="detail-label">Actions:</div>
                <div class="detail-value">
                    <button class="action-button">Acknowledge</button>
                    <button class="action-button">Investigate</button>
                    <button class="action-button">Resolve</button>
                </div>
            </div>
        </div>
        """
        
        # Create a tuple of (row_data, detail_html) for expandable rows
        row_tuple = (item, detail_html)
        row_data.append(row_tuple)
    
    # Create the PowerTable with expandable rows
    table = PowerTable(
        column_fields=column_fields,
        row_data=row_data,
        extra_class_name="demo-table expandable"
    )
    
    return table

def main():
    """Create and display PowerTable demos."""
    # Create the HTML compiler
    compiler = HtmlCompiler(title="PowerTable Demo")
    
    # Add a header
    compiler.add_body_component(Heading1("PowerTable Demo"))
    compiler.add_body_component(Paragraph(
        "This demo showcases the PowerTable component from html_utils, "
        "which provides advanced table features like sorting, filtering, and expandable rows."
    ))
    
    # Add custom CSS for the demo
    custom_css = """
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .demo-table {
            margin-bottom: 30px;
            width: 100%;
        }
        
        .striped tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        .status-green {
            color: #2ecc71;
            font-weight: bold;
        }
        
        .status-yellow {
            color: #f39c12;
            font-weight: bold;
        }
        
        .status-red {
            color: #e74c3c;
            font-weight: bold;
        }
        
        .status-blue {
            color: #3498db;
            font-weight: bold;
        }
        
        .status-gray {
            color: #7f8c8d;
            font-weight: bold;
        }
        
        .detail-container {
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
        
        .detail-grid {
            display: grid;
            grid-template-columns: 150px 1fr;
            gap: 10px;
        }
        
        .detail-label {
            font-weight: bold;
            color: #555;
        }
        
        .action-button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 5px 10px;
            margin-right: 10px;
            border-radius: 3px;
            cursor: pointer;
        }
        
        .action-button:hover {
            background-color: #2980b9;
        }
    """
    # Create a Style component with the CSS content
    style_component = Style(custom_css)
    compiler.add_body_component(style_component)
    
    # Basic Table Section
    compiler.add_body_component(Heading2("Basic PowerTable"))
    compiler.add_body_component(Paragraph(
        "A simple PowerTable with default styling. "
        "Click on column headers to sort the table."
    ))
    compiler.add_body_component(create_basic_table())
    compiler.add_body_component(HorizontalBreak())
    
    # Styled Table Section
    compiler.add_body_component(Heading2("Styled PowerTable"))
    compiler.add_body_component(Paragraph(
        "A PowerTable with custom styling applied to specific cells. "
        "Notice how the Status column has different colors based on the status value."
    ))
    compiler.add_body_component(create_basic_table())
    compiler.add_body_component(HorizontalBreak())
    
    # Expandable Table Section
    compiler.add_body_component(Heading2("Expandable PowerTable"))
    compiler.add_body_component(Paragraph(
        "A PowerTable with expandable rows. "
        "Click on a row to see additional details."
    ))
#    compiler.add_body_component(create_expandable_table())
    
    # Render the HTML
    output_file = Path(__file__).parent / "power_table_demo.html"
    html = compiler.render_to_file(output_file)
    print(f"HTML output written to: {output_file}")
    
    # Display info
    print("\nPowerTable Demo")
    print("===============\n")
    print("This demo shows how to create and customize PowerTable components.")
    print("Open the HTML file in a browser to see the interactive tables.")

if __name__ == "__main__":
    main()
