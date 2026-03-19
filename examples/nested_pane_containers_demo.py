#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Nested Pane Containers Demo

This demo shows how to create nested pane containers with multiple levels of nesting:

1. Outer Container (Level 1)
   - Contains regular content and inner containers
   
2. Inner Containers (Level 2)
   - One with a custom ID ("inner-container1")
   - One with an auto-generated ID
   
3. Deepest Container (Level 3)
   - Nested inside inner-container1
   - Demonstrates three levels of nesting

Each container maintains its own independent tabs and state, regardless of nesting level.
"""

# Standard Library Imports
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the tts_html_utils package
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Installed dependency imports
from IPython.display import display, HTML

# Teamtools Studio Imports
from tts_html_utils.core.compiler import HtmlCompiler
from tts_html_utils.core.components.structure import PaneContainer
from tts_html_utils.core.components.table import PowerTable
from tts_html_utils.core.components.misc import Div
from tts_html_utils.core.components.text import Heading1, Heading3, Paragraph


def create_demo_table(title, rows=3, cols=3):
    """Create a simple demo table with the given title."""
    # Create column fields
    column_fields = [f"column_{i+1}" for i in range(cols)]
    
    # Create row data as list of dictionaries
    row_data = []
    for i in range(rows):
        row = {}
        for j in range(cols):
            row[column_fields[j]] = f"{title} Row {i+1}, Col {j+1}"
        row_data.append(row)
    
    # Create the PowerTable
    return PowerTable(
        column_fields=column_fields,
        row_data=row_data,
        extra_class_name='demo-table'
    )


def create_demo_content(title):
    """Create some demo content with the given title."""
    return Div([
        Heading3(title),
        Paragraph(f"This is some demo content for {title}."),
        Paragraph("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
    ])


def main():
    """Create and display nested pane containers."""
    # Create the HTML compiler
    compiler = HtmlCompiler(title="Nested Pane Containers Demo")
    
    # Create the outer container with a custom ID
    outer_container = PaneContainer(id="outer-container")
    
    # Create the first inner container with a custom ID
    inner_container1 = PaneContainer(id="inner-container1")
    
    # Create a third-level (deepest) container with a custom ID
    deepest_container = PaneContainer(id="deepest-container")
    
    # Add panes to the deepest container
    deepest_container.add_pane(create_demo_table("Deepest Table", rows=2, cols=2), "Deepest Tab 1")
    deepest_container.add_pane(create_demo_content("Deepest Content"), "Deepest Tab 2")
    
    # Add panes to the first inner container, including the deepest container
    inner_container1.add_pane(create_demo_table("Inner Table 1"), "Inner Tab 1")
    inner_container1.add_pane(create_demo_content("Inner Content 1"), "Inner Tab 2")
    inner_container1.add_pane(deepest_container, "Third Level Container")  # Nested container inside inner_container1
    inner_container1.add_pane(create_demo_table("Inner Table 2", rows=2, cols=4), "Inner Tab 4")
    
    # Create the second inner container with an auto-generated ID
    inner_container2 = PaneContainer()
    
    # Add panes to the second inner container
    inner_container2.add_pane(create_demo_content("Another Inner Content"), "Another Inner Tab 1")
    inner_container2.add_pane(create_demo_table("Another Inner Table", rows=4, cols=2), "Another Inner Tab 2")
    
    # Add the inner containers and other content to the outer container
    outer_container.add_pane(create_demo_content("Outer Content 1"), "Outer Tab 1")
    outer_container.add_pane(inner_container1, "Nested Container 1")
    outer_container.add_pane(create_demo_table("Outer Table", rows=5, cols=3), "Outer Tab 3")
    outer_container.add_pane(inner_container2, "Nested Container 2")
    
    # Add a header and the outer container to the compiler
    compiler.add_body_component(Heading1("Nested Pane Containers Demo"))
    compiler.add_body_component(Paragraph("This demo shows how to create nested pane containers. Each container maintains its own independent tabs and state."))
    compiler.add_body_component(outer_container)
    
    # Render the HTML
    html = compiler.render()
    
    # Display info
    print("\nNested Pane Containers Demo")
    print("==========================\n")
    print("This demo shows how to create nested pane containers.")
    print("Each container maintains its own independent tabs and state.\n")
    
    # Write the HTML to a file
    output_file = Path(__file__).parent / "nested_pane_containers_demo.html"
    with open(output_file, "w") as f:
        f.write(html)
    print(f"HTML output written to: {output_file}\n")
    
    # If running in a Jupyter notebook, display the HTML
    try:
        display(HTML(html))
        print("HTML displayed in notebook.")
    except NameError:
        print("Not running in a Jupyter notebook. Open the HTML file to view the demo.")


if __name__ == "__main__":
    main()
