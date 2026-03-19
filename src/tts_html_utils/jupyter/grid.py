# Standard Library Imports
from typing import Dict, List, Union, Tuple, Any, Optional

# Installed dependency imports
# None yet

# Teamtools Studio Imports
from tts_utilities.logger import create_logger

# This Library Imports
from tts_html_utils.core.components.flexbox import FlexColumn, FlexRow, FlexItem

logger = create_logger(name='tts_html_utils.jupyter.grid')


class IPythonGrid:
    """
    A flexible grid layout system for displaying content in Jupyter notebooks.
    
    This class allows you to create complex grid layouts with precise control over
    the width and height of each cell. It uses CSS Flexbox for layout, ensuring
    that each column is truly independent of the others.
    
    Example:
        ```python
        grid = IPythonGrid()
        
        # Add content with keys
        grid.add_content('plot1', fig1)
        grid.add_content('plot2', fig2)
        grid.add_content('table1', table_widget)
        grid.add_content('plot3', fig3)
        
        # Configure Plotly figures for better display
        grid.set_plotly_aspect_ratio('plot1', aspect_ratio=1.5)  # width/height ratio
        grid.set_plotly_size('plot2', height=400)  # fixed height, auto width
        
        # Configure the layout
        grid.configure_layout([
            [['plot1', '250px', '50%'], ['plot2', '250px', '50%']],
            [['table1', '250px', '25%'], ['plot3', '250px', '75%']]
        ])
        
        # Or set uniform row heights
        grid.set_row_heights(['300px', '400px'])
        
        # Display the grid
        display(grid)
        ```
    """
    
    def __init__(self):
        """Initialize an empty grid."""
        self.content = {}  # Store content as key-value pairs
        self.layout = []   # Store layout configuration
    
    def add_content(self, key: str, content: Any) -> 'IPythonGrid':
        """
        Add content to the grid with an associated key.
        
        Args:
            key: A unique identifier for this content
            content: The content to add (e.g., a Plotly figure, widget, etc.)
            
        Returns:
            self for method chaining
        """
        self.content[key] = content
        return self
        
    def set_plotly_aspect_ratio(self, key: str, aspect_ratio: float = None) -> 'IPythonGrid':
        """
        Set the aspect ratio for a Plotly figure.
        
        Args:
            key: The key of the Plotly figure content
            aspect_ratio: The aspect ratio to set (width/height). 
                          If None, the aspect ratio will be determined by the container.
                          If a number, the figure will maintain that aspect ratio.
                          
        Returns:
            self for method chaining
        """
        if key not in self.content:
            raise KeyError(f"Content with key '{key}' not found")
            
        content = self.content[key]
        
        # Check if content is a Plotly figure
        if hasattr(content, 'layout') and hasattr(content, 'data'):
            try:
                if aspect_ratio is not None:
                    # Set the aspect ratio
                    content.update_layout(
                        autosize=True,
                        # The aspect ratio is maintained by setting yaxis.scaleanchor and yaxis.scaleratio
                        yaxis=dict(
                            scaleanchor="x",
                            scaleratio=1/aspect_ratio
                        )
                    )
                else:
                    # Remove any aspect ratio constraint
                    if hasattr(content.layout, 'yaxis'):
                        if hasattr(content.layout.yaxis, 'scaleanchor'):
                            del content.layout.yaxis.scaleanchor
                        if hasattr(content.layout.yaxis, 'scaleratio'):
                            del content.layout.yaxis.scaleratio
            except Exception as e:
                # If we encounter any error, log it but don't fail
                print(f"Warning: Could not set aspect ratio for Plotly figure: {e}")
        
        return self
    
    def set_plotly_size(self, key: str, width: int = None, height: int = None) -> 'IPythonGrid':
        """
        Set a fixed size for a Plotly figure.
        
        Args:
            key: The key of the Plotly figure content
            width: The width in pixels. If None, width will be determined by the container.
            height: The height in pixels. If None, height will be determined by the container.
            
        Returns:
            self for method chaining
        """
        if key not in self.content:
            raise KeyError(f"Content with key '{key}' not found")
            
        content = self.content[key]
        
        # Check if content is a Plotly figure
        if hasattr(content, 'layout') and hasattr(content, 'data'):
            try:
                # Update the layout with the specified size
                update_dict = {}
                
                if width is not None:
                    update_dict['width'] = width
                if height is not None:
                    update_dict['height'] = height
                    
                # Only update if we have changes to make
                if update_dict:
                    content.update_layout(**update_dict)
            except Exception as e:
                # If we encounter any error, log it but don't fail
                print(f"Warning: Could not set size for Plotly figure: {e}")
        
        return self
    
    def set_default_plot_dimensions(self, height: int = 400, width: int = None) -> 'IPythonGrid':
        """
        Set default dimensions for all Plotly figures in the grid.
        
        Args:
            height: Default height in pixels for all plots
            width: Default width in pixels for all plots. If None, width will be determined by container.
            
        Returns:
            self for method chaining
        """
        # Find all Plotly figures in the content
        for key, content in self.content.items():
            if hasattr(content, 'layout') and hasattr(content, 'data'):
                try:
                    # Update the layout with default dimensions
                    update_dict = {'autosize': True}
                    
                    if height is not None:
                        update_dict['height'] = height
                    if width is not None:
                        update_dict['width'] = width
                        
                    content.update_layout(**update_dict)
                except Exception as e:
                    # If we encounter any error, log it but don't fail
                    print(f"Warning: Could not set default dimensions for {key}: {e}")
        
        return self
    
    def set_row_heights(self, heights: List[str]) -> 'IPythonGrid':
        """
        Set the heights for all rows in the grid.
        
        Args:
            heights: A list of height values (e.g., ['200px', '300px', '400px']).
                    The number of heights should match the number of rows in the layout.
        
        Returns:
            self for method chaining
        """
        if not self.layout:
            raise ValueError("Layout must be configured before setting row heights")
            
        if len(heights) != len(self.layout):
            raise ValueError(f"Number of heights ({len(heights)}) does not match number of rows ({len(self.layout)})")
        
        # Update the height for each cell in each row
        for row_idx, row in enumerate(self.layout):
            height = heights[row_idx]
            for cell_idx, cell in enumerate(row):
                if isinstance(cell, list):
                    # Update the height in the list format [key, height, width]
                    if len(cell) >= 2:
                        cell[1] = height
                    elif len(cell) == 1:
                        cell.append(height)
                elif isinstance(cell, dict):
                    # Update the height in the dict format {'key': key, 'height': height, 'width': width}
                    cell['height'] = height
        
        return self
    
    def configure_layout(self, layout: List[List[Union[List, Dict]]]) -> 'IPythonGrid':
        """
        Configure the layout of the grid using an explicit layout configuration.
        
        Args:
            layout: A list of rows, where each row is a list of cell configurations.
                   Each cell configuration is a list or dict specifying [key, height, width] or
                   {'key': key, 'height': height, 'width': width}.
        
        Returns:
            self for method chaining
        """
        # Store the layout configuration
        self.layout = layout
        
        # Validate that all keys in the layout exist in the content
        for row in layout:
            for cell in row:
                # Extract the key based on whether cell is a list or dict
                if isinstance(cell, list):
                    key = cell[0]
                elif isinstance(cell, dict):
                    key = cell.get('key')
                else:
                    raise ValueError(f"Cell configuration must be a list or dict, got {type(cell)}")
                
                # Check if the key exists in content
                if key not in self.content:
                    raise ValueError(f"Key '{key}' in layout not found in content")
        
        return self
    
    def get_cell_config(self, cell: Union[List, Dict]) -> Tuple[str, Optional[str], Optional[str]]:
        """
        Extract the key, height, and width from a cell configuration.
        
        Args:
            cell: A cell configuration, either as a list [key, height, width] or
                 a dict {'key': key, 'height': height, 'width': width}
                 
        Returns:
            A tuple of (key, height, width)
        """
        if isinstance(cell, list):
            # List format: [key, height, width]
            if len(cell) >= 3:
                return cell[0], cell[1], cell[2]
            elif len(cell) == 2:
                return cell[0], cell[1], None
            elif len(cell) == 1:
                return cell[0], None, None
            else:
                raise ValueError("Cell list must have at least a key")
        elif isinstance(cell, dict):
            # Dict format: {'key': key, 'height': height, 'width': width}
            return cell.get('key'), cell.get('height'), cell.get('width')
        else:
            raise ValueError(f"Cell configuration must be a list or dict, got {type(cell)}")
    
    def _repr_html_(self):
        """
        Generate HTML representation of the grid for display in IPython.
        
        This method uses html_utils FlexContainer components to create a
        flexible grid layout that respects the specified widths and heights.
        
        Returns:
            HTML string representation of the grid
        """
        # Add CSS to help with Plotly figures
        plotly_css = """
        <style>
            /* Make Plotly figures responsive */
            .js-plotly-plot, .plot-container {
                width: 100% !important;
                height: 100% !important;
            }
            .svg-container {
                width: 100% !important;
                height: 100% !important;
            }
        </style>
        """
        
        # Create a main container (column direction)
        main_container = FlexColumn(gap='5px')
        
        # Add the CSS to the container
        main_container.add_child(plotly_css)
        
        # Process each row in the layout
        for row in self.layout:
            # Create a row container
            row_container = FlexRow(gap='5px')
            
            # Process each cell in the row
            for cell in row:
                # Get cell configuration
                key, height, width = self.get_cell_config(cell)
                
                # Create a flex item for the cell
                cell_style = {
                    'border': '1px solid #eaeaea',
                    'padding': '5px',
                    'overflow': 'hidden',
                    'box-sizing': 'border-box'
                }
                
                if height:
                    cell_style['height'] = height
                
                # Create the flex item with the specified width
                cell_item = FlexItem(
                    width=width if width else None,
                    style=cell_style
                )
                
                # Add the cell content if the key exists
                if key in self.content:
                    content = self.content[key]
                    
                    # For content with _repr_html_ method
                    if hasattr(content, '_repr_html_'):
                        html_content = content._repr_html_()
                        cell_item.add_child(html_content)
                    else:
                        cell_item.add_child(str(content))
                else:
                    cell_item.add_child(f"<div style='color:red; padding: 10px;'>Content for key '{key}' not found</div>")
                
                # Add the cell to the row
                row_container.add_child(cell_item)
            
            # Add the row to the main container
            main_container.add_child(row_container)
        
        # Render the HTML
        return main_container.render()
    
    def display(self):
        """
        Display the grid in a Jupyter notebook.
        
        This method is better for displaying interactive widgets.
        It uses ipywidgets to create a layout that properly handles
        interactive widgets.
        
        Returns:
            A widget container with the grid layout
        """
        from IPython.display import display as ipython_display
        import ipywidgets as widgets
        
        # Create a container for the entire grid
        grid_container = widgets.VBox(layout=widgets.Layout(width='100%'))
        rows = []
        
        # Process each row in the layout
        for row in self.layout:
            # Create a container for the row
            row_container = widgets.HBox(layout=widgets.Layout(width='100%'))
            cells = []
            
            # Process each cell in the row
            for cell in row:
                # Get cell configuration
                key, height, width = self.get_cell_config(cell)
                
                # Create a layout for the cell
                cell_layout = widgets.Layout(
                    border='1px solid #eaeaea',
                    padding='5px',
                    overflow='hidden',  # Hide overflow
                    min_height='100px'   # Ensure a minimum height
                )
                
                if height:
                    cell_layout.height = height
                if width:
                    cell_layout.width = width
                
                # Create a container for the cell content
                if key in self.content:
                    content = self.content[key]
                    
                    # Check if content is a Plotly figure (has 'layout' attribute)
                    if hasattr(content, 'layout') and hasattr(content, 'data'):
                        # Create an Output widget that will contain the figure
                        output = widgets.Output(layout=cell_layout)
                        
                        # Configure the figure for better fit
                        # Set autosize to true for responsiveness
                        content.update_layout(autosize=True)
                        
                        # Remove any fixed height/width to let the container determine size
                        if hasattr(content.layout, 'height'):
                            content.layout.height = None
                        if hasattr(content.layout, 'width'):
                            content.layout.width = None
                            
                        # Add config for responsiveness if possible
                        if not hasattr(content, '_config'):
                            content._config = {}
                        content._config['responsive'] = True
                        
                        # Add CSS to make the plot fill its container
                        css = """
                        <style>
                            /* Target this specific output area */
                            .output_subarea .js-plotly-plot, 
                            .output_subarea .plot-container {
                                width: 100% !important;
                                height: 100% !important;
                            }
                        </style>
                        """
                        
                        # Display the CSS and figure
                        with output:
                            ipython_display(widgets.HTML(css))
                            ipython_display(content)
                            
                        cell_widget = output
                    # Check if content is already a widget
                    elif isinstance(content, widgets.Widget):
                        # Instead of modifying the widget directly, wrap it in a container
                        container = widgets.Box(layout=cell_layout)
                        container.children = [content]
                        cell_widget = container
                    else:
                        # For other non-widget content, use an Output widget
                        output = widgets.Output(layout=cell_layout)
                        with output:
                            ipython_display(content)
                        cell_widget = output
                else:
                    cell_widget = widgets.HTML(
                        value=f"<div style='color:red; padding: 10px;'>Content for key '{key}' not found</div>",
                        layout=cell_layout
                    )
                
                cells.append(cell_widget)
            
            # Add cells to the row
            row_container.children = cells
            rows.append(row_container)
        
        # Add rows to the grid
        grid_container.children = rows
                    
        return grid_container
