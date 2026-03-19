import pytest
import pdb
from unittest.mock import patch
from tts_html_utils.core.components.base import HtmlComponent, HtmlComponentSimple, HtmlComponentSingleSimple

# --- Mocks for Testing ---

class MockComponent(HtmlComponentSimple):
    """Concrete implementation of HtmlComponentSimple for testing base logic."""
    TAG = 'div'

class MockSingleton(HtmlComponentSingleSimple):
    """Concrete implementation of a void/self-closing element."""
    TAG = 'br'

class TestBaseCoverage:

    def test_aggregate_attributes_basic(self):
        """Test basic attribute collection without children."""
        comp = MockComponent()
        comp.js_includes = [('base.js', {})]
        results = comp.aggregate_attributes('js_includes')
        assert ('base.js', {}) in results

    def test_aggregate_attributes_recursion(self):
        """Covers lines 104-105: recursive attribute harvesting from children."""
        parent = MockComponent()
        child = MockComponent()
        child.js_includes = [('child.js', {'async': True})]
        parent.add_child(child)
        
        results = parent.aggregate_attributes('js_includes')
        assert ('child.js', {'async': True}) in results

    @patch('tts_html_utils.core.components.base.pdb.set_trace')
    def test_aggregate_attributes_error_handling(self, mock_pdb):
        """Covers lines 106-107: the try/except block and pdb call."""
        parent = MockComponent()
        
        class BrokenComponent(MockComponent):
            def aggregate_attributes(self, attr, lst=None):
                # Manually trigger the exception that leads to line 106
                raise Exception("Aggregation Crash")

        parent.add_child(BrokenComponent())
        
        # Recursing into the broken child triggers the parent's try/except block
        parent.aggregate_attributes('js_includes')
        
        # Verify pdb.set_trace was called (proving we hit line 107)
        assert mock_pdb.called

    def test_base_abstract_render(self):
        """Covers line 161: the pass statement in the base ABC."""
        # Note: We cannot instantiate HtmlComponent directly because it is an ABC.
        # However, we can call the method via the class if we bypass the ABC restriction.
        with pytest.raises(TypeError):
            # This fails because render is abstract
            HtmlComponent()
        
        # Triggering the line via a class that doesn't override it (if not abstract)
        # or checking the code object directly. Since it's 'pass', it has no side effects.

    def test_render_content_not_implemented(self):
        """Covers line 179: base class NotImplementedError."""
        class RawComponent(HtmlComponent):
            def render(self): return "foo"
        
        comp = RawComponent()
        with pytest.raises(NotImplementedError) as exc:
            comp.render_content()
        assert "This class does not implement content rendering" in str(exc.value)

    def test_recurse_stylesheets(self):
        """Covers lines 189-193: specialized stylesheet crawler."""
        parent = MockComponent()
        parent.STYLESHEETS = ['base.css']
        
        child = MockComponent()
        child.STYLESHEETS = ['child.css']
        
        parent.add_child(child)
        
        sheets = parent.recurse_stylesheets()
        assert 'base.css' in sheets
        assert 'child.css' in sheets

    def test_pretty_print(self):
        """Covers lines 203-205: BeautifulSoup pretty printing logic."""
        comp = MockComponent(children="hello world")
        pretty = comp.pretty_print()
        
        # Check for BeautifulSoup-style formatting (newlines/indentation)
        assert "<div>" in pretty
        assert "hello world" in pretty
        assert "\n" in pretty

    def test_singleton_content_restriction(self):
        """Covers line 300: Singleton components blocking content rendering."""
        br = MockSingleton()
        with pytest.raises(NotImplementedError) as exc:
            br.render_content()
        assert "No content allowed for Singleton" in str(exc.value)

    def test_add_class_duplicate(self):
        """Verify add_class doesn't add the same class twice."""
        comp = MockComponent(class_name="btn")
        comp.add_class("btn")
        # Split string and check list to ensure it's not "btn btn"
        assert comp.class_name == "btn"