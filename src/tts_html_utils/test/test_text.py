import pytest
import pdb
from tts_html_utils.core.components.text import *
from tts_html_utils.core.components.base import HtmlComponent

class TestText:
    def test_headings(self):
        """Test rendering of all header levels and their aliases."""
        # Full class names
        assert Heading1('Heading 1 Test').render() == '<h1>Heading 1 Test</h1>'
        assert Heading2('Heading 2 Test').render() == '<h2>Heading 2 Test</h2>'
        assert Heading3('Heading 3 Test').render() == '<h3>Heading 3 Test</h3>'
        assert Heading4('Heading 4 Test').render() == '<h4>Heading 4 Test</h4>'
        assert Heading5('Heading 5 Test').render() == '<h5>Heading 5 Test</h5>'
        assert Heading6('Heading 6 Test').render() == '<h6>Heading 6 Test</h6>'

        # Aliases
        assert H1('H1 Test').render() == '<h1>H1 Test</h1>'
        assert H2('H2 Test').render() == '<h2>H2 Test</h2>'
        assert H3('H3 Test').render() == '<h3>H3 Test</h3>'
        assert H4('H4 Test').render() == '<h4>H4 Test</h4>'
        assert H5('H5 Test').render() == '<h5>H5 Test</h5>'
        assert H6('H6 Test').render() == '<h6>H6 Test</h6>'

    def test_other_text(self):
        """Test rendering of standard text formatting tags."""
        assert Paragraph('Paragraph Test').render() == '<p>Paragraph Test</p>'
        assert P('P Test').render() == '<p>P Test</p>'
        assert Span('Span Test').render() == '<span>Span Test</span>'
        assert Strong('Strong Test').render() == '<strong>Strong Test</strong>'
        assert Pre('Pre Test').render() == '<pre>Pre Test</pre>'

    def test_text_attributes(self):
        """
        Verify that text components correctly handle standard HTML attributes
        (ID, class, style) inherited from HtmlComponentSimple.
        """
        # Test using Paragraph as a representative sample
        p = Paragraph(
            "Styled Text", 
            id="my-p", 
            class_name="text-muted", 
            style={'color': 'red', 'font-weight': 'bold'}
        )
        
        html = p.render()
        
        assert '<p' in html
        assert 'id="my-p"' in html
        assert 'class="text-muted"' in html
        # Styles might be ordered differently depending on python version/dict implementation, 
        # but usually consistent. Checking substring existence.
        assert 'style="color: red; font-weight: bold;"' in html
        assert '>Styled Text</p>' in html

    def test_nesting(self):
        """Test nesting text components (e.g. a Strong tag inside a Paragraph)."""
        # Structure: <p>Normal <strong>Bold</strong> Text</p>
        child = Strong("Bold")
        p = Paragraph(children=["Normal ", child, " Text"])
        
        assert p.render() == '<p>Normal <strong>Bold</strong> Text</p>'