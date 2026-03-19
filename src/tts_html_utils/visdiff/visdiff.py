#Standard Library Imports
import pdb
from pathlib import Path
import uuid

#Installed dependency imports
#None

#Teamtools Studio Imports
from tts_utilities.logger import create_logger
from tts_utilities.util import as_list

#This Library Imports
from tts_html_utils.core.components.base import HtmlComponent, HtmlComponentSimple
from tts_html_utils.resource import render_html_from_stock_template, get_stylesheet
from tts_html_utils.core.components.navigation import Navbar
from tts_html_utils.core.components.misc import Div
from tts_html_utils.core.components.text import H1

logger = create_logger(name='tts_html_utils.core.visdiff.visdiff')

class VisualDiff(Div):
    """
    A specialized component for side-by-side comparison of two tables.

    **The Concept:**
    When you need to compare two datasets (e.g., "Expected Results" vs "Actual Results"), 
    placing them one after another is hard to read. This component places them 
    side-by-side in a split-pane view.

    **The "Magic":**
    Simply placing tables next to each other isn't enough. If one table has 5 lines of text 
    in row 1, and the other table only has 1 line, the rows will misalign visually.
    
    This component solves that by injecting custom JavaScript (`row_height_match.js`) 
    that forces every row on the left to be the exact same height as the corresponding 
    row on the right, ensuring perfect visual alignment. It also synchronizes scrolling, 
    so if you scroll the left table, the right table moves with it.

    :param left_table: The first HtmlComponent Table to display on the left.
    :type left_table: HtmlComponent
    :param right_table: The second HtmlComponent Table to display on the right.
    :type right_table: HtmlComponent
    :param left_label: A header/title for the left pane.
    :type left_label: str or HtmlComponent, optional
    :param right_label: A header/title for the right pane.
    :type right_label: str or HtmlComponent, optional
    :param uuid: A unique identifier to namespace the JavaScript variables (prevents conflicts if multiple Diffs are on one page).
    :type uuid: str
    :param overflow: Controls scrolling behavior. Currently supports 'synced_scroll' or None.
    :type overflow: str, optional
    """
    def __init__(self, left_table, right_table, left_label=None, right_label=None, uuid='', overflow='synced_scroll'):
        super().__init__()

        # Convert simple string labels into Header objects if necessary
        if isinstance(left_label, str): left_label = H1(left_label)
        if isinstance(right_label, str): right_label = H1(right_label)

        # 1. Inject Row Height Matching Logic
        # This script measures both tables and forces taller rows to shrink/expand so they match.
        js_path = Path(__file__).parent.parent.joinpath('javascript/visdiff_tables/row_height_match.js')
        self.js_includes.append((js_path, {'table_ids': [left_table.id, right_table.id], 'uuid': uuid}))

        if overflow == 'synced_scroll':
            # 2. Inject Scroll Sync Logic
            # This script listens for scroll events on one wrapper and mirrors them to the other.
            js_path = Path(__file__).parent.parent.joinpath('javascript/visdiff_tables/scroll_sync.js')
            left_wrapper_id = f'{left_table.id}-wrapper'
            right_wrapper_id = f'{right_table.id}-wrapper'
            self.js_includes.append((js_path, {'table_ids': [left_wrapper_id, right_wrapper_id], 'uuid': uuid}))

            # 3. Construct the Layout
            # We wrap the tables in divs with 'float: left/right' to create the side-by-side effect.
            if left_label is not None and right_label is not None:
                labels = Div([
                    Div(left_label, id=f'{left_wrapper_id}-label', style={'width': '45%', 'overflow-x': 'auto', 'float': 'left'}),
                    Div(right_label, id=f'{right_wrapper_id}-label', style={'width': '45%', 'overflow-x': 'auto', 'float': 'right'}),
                    ])

            elif left_label is not None or right_label is not None:
                raise Exception('Either both VisualDiff label must be None or neither must be None.')
            else:
                labels = None

            tables = Div([
                Div(left_table, id=left_wrapper_id, style={'width': '45%', 'overflow-x': 'auto', 'float': 'left'}),
                Div(right_table, id=right_wrapper_id, style={'width': '45%', 'overflow-x': 'auto', 'float': 'right'}),
                ])

            # 4. Final Assembly
            if labels is None:
                self.children = [tables]
            else:
                self.children = [Div([labels, tables])]
        else:
            # Fallback: Just stack them if sync is disabled
            self.children = [left_table, right_table]