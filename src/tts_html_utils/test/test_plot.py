import pytest
import pdb
from unittest.mock import MagicMock, patch
import plotly.graph_objects as go

from tts_html_utils.core.components.plot import PlotBase, ScatterPlot, TimelinePlot

class TestPlotBase:
    
    def test_init_defaults(self):
        """Test initializing with no arguments creates a blank Figure."""
        pb = PlotBase()
        assert isinstance(pb.fig, go.Figure)
        # Just verify a template is set, don't check deep equality against defaults
        # as specific template defaults (seaborn) differ from blank defaults.
        assert pb.fig.layout.template is not None

    def test_init_custom(self):
        """Test initializing with custom figure, title, and template."""
        fig = go.Figure()
        pb = PlotBase(fig=fig, title="My Plot", template="plotly_dark")
        
        assert pb.fig == fig
        assert pb.fig.layout.title.text == "My Plot"

    # @patch is a decorator that swaps the real function for a Mock object.
    # We patch 'html_utils.core.components.plot.pio.to_html' because 
    # that is where YOUR code imports and uses it.
    @patch('tts_html_utils.core.components.plot.pio.to_html')
    def test_render(self, mock_to_html):
        """
        Test that render() calls pio.to_html with correct settings.
        
        Args:
            mock_to_html: The mock object replacing pio.to_html.
        """
        # 1. Setup the Stunt Double
        # We tell the mock: "When someone calls you, just return this string."
        mock_to_html.return_value = "<div>PLOTLY_HTML</div>"
        
        # 2. Run your code
        pb = PlotBase()
        output = pb.render()
        
        # 3. Verify the Output
        assert "<div>PLOTLY_HTML</div>" in output
        assert output.startswith("<div>")
        assert output.endswith("</div>")
        
        # 4. Verify the Interaction
        # Did your code call the function with the right arguments?
        mock_to_html.assert_called_once_with(
            pb.fig, 
            include_plotlyjs=False, 
            full_html=False,
            div_id=pb.id
        )


class TestScatterPlot:
    
    def test_add_trace_modes(self):
        """Test that lines/markers boolean flags convert to correct Plotly modes."""
        sp = ScatterPlot()
        
        # Case 1: Markers only (default)
        sp.add_trace(x=[1, 2], y=[1, 2], name="A", lines=False, markers=True)
        # Case 2: Lines only
        sp.add_trace(x=[1, 2], y=[3, 4], name="B", lines=True, markers=False)
        # Case 3: Both
        sp.add_trace(x=[1, 2], y=[5, 6], name="C", lines=True, markers=True)
        
        assert len(sp.fig.data) == 3
        assert sp.fig.data[0].mode == 'markers'
        assert sp.fig.data[1].mode == 'lines'
        assert sp.fig.data[2].mode == 'lines+markers'

    def test_kwargs_passthrough(self):
        """Test passing styles and layout options via kwargs."""
        sp = ScatterPlot()
        
        # We mock the add_trace method on the figure instance.
        # This prevents Plotly from throwing errors about valid/invalid arguments
        # and allows us to simply check if the arguments were passed through.
        sp.fig.add_trace = MagicMock()
        
        sp.add_trace(
            x=[1], y=[1], 
            scatter_kwargs={'marker': {'color': 'red'}},
            trace_kwargs={'secondary_y': True} 
        )
        
        # Verify the mock was called
        args, kwargs = sp.fig.add_trace.call_args
        
        # args[0] is the go.Scatter object created inside your method
        trace_obj = args[0]
        assert isinstance(trace_obj, go.Scatter)
        assert trace_obj.marker.color == 'red'
        
        # kwargs are the trace_kwargs passed to add_trace
        assert kwargs['secondary_y'] is True


class TestTimelinePlot:

    # We patch `px.timeline` because creating a real timeline requires pandas 
    # and complex data processing we don't want to run here.
    @patch('tts_html_utils.core.components.plot.px.timeline')
    def test_init_calls_express(self, mock_timeline):
        """Test that initializing TimelinePlot delegates to plotly.express."""
        
        # 1. Setup the Stunt Double
        # px.timeline usually returns a Figure. So we tell our mock to return a NEW mock Figure.
        mock_fig = go.Figure()
        mock_timeline.return_value = mock_fig
        
        data = [{'Task': 'A', 'Start': '1', 'Finish': '2'}]
        
        # 2. Run code
        tp = TimelinePlot(
            data, 
            x_start_name='Start', 
            x_end_name='Finish', 
            y_name='Task', 
            title="Gantt Chart"
        )
        
        # 3. Verify Interaction
        mock_timeline.assert_called_once_with(
            data, 
            x_start='Start', 
            x_end='Finish', 
            y='Task', 
            color=None
        )
        
        # Did your class update the layout title on the figure returned by the mock?
        assert tp.fig.layout.title.text == "Gantt Chart"

    @patch('tts_html_utils.core.components.plot.px.timeline')
    def test_date_formatting(self, mock_timeline):
        """Test that date_format_str updates the x-axis tick format."""
        # We need a real Figure object here so we can check if .update_layout actually changed properties
        mock_timeline.return_value = go.Figure()
        
        tp = TimelinePlot([], 's', 'e', 'y', date_format_str='%Y-%m')
        
        # Verify the property was set on the underlying figure
        assert tp.fig.layout.xaxis.tickformat == '%Y-%m'