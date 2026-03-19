import pytest
import pdb
from tts_html_utils.core.components.navigation import *

class TestNavigation:
    def test_navbar(self):
        """Test basic flat navbar rendering."""
        mapping = {'Item A': 'https://A.com', 'Item B': 'https://B.com', 'Item C': 'https://C.com'}
        # Note: target="_self" is the default for Navbar (new_tab=False)
        expected = '<ul class="navbar"><li class="navbartab"><a href="https://A.com" target="_self">Item A</a></li><li class="navbartab"><a href="https://B.com" target="_self">Item B</a></li><li class="navbartab"><a href="https://C.com" target="_self">Item C</a></li></ul>'
        assert Navbar(mapping).render() == expected

    def test_nested_navbar(self):
        """Test nested navbar rendering using dicts."""
        mapping = {
            'Item A': {
                'Item A1': 'https://A1.com',
                'Item A2': 'https://A2.com',
                'Item A3': 'https://A3.com',
                },
            'Item B': 'https://B.com', 
            'Item C': {
                'Item C1': 'https://C1.com',
                'Item C2': 'https://C2.com',
                'Item C3': {
                    'Item C3.1': 'https://C31.com',
                    'Item C3.2': 'https://C32.com',
                    'Item C3.3': 'https://C33.com'
                    }
                }
            }

        expected = '<ul class="navbar"><li>Item A<ul><li class="navbartab"><a href="https://A1.com" target="_self">Item A1</a></li><li class="navbartab"><a href="https://A2.com" target="_self">Item A2</a></li><li class="navbartab"><a href="https://A3.com" target="_self">Item A3</a></li></ul></li><li class="navbartab"><a href="https://B.com" target="_self">Item B</a></li><li>Item C<ul><li class="navbartab"><a href="https://C1.com" target="_self">Item C1</a></li><li class="navbartab"><a href="https://C2.com" target="_self">Item C2</a></li><li>Item C3<ul><li class="navbartab"><a href="https://C31.com" target="_self">Item C3.1</a></li><li class="navbartab"><a href="https://C32.com" target="_self">Item C3.2</a></li><li class="navbartab"><a href="https://C33.com" target="_self">Item C3.3</a></li></ul></li></ul></li></ul>'
        assert Navbar(mapping).render() == expected

    def test_navbar_empty(self):
        """Test that an empty mapping renders an empty list with the navbar class."""
        assert Navbar({}).render() == '<ul class="navbar"></ul>'

    def test_navbar_new_tab(self):
        """Test that setting new_tab=True changes the link targets."""
        mapping = {'Item A': 'https://A.com'}
        expected = '<ul class="navbar"><li class="navbartab"><a href="https://A.com" target="_blank">Item A</a></li></ul>'
        assert Navbar(mapping, new_tab=True).render() == expected

    def test_navbar_css_inclusion(self):
        """Test that the Navbar automatically includes its CSS file."""
        nb = Navbar({})
        assert len(nb.css_includes) > 0
        path, _ = nb.css_includes[0]
        assert path.name == 'navbar.css'

    def test_navbar_add_items(self):
        """Test adding items to an existing navbar."""
        nb = Navbar({'Item A': 'https://A.com'})
        nb.add_items({'Item B': 'https://B.com'})
        
        expected = '<ul class="navbar"><li class="navbartab"><a href="https://A.com" target="_self">Item A</a></li><li class="navbartab"><a href="https://B.com" target="_self">Item B</a></li></ul>'
        assert nb.render() == expected