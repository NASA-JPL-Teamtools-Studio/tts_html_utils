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

logger = create_logger(name='html_utils.core.components.base')

#================================================
# :: Table
#================================================
class Cell(HtmlComponentSimple):
    """
    A single table data cell (<td>).
    
    **Concept:**
    The atomic unit of a table. It holds the actual data (text, numbers, or other HTML).
    
    **Alias:** `TD` (conceptually, though not explicitly aliased in python)
    """
    TAG = 'td'

class Row(HtmlComponentSimple):
    """
    A table row (<tr>).
    
    **Concept:**
    A horizontal container that holds `Cell` objects. HTML tables are row-oriented; 
    you cannot define columns directly, only rows of cells.

    :param children: The contents of the row. Can be `Cell` objects, strings, or numbers.
    :type children: List, optional
    :param class_name: CSS classes for the row.
    :type class_name: str or list of str, optional
    :param extra_class_name: Additional CSS classes to append.
    :type extra_class_name: str or list of str, optional
    :param tag: The HTML tag. Defaults to 'tr'. (Rarely needs changing).
    :type tag: str, optional
    :param id: HTML id attribute.
    :type id: str, optional
    :param style: Inline CSS styles.
    :type style: dict, optional
    :param apply_cells: If True, automatically wraps plain strings/numbers in `Cell` objects.
                        If False, assumes `children` are already valid HTML components. 
                        Defaults to True.
    :type apply_cells: bool
    :param cell_styles: A list of style dictionaries to apply to the generated cells. 
                        Must match the length of `children`.
    :type cell_styles: list, optional
    """

    TAG = 'tr'
    def __init__(self, children=None, class_name=None, extra_class_name=None, tag=None, id=None, style=None, apply_cells=True, cell_styles=None):
        children = as_list(children)
        if cell_styles is None: cell_styles = [None]*len(children)

        if apply_cells and (children is not None):
            cells = [child if isinstance(child, Cell) else Cell(child, style=cell_style) for child, cell_style in zip(as_list(children), cell_styles)]
        else:
            cells = children
        super().__init__(children=cells, class_name=class_name, extra_class_name=extra_class_name, tag=tag, id=id, style=style)

class Header(HtmlComponentSimple):
    """
    The Table Head section (<thead>).

    **Concept:**
    A special row group reserved for column titles. Browsers and printers treat this 
    differently than the body (e.g., repeating the header on every page of a printout).

    **Note:** While you can use this class manually, `PowerTable` creates this automatically 
    via the `add_header` method.

    :param column_names: A list of strings to be used as column titles.
    :type column_names: List[str]
    :param class_name: CSS classes for the header row.
    :type class_name: str, optional
    :param extra_class_name: Additional CSS classes.
    :type extra_class_name: str, optional
    :param style: Inline CSS styles.
    :type style: dict, optional
    :param include_filter_inputs: If True, injects `<input>` boxes for column filtering. 
                                  Used internally by `PowerTable` when filtering is enabled.
    :type include_filter_inputs: bool
    """
    TAG = 'thead'
    def __init__(self, column_names, class_name=None, extra_class_name=None, style={}, include_filter_inputs=False):
        super().__init__(class_name=class_name, extra_class_name=extra_class_name, style=style)
        self.col_names = column_names
        self.cells = []
        for col_name in self.col_names:
            children = col_name
            column_header_js = col_name.lower().replace(' ','-').replace('_','-')
            if include_filter_inputs:
                children = f'<div id="{column_header_js}-sort">{children}</div>'
                #to do: consider making List class for this
                #but for now this is good enough
                children += f'<input type="text" id="{column_header_js}-filter" class="filter-input" data-column="{column_header_js}">'

            self.cells.append(
                Cell(tag='th', children=children, extra_class_name=extra_class_name)
                )


    def render_content(self):
        """
        Internal render hook. 
        """
        row = Row(children=self.cells, extra_class_name=['header'])
        return row.rendered

class Superheader(HtmlComponentSimple):
    """
    A secondary header row that sits *above* the main column headers.

    **Concept:**
    Often used for a table title or to group multiple columns under a single category.
    This element spans all columns (`colspan=100%`) by default.

    :param text: The text to display in the superheader.
    :type text: str
    :param collapsible: Enables accordion-style collapsing of the table body.
    :type collapsible: bool
    :param default_closed: If `collapsible` is True, this sets the initial state to closed.
    :type default_closed: bool
    :param class_name: CSS classes.
    :type class_name: str, optional
    :param extra_class_name: Additional CSS classes.
    :type extra_class_name: str, optional
    :param style: Inline CSS styles.
    :type style: dict, optional
    """
    TAG = 'thead'
    def __init__(self, text, collapsible=False, default_closed=False, class_name=None, extra_class_name=None, style={}):
        super().__init__(class_name=class_name, extra_class_name=extra_class_name, style=style)
        self.cells = [Cell(tag='th', children=text)]
        self.cells[0].attr = {**self.cells[0].attr, **{'colspan': '100%'}}
        if collapsible:
            self.add_class('collapsible-group')
            if default_closed:
                self.add_class('active-clicked')

    def render_content(self):
        """
        Internal render hook. 
        """
        row = Row(children=self.cells, extra_class_name=['superheader'])
        return row.rendered


class PowerTable(HtmlComponent):
    """
    The "Swiss Army Knife" of tables.

    **Concept:**
    Building tables tag-by-tag (`<table>`, `<thead>`, `<tbody>`, `<tr>`, `<td>`...) 
    is tedious. `PowerTable` allows you to pass a list of Python dictionaries or tuples, 
    and it automatically constructs the full HTML structure.

    **Advanced Features:**
    It supports "Expandable Rows" (accordion details), sorting, and filtering via 
    pre-packaged JavaScript libraries included in this module.

    :param column_fields: A list of keys (e.g. `['name', 'age']`) to extract from `row_data` dictionaries.
                          If None, it infers them from the keys of the first row.
    :type column_fields: List[str], optional

    :param row_data: The actual data to display.
                     **Format 1 (Simple):** A list of dicts: `[{'name': 'Bob'}, {'name': 'Alice'}]`.
                     **Format 2 (Expandable):** A list of tuples: `[(primary_data_dict, hidden_details_html)]`.
                     If the second element of the tuple is not None, a hidden detail row is created 
                     that expands when the user clicks the main row.
    :type row_data: List[dict] or List[tuple], optional

    :param class_name: CSS class for the table. Defaults to `['power-table', 'alternating', 'sticky-header']`.
    :type class_name: str or list, optional
    :param extra_class_name: Additional CSS classes.
    :type extra_class_name: str or list, optional
    :param id: Unique ID. If None, a UUID is generated automatically (required for JS features).
    :type id: str, optional
    :param style: Inline CSS styles. Defaults to `{'text-align': 'left', 'border': '2px black solid'}`.
    :type style: dict, optional
    :param row_styles: A list of style dicts, one for each row in `row_data`.
    :type row_styles: List[dict], optional
    :param cell_classes: A list of class strings/lists, one for each row.
    :type cell_classes: List, optional
    :param cell_styles: A list of style dicts, one for each row.
    :type cell_styles: List, optional

    :param add_filters: Enables search inputs in the header. Options: `'local'`, `'django'`, or None.
    :type add_filters: str, optional
    :param add_sorting: Enables column sorting. Options: `'local'`, `'django'`, or None.
    :type add_sorting: str, optional
    """ 
    TAG = 'table'
    DEFAULT_CLASS = ['power-table', 'alternating', 'sticky-header']
    STYLESHEETS = [
    get_stylesheet('rule_result_table.css'),
    get_stylesheet('report_base.css'),
    get_stylesheet('rule_summary.css')
    ]

    def __init__(self, column_fields=None, row_data=None, class_name=None, extra_class_name=None, id=None, style={'text-align': 'left'}, row_styles=None, cell_classes=None, cell_styles=None, add_filters=None, add_sorting=None):
        #to do, put consider putting style into a sheet
        style = {**style, **{'border': '2px black solid'}}
        super().__init__(class_name=class_name, extra_class_name=extra_class_name, id=id, style=style)
        self.col_fields = column_fields
        self.add_sorting = add_sorting
        self.children = []
        self.filter_table = False
        self.id = id if id is not None else f'power-table-{uuid.uuid4()}'
        #force every table to have a unique ID for js reasons
        if self.id is None: self.id = uuid.uuid4()

        #TO DO: Replace this boolean hack
        already_included_show_hide = False
        if row_data is not None:
            #these rows seem hacky. But we need to be able to iterate.
            #just make this the default kwarg value??
            if row_styles is None: row_styles = [None]*len(row_data)
            if cell_styles is None: cell_styles = [None]*len(row_data)
            if cell_classes is None: cell_classes = [None]*len(row_data)
            
            # Logic fix for 100% coverage and tuple-data crash
            if self.col_fields is None: 
                first_row = row_data[0][0] if isinstance(row_data[0], tuple) else row_data[0]
                self.col_fields = [k for k in first_row.keys()]
                
            for row, row_style, cell_classes_this_row, cell_styles_this_row in zip(row_data, row_styles, cell_classes, cell_styles):
                if isinstance(row, tuple):
                    if not already_included_show_hide and row[1] is not None:
                        js_path = Path(__file__).parent.parent.parent.joinpath('javascript/filter_table/show_hide_details.js')
                        self.js_includes.append((js_path, {'table_id': self.id}))
                        already_included_show_hide = True
                    
                    # Corrected dictionary access within the tuple
                    if '_primary_key' in row[0].keys():
                        row_id = f'{self.id}-{row[0]["_primary_key"]}'
                    else:
                        row_id = uuid.uuid4()
                    self.add_row(row[0], style=row_style, id=row_id, row_class_name='prime_row', cell_classes=cell_classes_this_row, cell_styles=cell_styles_this_row)
                    if row[1] is not None:
                        desc_cell = Cell(row[1], style={'display':'none'})
                        desc_cell.attr['colspan'] = '100%'
                        self.add_row(Row(children=desc_cell, id=f'{row_id}-details', class_name='detail_row'), cell_classes=cell_classes_this_row, cell_styles=cell_styles_this_row)
                else:
                    if '_primary_key' in row.keys():
                        row_id = f'{self.id}-{row["_primary_key"]}'
                    else:
                        row_id = uuid.uuid4()

                    self.add_row(row, style=row_style, id=row_id, cell_classes=cell_classes_this_row, cell_styles=cell_styles_this_row)

        self.header = None
        self.superheader = None

        if add_filters:
            self.filter_table = True
            if add_filters is True: add_filters = 'local'
            if add_filters == 'local':
                js_path = Path(__file__).parent.parent.parent.joinpath('javascript/filter_table/static_html_filter_table.js')
            elif add_filters == 'django':
                js_path = Path(__file__).parent.parent.parent.joinpath('javascript/filter_table/django_html_filter_table.js')
            else:
                raise Exception(f'I don\'t understand how to add {add_filters} filters')
            self.js_includes.append((js_path, {'table_id': self.id}))
        else:
            self.filter_table = False

        if add_sorting:
            if add_sorting is True: add_sorting = 'local'
            if add_sorting == 'local':
                js_path = Path(__file__).parent.parent.parent.joinpath('javascript/filter_table/static_html_table_sort.js')
            elif add_sorting == 'django':
                js_path = Path(__file__).parent.parent.parent.joinpath('javascript/filter_table/django_html_table_sort.js')
            else:
                raise Exception(f'I don\'t understand how to add {add_sorting} sorting')
            self.js_includes.append((js_path, {'table_id': self.id}))

        self.css_includes = [(s, {}) for s in self.STYLESHEETS]

        
    def add_header(self, column_names=None, class_name=None, extra_class_name=None, style={}):
        """
        Adds a Header object to the PowerTable.

        :param column_names: Cell contents for the cells in the thead row.
                             If None, defaults to the capitalized keys from `col_fields`.
        :type column_names: List[str], optional
        :param class_name: Primary CSS class
        :type class_name: str
        :param extra_class_name: Secondary CSS class
        :type extra_class_name: str
        :param style: Dictionary of element-level CSS styles
        :type style: dict
        """
        if column_names is None:
            if self.col_fields is None:
                raise ValueError(f'Must set either column_names or have column_fields already set when adding header')
            column_names = [_.title() for _ in self.col_fields]

        self.header = Header(column_names, class_name=class_name, extra_class_name=extra_class_name, style=style, include_filter_inputs=self.filter_table)

    def add_superheader(self, text, class_name=None, extra_class_name=None, collapsible=False, default_closed=False, style={}):
        """
        Adds a SuperHeader (title row) object to the PowerTable.

        :param text: The text to display.
        :type text: str    
        :param class_name: Primary CSS class
        :type class_name: str    
        :param extra_class_name: Secondary CSS class
        :type extra_class_name: str    
        :param collapsible: Whether clicking the header toggles visibility of the table body.
        :type collapsible: bool    
        :param default_closed: Initial state if collapsible is True.
        :type default_closed: bool    
        :param style: Dictionary of element-level CSS styles
        :type style: dict
        """
        self.superheader = Superheader(
            text,
            class_name=class_name,
            extra_class_name=extra_class_name,
            collapsible=collapsible,
            default_closed=default_closed, 
            style=style
        )

    def add_row(self, row, id=None, row_class_name=None, row_extra_class_name=None, style={}, cell_classes=None, cell_styles=None):
        """
        Manually appends a Row object to the PowerTable.

        :param row: Can be an existing `Row` object, or a list/dict of data to convert into a Row.
        :type row: Row, list, or dict
        :param id: HTML id, should be unique among all HTML elements.
        :type id: str, optional
        :param row_class_name: CSS class for just this row.
        :type row_class_name: str, optional
        :param row_extra_class_name: Secondary CSS class for just this row.
        :type row_extra_class_name: str, optional
        :param style: Dictionary of element-level CSS styles.
        :type style: dict, optional
        :param cell_classes: List of classes to be applied to each cell in this row.
        :type cell_classes: List, optional
        :param cell_styles: List of CSS styles to be applied to each cell in this row.
        :type cell_styles: List, optional
        """
        if isinstance(row, Row):
            self.children.append(row)
            return

        if isinstance(row, dict) and self.col_fields is not None:
            row_data = [row.get(_) for _ in self.col_fields]
        else:
            row_data = list(row)


        if cell_styles is None: cell_styles = [None]*len(row_data)
        if cell_classes is None: cell_classes = [None]*len(row_data)

        row_cells = [row_datum if isinstance(row_datum, Cell) else Cell(children=row_datum, class_name=cell_class, style=cell_style) for row_datum, cell_class, cell_style in zip(row_data, cell_classes, cell_styles)]

        self.children.append(Row(children=row_cells, class_name=row_class_name, extra_class_name=row_extra_class_name, style=style, id=id, cell_styles=cell_styles))
        
    def render_content(self):
        """
        Internal render hook. 
        """
        raise NotImplementedError(f'Use full render pipeline for PowerTable')

    def render(self):
        """
        Converts the python objects into rendered HTML.
        
        This method uses a dedicated Jinja2 template (`table.html`) to ensure 
        headers, superheaders, and sorting/filtering inputs are placed correctly.
        """
        return render_html_from_stock_template(
            'table.html',
            table=self
        )