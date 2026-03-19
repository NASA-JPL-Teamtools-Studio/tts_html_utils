#Standard Library Imports
import pdb
from pathlib import Path
import uuid

#Installed dependency imports
#None

#Teamtools Studio Imports
from tts_utilities.util import as_list
from tts_utilities.logger import create_logger

#This Library Imports
from tts_html_utils.core.components.base import HtmlComponent, HtmlComponentSimple
from tts_html_utils.resource import render_html_from_stock_template, get_stylesheet
from tts_html_utils.core.components.navigation import Navbar
from tts_html_utils.core.components.misc import Div

logger = create_logger(name='html_utils.core.components.structure')


class PaneContainer(HtmlComponentSimple):
    """
    A "Tabbed" view container.

    **The Concept:**
    Sometimes you have too much content to fit on one screen (e.g., three different 
    data tables: "Raw Data", "Processed Data", "Errors"). 
    
    Instead of stacking them vertically (making the page 10 miles long), a `PaneContainer` 
    stacks them on top of each other like a deck of cards. It automatically generates 
    a navigation bar (tabs) at the top. Clicking a tab swaps which card is visible.

    **How it works:**
    1. You create the container.
    2. You call `.add_pane("Raw Data", my_table_component)`.
    3. The container automatically builds a `Navbar` with a "Raw Data" button.
    4. The included JavaScript handles the click events to toggle visibility between panes.
    
    **Nested Containers:**
    PaneContainer supports nesting - you can add a PaneContainer as a pane inside another PaneContainer.
    Each container maintains its own independent tabs and state.

    :param args: Arguments passed to the parent `Div`.
    :param kwargs: Keyword arguments passed to the parent `Div`.
    :param id: Optional. A custom ID for this container. If not provided, a unique ID will be generated.
    """
    TAG = 'div'

    def __init__(self, *args, **kwargs):
        # Extract id from kwargs if provided
        user_id = kwargs.pop('id', None)
        
        super().__init__(*args, **kwargs)
        self.panes = {}
        self.js_includes = []
        self.css_includes = []
        
        # Use user-provided ID if available, otherwise generate a unique ID
        if user_id:
            self.container_id = user_id
        else:
            self.container_id = f"pane-container-{uuid.uuid4().hex[:8]}"
        
        # Set the HTML id attribute if not already set
        if not hasattr(self, 'id') or not self.id:
            self.id = self.container_id
        
        # Add the container ID as a data attribute
        if 'attr' not in self.__dict__ or self.attr is None:
            self.attr = {}
        self.attr['data-container-id'] = self.container_id
        
        # Add a class to identify this as a pane container
        self._class.append('pane-container')

        # Inject the specialized logic for swapping tabs
        js_path = Path(__file__).parent.parent.parent.joinpath('javascript/pane_container/pane_container.js')
        self.js_includes.append((js_path, {}))

        css_path = Path(__file__).parent.parent.parent.joinpath('css/pane_container/pane_container.css')
        self.css_includes.append((css_path, {}))

    def add_pane(self, html_components, pane_name):
        """
        Adds a new "Tab" (Pane) to the container.

        :param html_components: The content to display when this tab is active. 
                                Can be a single component (like a Table) or a Div containing many.
        :type html_components: HtmlComponent or list
        :param pane_name: The label that will appear on the navigation button (e.g., "Summary Results").
        :type pane_name: str
        :raises Exception: If a pane with the same name already exists.
        """
        if pane_name in self.panes.keys():
            raise Exception(f'Pane "{pane_name}" already exists in this pane container.')
        else:
            # Create a pane ID that's unique to this container
            pane_id = f"{self.container_id}-{pane_name.lower().replace(' ','-')}"
            
            # We wrap the content in a Div with data attributes so the JS knows what to show/hide
            # and which container it belongs to
            self.panes[pane_name] = Div(html_components, attr={
                'data-id': pane_id,
                'data-pane-name': pane_name.lower().replace(' ','-'),
                'data-container-id': self.container_id
            })
        self.update_children()

    def add_child(self, child):
        """
        [Disabled]
        
        You cannot add generic children to a PaneContainer because it breaks the 
        tab logic. You must use `.add_pane()` instead. It must be included here
        because PaneContainer extends HtmlComponentSimple, which requires that it
        be defined.
        """
        raise NotImplementedError('add_child is not available on PaneContainer. Use add_pane instead. Children will be built at compile time.')

    def update_children(self):
        """
        Internal method to rebuild the layout.

        Every time a new pane is added, this deletes the old internal structure and 
        rebuilds the Navbar (to include the new button) and re-stacks the pane Divs.
        """
        # Create a mapping of pane names to their unique IDs
        pane_ids = {}
        for pane_name, pane in self.panes.items():
            # Extract the pane ID from the data-id attribute
            pane_id = pane.attr.get('data-id')
            pane_ids[pane_name] = pane_id
        
        # 1. Rebuild the Navigation Bar based on current pane names
        # Add data attributes to identify which container this navbar belongs to
        nav_links = {}
        for k in self.panes.keys():
            pane_id = pane_ids[k]
            # Use the full pane ID for the href
            nav_links[k] = '#' + pane_id
        
        navbar = Navbar(nav_links)
        # Add container ID to the navbar
        navbar.attr = navbar.attr or {}
        navbar.attr['data-container-id'] = self.container_id
        self.children = [navbar]
        
        # 2. Re-attach all pane Divs
        for ii, pane in enumerate(self.panes.values()):
            # Reset visibility classes
            pane._class = [x for x in pane._class if x not in ['hidden-pane', 'visible-pane']]
            
            # The first pane added is always visible by default; others are hidden
            if ii == 0:
                pane._class.append('visible-pane')
            else:
                pane._class.append('hidden-pane')
            self.children.append(pane)