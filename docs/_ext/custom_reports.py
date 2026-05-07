"""
Custom Sphinx extension for generating dynamic content.

Add custom report generation functions here. They'll be called during the Sphinx build.
"""
from docutils import nodes
from docutils.parsers.rst import Directive
from datetime import datetime


class CustomReportDirective(Directive):
    """
    Directive to generate custom reports via Python code.
    
    Usage in .rst files:
        .. custom-report:: system_info
    """
    required_arguments = 1  # The name of the report function
    has_content = False
    
    def run(self):
        report_name = self.arguments[0]
        
        # Call the appropriate report generator
        if report_name == "system_info":
            html = generate_system_info()
        elif report_name == "component_table":
            html = generate_component_table()
        else:
            html = f"<p>Unknown report: {report_name}</p>"
        
        # Return raw HTML node
        raw_node = nodes.raw('', html, format='html')
        return [raw_node]


def generate_system_info():
    """Generate a system information table."""
    html = '<table border="1" style="border-collapse: collapse;">'
    html += '<tr><td><strong>Generated On</strong></td>'
    html += f'<td>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</td></tr>'
    html += '<tr><td><strong>Documentation System</strong></td><td>Sphinx</td></tr>'
    html += '</table>'
    return html


def generate_component_table():
    """Generate a table of HTML components."""
    html = '<div style="background: #f0f0f0; padding: 10px; margin: 10px 0;">'
    html += '<h4>Available Components</h4>'
    html += '<ul>'
    html += '<li><strong>PowerTable</strong>: Interactive tables with sorting and filtering</li>'
    html += '<li><strong>Header</strong>: Table headers with optional sort/filter controls</li>'
    html += '<li><strong>Cell</strong>: Individual table cells</li>'
    html += '</ul>'
    html += '</div>'
    return html


def setup(app):
    """Register the extension with Sphinx."""
    app.add_directive('custom-report', CustomReportDirective)
    
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
