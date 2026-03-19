import pytest
from tts_html_utils.core.components.list import *
import pdb
class TestList:
    def test_unordered_list(self):
        """Test basic UL rendering."""
        assert UnorderedList([ListItem(str(ii)) for ii in range(4)]).render() == '<ul><li>0</li><li>1</li><li>2</li><li>3</li></ul>'
        assert UL([LI(str(ii)) for ii in range(4)]).render() == '<ul><li>0</li><li>1</li><li>2</li><li>3</li></ul>'

    def test_ordered_list(self):
        """Test basic OL rendering."""
        assert OrderedList([ListItem(str(ii)) for ii in range(4)]).render() == '<ol><li>0</li><li>1</li><li>2</li><li>3</li></ol>'
        assert OL([LI(str(ii)) for ii in range(4)]).render() == '<ol><li>0</li><li>1</li><li>2</li><li>3</li></ol>'

    def test_list_item_attributes(self):
        """Test that ListItems render styles and classes correctly."""
        li = LI("Item", class_name="active", style={'color': 'red'})
        assert li.render() == '<li class="active" style="color: red;">Item</li>'

    def test_powerlist_basic(self):
        """Test the basic indented structure functionality from the original test."""
        pl = PowerList()
        pl.line(1)
        pl.line(2)
        pl.up_level()
        pl.line(3)
        pl.line(4)
        pl.up_level(ordered=True)
        pl.line(5)
        pl.line(6)
        pl.down_level()
        pl.line(7)
        pl.line(8)
        pl.down_level()
        pl.line(9)
        pl.line(10)
        
        expected = (
            '<ul>'
            '<li>1</li>'
            '<li>2</li>'
            '<li>'  # up_level() creates a new wrapper LI
                '<ul>'
                '<li>3</li>'
                '<li>4</li>'
                '<li>' # up_level(ordered=True) creates wrapper LI
                    '<ol>'
                    '<li>5</li>'
                    '<li>6</li>'
                    '</ol>'
                '</li>'
                '<li>7</li>'
                '<li>8</li>'
                '</ul>'
            '</li>'
            '<li>9</li>'
            '<li>10</li>'
            '</ul>'
        )
        assert pl.render() == expected

    def test_powerlist_init_args(self):
        """Test initializing PowerList with children, classes, and style."""
        # Initialize with one child
        pl = PowerList(children=[LI("First")], class_name="my-list", style={"padding": "10px"}, ordered=True)
        pl.line("Second")
        
        expected = '<ol class="my-list" style="padding: 10px;"><li>First</li><li>Second</li></ol>'
        assert pl.render() == expected

    def test_powerlist_line_attributes(self):
        """Test passing classes and styles to the .line() method."""
        pl = PowerList()
        pl.line("Plain")
        pl.line("Styled", class_name="highlight", style={"font-weight": "bold"})
        
        expected = '<ul><li>Plain</li><li class="highlight" style="font-weight: bold;">Styled</li></ul>'
        assert pl.render() == expected

    def test_powerlist_up_level_with_label(self):
        """Test up_level with a label (text that appears before the nested list starts)."""
        pl = PowerList()
        pl.line("Item 1")
        # This should create: <li>Item 1</li> <li>Subgroup Title <ul>...</ul></li>
        pl.up_level(label="Subgroup Title") 
        pl.line("Item 1.1")
        
        expected = '<ul><li>Item 1</li><li>Subgroup Title<ul><li>Item 1.1</li></ul></li></ul>'
        assert pl.render() == expected

    def test_powerlist_up_level_styling(self):
        """Test passing classes/styles to the nested list via up_level."""
        pl = PowerList()
        pl.line("Root Item")
        # The nested UL should have the class 'nested-list'
        pl.up_level(class_name="nested-list", ordered=True)
        pl.line("Nested Item")
        
        expected = '<ul><li>Root Item</li><li><ol class="nested-list"><li>Nested Item</li></ol></li></ul>'
        assert pl.render() == expected

    def test_powerlist_down_level_safety(self):
        """Test that calling down_level at the root doesn't crash or remove the root."""
        pl = PowerList()
        pl.line("A")
        pl.down_level() # Should do nothing
        pl.down_level() # Should still do nothing
        pl.line("B")
        
        assert pl.render() == '<ul><li>A</li><li>B</li></ul>'

    def test_powerlist_custom_new_list(self):
        """Test passing a specific list instance to up_level."""
        pl = PowerList()
        pl.line("A")
        
        # Manually creating the sub-list structure
        custom_sub = PowerList(ordered=True, class_name="custom")
        custom_sub.line("B")
        
        # Injecting it via up_level
        # Note: up_level adds the new_list to the stack, so subsequent .line() calls go into it
        pl.up_level(new_list=custom_sub) 
        pl.line("C") # Should go into custom_sub
        
        expected = '<ul><li>A</li><li><ol class="custom"><li>B</li><li>C</li></ol></li></ul>'
        assert pl.render() == expected