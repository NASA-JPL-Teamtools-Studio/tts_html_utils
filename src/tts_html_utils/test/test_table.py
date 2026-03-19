import pytest
import pdb
from bs4 import BeautifulSoup
from unittest.mock import MagicMock, patch

from tts_html_utils.core.components.base import HtmlComponentSimple
from tts_html_utils.core.components.table import Cell, Row, Header, Superheader, PowerTable
from tts_html_utils.core.components.misc import Link, Button

class TestTableComponents:

    # --- Basic Components (Cell/Row) ---
    
    def test_cell_basic(self):
        """Test Cell rendering."""
        c = Cell("Data")
        assert c.render() == '<td>Data</td>'

    def test_row_basic(self):
        """Test Row rendering with auto-cell wrapping."""
        r = Row(['A', 'B'])
        html = r.render()
        assert '<tr>' in html
        assert '<td>A</td>' in html
        assert '<td>B</td>' in html

    def test_row_manual_cells(self):
        """Test Row with pre-made Cell objects."""
        c1 = Cell("A", style={'color': 'red'})
        r = Row([c1, "B"])
        html = r.render()
        assert '<td style="color: red;">A</td>' in html
        assert '<td>B</td>' in html

    # --- Headers ---

    def test_header_basic(self):
        """Test Header rendering standard TH tags."""
        h = Header(['Name', 'Age'])
        html = h.render()
        soup = BeautifulSoup(html, 'html.parser')
        
        th_tags = soup.find_all('th')
        assert len(th_tags) == 2
        assert th_tags[0].text == 'Name'
        assert th_tags[1].text == 'Age'

    def test_header_with_filters(self):
        """Test Header injects input fields when filtering is enabled."""
        h = Header(['Name'], include_filter_inputs=True)
        html = h.render()
        
        assert 'input' in html
        assert 'id="name-filter"' in html
        assert 'class="filter-input"' in html

    def test_superheader(self):
        """Test Superheader rendering and attributes."""
        sh = Superheader("My Table Title", collapsible=True, default_closed=True)
        html = sh.render()
        soup = BeautifulSoup(html, 'html.parser')
        
        th = soup.find('th')
        assert th.attrs['colspan'] == '100%'
        assert "My Table Title" in th.text
        
        tr = soup.find('tr')
        assert 'superheader' in tr.attrs['class'] 

    # --- PowerTable ---

    @patch('tts_html_utils.core.components.table.render_html_from_stock_template')
    def test_powertable_init_simple(self, mock_render):
        """Test initializing PowerTable with simple dict data."""
        data = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
        pt = PowerTable(row_data=data)
        
        # Verify columns inferred
        assert pt.col_fields == ['name', 'age']
        
        # Verify rows created
        rows = [c for c in pt.children if isinstance(c, Row)]
        assert len(rows) == 2
        
        # Check first row content
        row_html = rows[0].render()
        assert 'Alice' in row_html
        assert '30' in row_html

    def test_powertable_expandable_rows(self):
        """Test creating a table with expandable details."""
        # Tuple format: (Main Data, Hidden Details)
        data = [
            ({'id': 1, 'name': 'Item A'}, "Details for A"),
            ({'id': 2, 'name': 'Item B'}, None) # No details
        ]
        
        pt = PowerTable(row_data=data, column_fields=['name'])
        
        rows = [c for c in pt.children if isinstance(c, Row)]
        
        # Should have 3 rows: 
        # 1. Item A (Primary)
        # 2. Item A Details (Hidden)
        # 3. Item B (Primary)
        assert len(rows) == 3
        
        # Check Item A Primary
        assert 'prime_row' in rows[0].class_name
        
        # Check Item A Details
        assert 'detail_row' in rows[1].class_name
        assert 'style="display: none;"' in rows[1].children[0].render() # The cell inside is hidden
        assert 'Details for A' in rows[1].render()

    def test_powertable_add_header(self):
        """Test adding a header explicitly."""
        pt = PowerTable()
        pt.col_fields = ['a', 'b'] # Required if adding header without names
        pt.add_header()
        
        assert pt.header is not None
        assert isinstance(pt.header, Header)
        assert pt.header.col_names == ['A', 'B'] # Title cased

    def test_powertable_js_injection(self):
        """Test that enabling features injects the correct JS."""
        # 1. Filters
        pt = PowerTable(add_filters='local')
        assert pt.filter_table is True
        assert any('static_html_filter_table.js' in str(p[0]) for p in pt.js_includes)

        # 2. Sorting
        pt2 = PowerTable(add_sorting='django')
        assert any('django_html_table_sort.js' in str(p[0]) for p in pt2.js_includes)

    def test_powertable_id_generation(self):
        """Test UUID generation for tables."""
        pt1 = PowerTable()
        pt2 = PowerTable()
        assert pt1.id is not None
        assert pt2.id is not None
        assert pt1.id != pt2.id

    def test_powertable_js_injection_complete(self):
        """Test ALL branches of JS injection for sorting and filtering."""
        
        # 1. Filter: Local (Already tested, but keeping for completeness)
        pt_local_filter = PowerTable(add_filters='local')
        assert any('static_html_filter_table.js' in str(p[0]) for p in pt_local_filter.js_includes)

        # 2. Filter: Django
        pt_django_filter = PowerTable(add_filters='django')
        assert any('django_html_filter_table.js' in str(p[0]) for p in pt_django_filter.js_includes)

        # 3. Sorting: Local
        pt_local_sort = PowerTable(add_sorting='local')
        assert any('static_html_table_sort.js' in str(p[0]) for p in pt_local_sort.js_includes)

        # 4. Sorting: Django
        pt_django_sort = PowerTable(add_sorting='django')
        assert any('django_html_table_sort.js' in str(p[0]) for p in pt_django_sort.js_includes)

    def test_powertable_invalid_options(self):
        """Test that invalid filter/sorting options raise Exceptions (missing else branches)."""
        
        # 1. Invalid Filter
        with pytest.raises(Exception) as exc:
            PowerTable(add_filters='invalid_option')
        assert "don't understand how to add invalid_option filters" in str(exc.value)

        # 2. Invalid Sorting
        with pytest.raises(Exception) as exc:
            PowerTable(add_sorting='invalid_option')
        assert "don't understand how to add invalid_option sorting" in str(exc.value)

    def test_powertable_no_features(self):
        """Test the explicit 'else' block when features are None."""
        pt = PowerTable(add_filters=None, add_sorting=None)
        assert pt.filter_table is False
        # Verify no sorting/filter JS was added
        js_str = str(pt.js_includes)
        assert 'filter_table.js' not in js_str
        assert 'table_sort.js' not in js_str    

    def test_link_with_extra_attr(self):
        """Test passing explicit attributes via kwargs covers lines 207-208."""
        # By passing 'attr', we trigger the merge logic and the 'del' statement
        link = Link('Link Text', href='https://example.com', attr={'id': 'custom-link', 'data-info': 'extra'})
        html = link.render()
        
        assert 'id="custom-link"' in html
        assert 'data-info="extra"' in html
        assert 'href="https://example.com"' in html
        assert 'target="_blank"' in html # Default preserved

    def test_button_with_extra_attr(self):
        """Test passing explicit attributes via kwargs covers lines 235-236."""
        # By passing 'attr', we trigger the merge logic and the 'del' statement
        btn = Button('Click Me', attr={'name': 'submit-btn', 'disabled': 'true'})
        html = btn.render()
        
        assert 'name="submit-btn"' in html
        assert 'disabled="true"' in html
        assert 'type="button"' in html # Default preserved

class TestTableCoverage:
    def test_row_with_premade_cells(self):
        """Covers line 70: passing premade Cell objects to Row."""
        c = Cell("Existing")
        # apply_cells=False is usually how this is triggered
        r = Row(children=[c], apply_cells=False)
        assert "<td>Existing</td>" in r.render()

    def test_powertable_primary_key_logic(self):
        """Covers lines 241 & 251: using _primary_key for row IDs."""
        # Case 1: Simple row with primary key (Hits line 251)
        data_simple = [{'_primary_key': 'rowA', 'val': 1}]
        pt1 = PowerTable(row_data=data_simple)
        assert any('id="' in child.render() and 'rowA' in child.render() for child in pt1.children if isinstance(child, Row))

        # Case 2: Expandable row with primary key (Hits line 241)
        # Note: we pass column_fields to avoid the 'tuple.keys()' AttributeError in the inference logic
        data_complex = [({'_primary_key': 'rowB', 'val': 2}, "Details")]
        pt2 = PowerTable(row_data=data_complex, column_fields=['val'])
        
        # Verify the fix for line 241: row[0]["_primary_key"]
        html = pt2.children[0].render()
        assert 'rowB' in html
        # Verify the details row linked to the primary key
        assert any('rowB-details' in child.render() for child in pt2.children if isinstance(child, Row))

    def test_powertable_list_data(self):
        """Covers line 357: passing a list instead of a dict to add_row."""
        pt = PowerTable(column_fields=['a', 'b'])
        pt.add_row(['val1', 'val2']) # Triggers the 'else' branch of add_row
        assert '<td>val1</td><td>val2</td>' in pt.children[-1].render()

    def test_powertable_errors(self):
        """Covers lines 300, 371: testing NotImplemented and ValueErrors."""
        pt = PowerTable()
        
        # Missing column names/fields for header (Line 300)
        with pytest.raises(ValueError):
            pt.add_header()

        # Direct render_content call (Line 371)
        with pytest.raises(NotImplementedError):
            pt.render_content()

    @patch('tts_html_utils.core.components.table.render_html_from_stock_template')
    def test_powertable_render_call(self, mock_render):
        """Covers line 380: full render pipeline."""
        pt = PowerTable()
        pt.render()
        mock_render.assert_called_once()