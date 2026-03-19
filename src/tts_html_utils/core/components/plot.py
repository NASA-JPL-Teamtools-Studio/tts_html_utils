#Standard Library Imports
import pdb
import uuid

#Installed dependency imports
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

#Teamtools Studio Imports
from tts_utilities.logger import create_logger

#This Library Imports
from tts_html_utils.core.components.base import HtmlComponent
from tts_html_utils.core.components.misc import Div

logger = create_logger(name='html_utils.core.components.base')

class PlotBase(HtmlComponent):
    """
    The base wrapper for embedding Plotly figures into the HTML document.

    **Concept:**
    Plotly produces interactive, JavaScript-based charts. To put them in an HTML file, 
    we need to convert the Python `Figure` object into a specific block of HTML/JS code.
    
    **Important Note on Performance:**
    This component renders with `include_plotlyjs=False`. The global `plotly.js` library 
    is automatically requested via the component's `js_includes` and managed by the 
    `HtmlCompiler` to ensure it is loaded once in the `<head>`.

    :param fig: The existing Plotly figure to render. If None, creates a blank figure.
    :type fig: plotly.graph_objects.Figure, optional
    :param title: Sets the title of the plot layout.
    :type title: str, optional
    :param template: The visual theme to use (e.g., 'plotly_dark', 'seaborn', 'ggplot2'). 
                     Defaults to 'seaborn'.
    :type template: str, optional
    :param class_name: Primary CSS class for the container Div.
    :type class_name: str, optional
    :param extra_class_name: Additional CSS classes.
    :type extra_class_name: str, optional
    :param id: Optional. A custom ID for this container. If not provided, a unique ID will be generated.
    :type id: str, optional
    :param style: Dictionary of inline CSS styles for the container Div.
    :type style: dict, optional
    """
    DEFAULT_PLOTLY_TEMPLATE = 'seaborn'
    def __init__(self, fig=None, title=None, template=None, class_name=None, extra_class_name=None, id=None, style=None, include_plotlyjs=False, full_html=False):
        self.fig = fig or go.Figure()
        self.fig.update_layout(template=(template or self.DEFAULT_PLOTLY_TEMPLATE))
        self.include_plotlyjs = include_plotlyjs
        self.full_html = full_html
        
        if title:
            self.fig.update_layout(title=title)
        
        # Ensure every plot has a unique ID for JS scoping if one isn't provided
        if id is None:
            id = f"plotly-{uuid.uuid4().hex[:8]}"

        super().__init__(children=None, class_name=class_name, extra_class_name=extra_class_name, id=id, style=style)
        
        # Automatically include the Plotly global library via CDN
        # The HtmlCompiler will deduplicate this if multiple plots are present.
        self.js_includes.append(("https://cdn.plot.ly/plotly-3.3.1.min.js", {}))

    def render(self):
        """
        Converts the Python Plotly figure into an HTML Div string.
        """
        # Generate the Plotly HTML snippet. 
        # This already includes a <div id="self.id"> and a <script>.
        plotly_html = pio.to_html(
            self.fig,
            include_plotlyjs=self.include_plotlyjs,
            full_html=self.full_html,
            div_id=self.id
        )

        return plotly_html


class ScatterPlot(PlotBase):
    """
    A helper for creating basic line/scatter plots.

    **Legacy Note:** This is a legacy wrapper. For complex visualization needs, it is generally 
    recommended to use `dtat-lib` or build `go.Figure` objects directly and pass 
    them to `PlotBase`.
    """
    def add_trace(self, y, x=None, name=None, lines=False, markers=True, trace_kwargs=None, scatter_kwargs=None):
        """
        Adds a new data series (trace) to the plot.

        :param y: The Y-axis data points.
        :type y: list or array-like
        :param x: The X-axis data points.
        :type x: list or array-like, optional
        :param name: The name of this series (appears in the legend).
        :type name: str, optional
        :param lines: If True, connects points with lines.
        :type lines: bool, default False
        :param markers: If True, draws a dot at each data point.
        :type markers: bool, default True
        :param trace_kwargs: A passthrough dictionary of arguments sent to `self.fig.add_trace`. 
                             Useful for advanced layout options like `secondary_y=True`.
        :type trace_kwargs: dict, optional
        :param scatter_kwargs: A passthrough dictionary of arguments sent to `go.Scatter`.
                               Useful for styling options like `line_color`, `marker_size`, etc.
        :type scatter_kwargs: dict, optional
        """
        modes = []
        if lines:
            modes.append('lines')
        if markers:
            modes.append('markers')

        trace_kwargs = trace_kwargs or {}
        scatter_kwargs = scatter_kwargs or {}

        self.fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode='+'.join(modes),
                name=name,
                **scatter_kwargs
            ),
            **trace_kwargs
        )

class TimelinePlot(PlotBase):
    """
    A helper for creating Gantt-style timeline charts.

    **Legacy Note:**
    This is a legacy wrapper. Consider using `dtat-lib` for modern timeline visualization.
    """
    def __init__(self, data, x_start_name, x_end_name, y_name, color=None, title=None, date_format_str=None):
        """
        Initialize the timeline using `plotly.express.timeline`.

        :param data: The dataset (usually a Pandas DataFrame).
        :type data: pandas.DataFrame or list of dicts
        :param x_start_name: The column name containing start timestamps.
        :type x_start_name: str
        :param x_end_name: The column name containing end timestamps.
        :type x_end_name: str
        :param y_name: The column name to use for the Y-axis labels (tasks/rows).
        :type y_name: str
        :param color: The column name to use for coloring the bars.
        :type color: str, optional
        :param title: The chart title.
        :type title: str, optional
        :param date_format_str: A d3-formatting string to control how dates appear on the X-axis 
                                (e.g., '%Y-%m-%d').
        :type date_format_str: str, optional
        """
        timeline = px.timeline(data, x_start=x_start_name, x_end=x_end_name, y=y_name, color=color)

        super().__init__(fig=timeline, title=title)

        # optionally update the formatting of the x-axis ticks (which are datetime compliant for all timeline plots)
        if date_format_str:
            self.fig.update_layout(xaxis_tickformat = date_format_str)