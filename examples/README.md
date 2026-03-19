# HTML Utils Demos

This directory contains demonstrations of various components and features of the `html_utils` package.

## Available Demos

### Nested Pane Containers

The nested pane containers demo shows how to create pane containers that are nested inside other pane containers, with each container maintaining its own independent tabs and state.

- **Python Script**: `nested_pane_containers_demo.py`
- **Jupyter Notebook**: `nested_pane_containers_demo.ipynb`
- **Output HTML**: `nested_pane_containers_demo.html` (generated when you run the script)

To run the Python script demo:

```bash
cd /path/to/html_utils/demo
python nested_pane_containers_demo.py
```

This will generate an HTML file and print its location. Open this file in a web browser to see the demo.

To run the Jupyter notebook demo:

```bash
cd /path/to/html_utils/demo
jupyter notebook nested_pane_containers_demo.ipynb
```

## Key Features Demonstrated

1. **Custom IDs**: How to provide custom IDs for pane containers
2. **Auto-generated IDs**: How containers generate unique IDs when none are provided
3. **Nesting**: How to nest one pane container inside another
4. **Independent State**: How each container maintains its own tab state

## Adding New Demos

When adding new demos to this directory, please follow these guidelines:

1. Create both a Python script and a Jupyter notebook version if possible
2. Include detailed comments and explanations
3. Update this README with information about your demo
