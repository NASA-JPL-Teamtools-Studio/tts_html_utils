#!/usr/bin/env python3

from tts_data_utils.core.generic import GenericContainer
from tts_html_utils.core.compiler import HtmlCompiler

# Create some sample data with subcontainers (like Tower's rule results)
data = [
    {'name': 'Alice', 'age': 30, 'score': 85.5, 'department': 'Engineering', '_primary_key': 'alice'},
    {'name': 'Bob', 'age': 25, 'score': 92.3, 'department': 'Sales', '_primary_key': 'bob'},
    {'name': 'Charlie', 'age': 35, 'score': 78.9, 'department': 'Engineering', '_primary_key': 'charlie'},
    {'name': 'Diana', 'age': 28, 'score': 95.1, 'department': 'Marketing', '_primary_key': 'diana'},
    {'name': 'Eve', 'age': 32, 'score': 88.7, 'department': 'Engineering', '_primary_key': 'eve'},
    {'name': 'Frank', 'age': 29, 'score': 91.2, 'department': 'Sales', '_primary_key': 'frank'},
    {'name': 'Grace', 'age': 31, 'score': 83.4, 'department': 'Marketing', '_primary_key': 'grace'},
    {'name': 'Henry', 'age': 27, 'score': 89.6, 'department': 'Engineering', '_primary_key': 'henry'},
    {'name': 'Iris', 'age': 33, 'score': 94.8, 'department': 'Sales', '_primary_key': 'iris'},
    {'name': 'Jack', 'age': 26, 'score': 87.3, 'department': 'Marketing', '_primary_key': 'jack'},
]

# Create subcontainers for each record (like Tower's disposition details)
subcontainers = []
for person in data:
    detail_data = [
        {'field': 'Email', 'value': f"{person['name'].lower()}@company.com"},
        {'field': 'Location', 'value': f"Office {person['age'] % 3 + 1}"},
        {'field': 'Notes', 'value': f"Employee in {person['department']}"},
    ]
    subcontainers.append({
        'Details': GenericContainer(detail_data)
    })

# Create a GenericContainer with subcontainers
container = GenericContainer(raw_data=data, subcontainers=subcontainers)

# Create a power table with sorting and filtering enabled
table = container.power_table(
    superheader='Employee Data - Test Sorting and Filtering',
    add_sorting='local',
    add_filters='local'
)

# Create an HTML compiler
compiler = HtmlCompiler('PowerTable Sorting Test')

# Add the table to the body
compiler.add_body_component(table)

# Render to file
output_path = '/Users/muszynsk/projects/tt_studio/dev/tts_core/tts_html_utils/examples/table_sort_test.html'
compiler.render_to_file(output_path)

print(f'HTML report generated: {output_path}')
print('Open this file in a browser to test sorting and filtering functionality')
