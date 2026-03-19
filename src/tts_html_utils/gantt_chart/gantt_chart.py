import json
import uuid
import sys
from pathlib import Path

# --- Library Imports ---
from tts_html_utils.core.compiler import HtmlCompiler
from tts_html_utils.core.components.misc import Div
from tts_html_utils.core.components.base import HtmlComponent

# --- THE COMPONENT CLASS ---
class InteractiveGantt(Div):
    TEMPLATE_FILE = 'interactive_gantt.html'

    def __init__(self, data, name_key='name', start_key='start', end_key='end', 
                 children_key='children', inner_width='2000px', height='100vh', 
                 default_depth=1, **kwargs): # default_depth=1 means only root and direct children
        super().__init__(**kwargs)
        self.raw_data = data if isinstance(data, list) else [data]
        self.inner_width = inner_width
        self.height = height
        self.default_depth = default_depth
        self.name_key = name_key
        self.start_key = start_key
        self.end_key = end_key
        self.children_key = children_key
        self.unique_id = uuid.uuid4().hex[:8]
        self.min_date = None
        self.max_date = None
        self.get_context_data()

    def _normalize_data(self, items):
        result = []
        for item in items:
            node = {
                'name': item.get(self.name_key, 'Unnamed'),
                'start': item.get(self.start_key),
                'end': item.get(self.end_key),
                'color': item.get('color'),  # Add support for custom color
                'highlight_full_height': item.get('highlight_full_height', False),  # Add support for full height highlighting
                'below_the_fold': item.get('below_the_fold', False),  # Add support for below-the-fold status
                'hover_text': item.get('hover_text').render() if isinstance(item.get('hover_text'), HtmlComponent) else  item.get('hover_text') ,  # Add support for custom hover text
                'children': []
            }
            if node['start']:
                if self.min_date is None or node['start'] < self.min_date:
                    self.min_date = node['start']
            if node['end']:
                if self.max_date is None or node['end'] > self.max_date:
                    self.max_date = node['end']

            children = item.get(self.children_key, [])
            if children:
                node['children'] = self._normalize_data(children)
            result.append(node)
        return result

    def get_context_data(self):
        self.min_date = None
        self.max_date = None
        normalized = self._normalize_data(self.raw_data)
        
        if not self.min_date: self.min_date = "2024-01-01"
        if not self.max_date: self.max_date = "2024-12-31"

        # Create context for the HTML template
        context = {
            'unique_id': self.unique_id,
            'chart_data_json': json.dumps(normalized, indent=2), 
            'start_date': self.min_date,
            'end_date': self.max_date,
            'inner_width': self.inner_width,
            'height': self.height,
            'default_depth': self.default_depth
        }
        
        js_path = Path(__file__).parent.parent.joinpath('javascript/gantt_chart/gantt_chart.js')
        self.js_includes.append((js_path, context))

        css_path = Path(__file__).parent.parent.joinpath('css/gantt_chart/gantt_chart.css')
        self.css_includes.append((css_path, context))

        from jinja2 import Template
        template = Template("""

                            <div id="gantt-{{ unique_id }}" class="gantt-wrapper">
                                <div class="gantt-toolbar">
                                    <button class="gantt-btn" id="zoom-in-{{ unique_id }}">In (+)</button>
                                    <button class="gantt-btn" id="zoom-out-{{ unique_id }}">Out (-)</button>
                                    <button class="gantt-btn" id="fit-{{ unique_id }}">Fit</button>
                                    
                                    <span style="margin-left: 10px; color:#888; font-size:11px;">Cursor:</span>
                                    <span class="cursor-time-display" id="cursor-time-{{ unique_id }}">--</span>
                                    
                                    <span style="flex-grow:1"></span>
                                    
                                    <span class="view-range-display" id="view-range-{{ unique_id }}"></span>
                                    
                                    <span style="width:15px; border-right:1px solid #ccc; margin: 0 10px;"></span>
                                    <span style="font-size:11px; color:#888; min-width:60px; text-align:right;" id="status-{{ unique_id }}"></span>
                                </div>

                                <div class="gantt-header-row">
                                    <div class="gantt-sidebar-header">Task Name</div>
                                    <div class="gantt-timeline-header" id="tl-header-{{ unique_id }}">
                                        Timeline <span style="font-weight:normal; font-size:11px; color:#999">(Shift+Scroll to Pan, Ctrl+Wheel to Zoom)</span>
                                    </div>
                                </div>
                                
                                <div class="gantt-body">
                                    <div class="gantt-sidebar">
                                        <div class="sidebar-spacer">Task Hierarchy</div>
                                        <div id="sidebar-list-{{ unique_id }}"></div>
                                    </div>
                                    
                                    <div class="gantt-timeline-scroll-area" id="timeline-scroll-{{ unique_id }}">
                                        <div class="gantt-timeline-canvas" id="canvas-{{ unique_id }}">
                                            <div class="gantt-axis-row" id="axis-{{ unique_id }}"></div>
                                            <div id="grid-{{ unique_id }}"></div>
                                            <div id="bars-{{ unique_id }}"></div>
                                        </div>
                                    </div>
                                </div>
                                <div id="tooltip-{{ unique_id }}" class="gantt-tooltip"></div>
                            </div>
                        """)
        self.children = template.render(**context)
        return context
        
# --- DEMO EXECUTION ---
if __name__ == '__main__':
    data = [
        {
            "name": "2024 Project (Year Scale)",
            "start": "2024-01-01",
            "end": "2024-12-31",
            "children": [
                {"name": "Q1 Planning", "start": "2024-01-01", "end": "2024-03-31", "children": []},
                {"name": "Q2 Execution", "start": "2024-04-01", "end": "2024-06-30", "children": []},
                {"name": "Important Milestone", "start": "2024-05-15", "end": "2024-05-15", "color": "#e11d48", "highlight_full_height": True, "children": []},
            ]
        },
        {
            "name": "Rocket Launch (Second Scale)",
            "start": "2024-06-01T12:00:00",
            "end": "2024-06-01T12:01:00",
            "children": [
                {"name": "T-10 Count", "start": "2024-06-01T11:59:50", "end": "2024-06-01T12:00:00", "children": []},
                {"name": "Ignition", "start": "2024-06-01T12:00:00", "end": "2024-06-01T12:00:05", "color": "#f97316", "highlight_full_height": True, "children": []},
                {"name": "Liftoff", "start": "2024-06-01T12:00:05", "end": "2024-06-01T12:00:15", "children": []},
            ]
        }
    ]

    print("Initializing...")
    chart = InteractiveGantt(
        data=data, 
        children_key='children', 
        default_depth=2,
        inner_width='1500px'
    )

    print("Compiling...")
    compiler = HtmlCompiler(title="Gantt Zoom Demo")
    compiler.add_body_component(chart)
    compiler.render_to_file("zoom_gantt.html")
    print("Done! Open 'zoom_gantt.html'")