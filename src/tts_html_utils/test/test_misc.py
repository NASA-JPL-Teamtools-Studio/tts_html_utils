import pytest
from tts_html_utils.core.components.misc import *
import pdb

class TestMisc:
    
    # --- Structural/Container Tags ---
    def test_header(self):
        """Test Header rendering."""
        assert Header('Header Test').render() == '<header>Header Test</header>'

    def test_footer(self):
        """Test Footer rendering."""
        assert Footer('Footer Test').render() == '<footer>Footer Test</footer>'

    def test_div(self):
        """Test Div rendering."""
        assert Div('Div Test').render() == '<div>Div Test</div>'
    
    def test_basic_containers(self):
        """Test other basic container tags not covered above."""
        # These are usually managed by the compiler, but we verify 
        # the class definitions remain valid.
        assert HTML("Content").render() == '<html>Content</html>'
        assert Head("Content").render() == '<head>Content</head>'
        assert Body("Content").render() == '<body>Content</body>'
        assert Title('Page Title').render() == '<title>Page Title</title>'

    def test_raw_code_containers(self):
        """Test containers meant for raw code (Style/Script)."""
        css = ".class { color: red; }"
        js = "console.log('test');"
        assert Style(css).render() == f'<style>{css}</style>'
        assert Script(js).render() == f'<script>{js}</script>'

    # --- Void Elements ---
    def test_hr(self):
        """Test HR renders with its default class."""
        # Test class instantiation directly
        assert HorizontalBreak().render() == '<hr class="faded">'
        # Test alias
        assert HR().render() == '<hr class="faded">'
        # Test overriding class
        assert HR(class_name="bold").render() == '<hr class="bold">'

    def test_br(self):
        """Test BR renders as a void tag."""
        assert LineBreak().render() == '<br>'
        assert BR().render() == '<br>'

    # --- Interactive Elements ---
    def test_link(self):
        """Test basic Link rendering."""
        assert Link('Link Test', href='https://jpl.nasa.gov/').render() == '<a href="https://jpl.nasa.gov/" target="_blank">Link Test</a>'
        assert A('Anchor Test', href='https://jpl.nasa.gov/').render() == '<a href="https://jpl.nasa.gov/" target="_blank">Anchor Test</a>'

    def test_link_defaults(self):
        """Test Link defaults to new_tab=True."""
        expected = '<a href="https://jpl.nasa.gov/" target="_blank">Link Test</a>'
        assert Link('Link Test', href='https://jpl.nasa.gov/').render() == expected

    def test_link_same_tab(self):
        """Test Link with new_tab=False sets target=_self."""
        expected = '<a href="https://google.com" target="_self">Link Test</a>'
        assert Link('Link Test', href='https://google.com', new_tab=False).render() == expected

    def test_link_href_inference(self):
        """Test that if href is omitted, the text is used as the URL."""
        url = "https://jpl.nasa.gov"
        expected = f'<a href="{url}" target="_blank">{url}</a>'
        assert Link(url).render() == expected

    def test_button(self):
        """Test basic Button rendering."""
        assert Button('Button Test').render() == '<button type="button">Button Test</button>'

    def test_button_types(self):
        """Test setting specific button types (submit/reset)."""
        assert Button('Submit', button_type='submit').render() == '<button type="submit">Submit</button>'
        assert Button('Reset', button_type='reset').render() == '<button type="reset">Reset</button>'

    # --- Special Components ---
    def test_favicon(self):
        """
        Test that TtsFavicon injects the javascript payload into js_includes.
        It does not render content directly to HTML (it's empty), 
        but relies on the compiler to pick up the js_includes.
        """
        fav = TtsFavicon()
        
        # Should render as an empty script tag (or just be a vehicle for metadata)
        # Inherits from Script, so it renders <script></script> if empty children
        assert fav.render() == '<script></script>'
        
        # Verify the payload exists
        assert len(fav.js_includes) > 0
        js_payload, _ = fav.js_includes[0]
        
        # Check for critical parts of the logic
        assert "document.createElement('link')" in js_payload
        assert "favicon.rel = 'icon'" in js_payload
        assert "document.head.appendChild(favicon)" in js_payload

    def test_link_with_extra_attr(self):
        """Test passing explicit attributes via kwargs covers the merge logic."""
        # This triggers lines 207-208
        link = Link('Text', attr={'title': 'Hover Text', 'data-id': '123'})
        html = link.render()
        
        assert 'title="Hover Text"' in html
        assert 'data-id="123"' in html
        # Verify default attrs like href/target are preserved
        assert 'href="Text"' in html 

    def test_button_with_extra_attr(self):
        """Test passing explicit attributes via kwargs covers the merge logic."""
        # This triggers lines 235-236
        btn = Button('Click Me', attr={'onclick': 'alert(1)', 'disabled': 'true'})
        html = btn.render()
        
        assert 'onclick="alert(1)"' in html
        assert 'disabled="true"' in html
        # Verify default type='button' is preserved
        assert 'type="button"' in html    

    def test_link_attr_merging(self):
        """Covers lines 207-208: merging custom attributes into Links."""
        # Triggering the 'if attr in kwargs' branch
        link = Link('Home', href='/', attr={'id': 'nav-home', 'class': 'custom'})
        html = link.render()
        assert 'id="nav-home"' in html
        assert 'href="/"' in html

    def test_button_attr_merging(self):
        """Covers lines 235-236: merging custom attributes into Buttons."""
        # Triggering the 'if attr in kwargs' branch
        btn = Button('Click', attr={'data-id': '123', 'disabled': 'disabled'})
        html = btn.render()
        assert 'data-id="123"' in html
        assert 'disabled="disabled"' in html
        assert 'type="button"' in html

    def test_div_basic(self):
        div = Div("Content")
        assert div.render() == "<div>Content</div>"            