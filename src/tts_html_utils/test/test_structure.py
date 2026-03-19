import pytest
import pdb
from tts_html_utils.core.components.structure import PaneContainer
from tts_html_utils.core.components.misc import Div
from tts_html_utils.core.components.navigation import Navbar

class TestPaneContainer:

    def test_init(self):
        """Test that the container initializes with correct defaults and resources."""
        pc = PaneContainer()
        assert pc.tag == 'div'
        assert pc.panes == {}
        assert pc.children == []
        
        # Verify JS/CSS injection
        # Note: We check if at least one resource is added, specific paths depend on environment
        assert len(pc.js_includes) > 0
        assert len(pc.css_includes) > 0
        assert "pane_container.js" in str(pc.js_includes[0][0])
        assert "pane_container.css" in str(pc.css_includes[0][0])

    def test_add_pane_single(self):
        """Test adding a single pane results in a visible pane and a navbar."""
        pc = PaneContainer(id='pane-container-a')
        content = Div("Content A")
        pc.add_pane(content, "Tab A")

        # 1. Verify internal storage
        assert "Tab A" in pc.panes
        pane_div = pc.panes["Tab A"]
        
        # 2. Verify wrapper Div attributes
        assert pane_div.attr['data-id'] == 'pane-container-a-tab-a'
        assert pane_div.attr['data-pane-name'] == 'tab-a'
        assert pane_div.attr['data-container-id'] == 'pane-container-a'
        assert "visible-pane" in pane_div._class
        assert "hidden-pane" not in pane_div._class

        # 3. Verify Structure (Navbar + Pane)
        assert len(pc.children) == 2
        assert isinstance(pc.children[0], Navbar)
        assert pc.children[1] == pane_div

    def test_add_pane_multiple_visibility(self):
        """Test that subsequent panes are hidden by default."""
        pc = PaneContainer(id='pane-container-a')
        pc.add_pane(Div("A"), "Tab A")
        pc.add_pane(Div("B"), "Tab B")

        pane_a = pc.panes["Tab A"]
        pane_b = pc.panes["Tab B"]

        # First pane visible
        assert "visible-pane" in pane_a._class
        assert "hidden-pane" not in pane_a._class
        assert pane_a.attr['data-id'] == 'pane-container-a-tab-a'

        # Second pane hidden
        assert "visible-pane" not in pane_b._class
        assert "hidden-pane" in pane_b._class
        assert pane_b.attr['data-id'] == 'pane-container-a-tab-b'

    def test_add_pane_duplicate_error(self):
        """Test that adding a duplicate pane name raises an exception."""
        pc = PaneContainer(id='pane-container-a')
        pc.add_pane(Div("A"), "Tab A")
        
        with pytest.raises(Exception) as excinfo:
            pc.add_pane(Div("B"), "Tab A")
        
        assert 'Pane "Tab A" already exists' in str(excinfo.value)

    def test_add_child_disabled(self):
        """Test that the generic add_child method is disabled."""
        pc = PaneContainer(id='pane-container-a')
        with pytest.raises(NotImplementedError) as excinfo:
            pc.add_child(Div("Fail"))
        
        assert "add_child is not available" in str(excinfo.value)

    def test_rendering(self):
        """Test the full HTML output of the container."""
        pc = PaneContainer(id='pane-container-a')
        pc.add_pane("Content A", "My Tab")
        pc.add_pane("Content B", "Other Tab")
        
        html = pc.render()
        
        # 1. Verify Container and Navbar
        assert '<div id="pane-container-a" class="pane-container" data-container-id="pane-container-a">' in html
        assert '<ul class="navbar">' in html
        
        # 2. Verify Links
        assert '<li class="navbartab"><a href="#pane-container-a-my-tab" target="_self">My Tab</a></li>' in html
        assert '<li class="navbartab"><a href="#pane-container-a-other-tab" target="_self">Other Tab</a></li>' in html

        # 3. Verify Panes
        assert '<div class="visible-pane" data-id="pane-container-a-my-tab" data-pane-name="my-tab" data-container-id="pane-container-a">Content A</div>' in html
        assert '<div class="hidden-pane" data-id="pane-container-a-other-tab" data-pane-name="other-tab" data-container-id="pane-container-a">Content B</div>' in html
        
    def test_nested_pane_containers(self):
        """Test that pane containers can be nested inside other pane containers."""
        # Create outer container
        outer_container = PaneContainer(id='outer-container')
        
        # Create inner container
        inner_container = PaneContainer(id='inner-container')
        
        # Add panes to inner container
        inner_container.add_pane("Inner Content A", "Inner Tab A")
        inner_container.add_pane("Inner Content B", "Inner Tab B")
        
        # Add inner container and other content to outer container
        outer_container.add_pane("Outer Content", "Outer Tab A")
        outer_container.add_pane(inner_container, "Nested Container")
        
        # Render the HTML
        html = outer_container.render()
        
        # 1. Verify outer container structure
        assert '<div id="outer-container" class="pane-container" data-container-id="outer-container">' in html
        assert '<li class="navbartab"><a href="#outer-container-outer-tab-a" target="_self">Outer Tab A</a></li>' in html
        assert '<li class="navbartab"><a href="#outer-container-nested-container" target="_self">Nested Container</a></li>' in html
        
        # 2. Verify inner container structure
        assert '<div id="inner-container" class="pane-container" data-container-id="inner-container">' in html
        assert '<li class="navbartab"><a href="#inner-container-inner-tab-a" target="_self">Inner Tab A</a></li>' in html
        assert '<li class="navbartab"><a href="#inner-container-inner-tab-b" target="_self">Inner Tab B</a></li>' in html
        
        # 3. Verify inner container panes
        assert '<div class="visible-pane" data-id="inner-container-inner-tab-a" data-pane-name="inner-tab-a" data-container-id="inner-container">Inner Content A</div>' in html
        assert '<div class="hidden-pane" data-id="inner-container-inner-tab-b" data-pane-name="inner-tab-b" data-container-id="inner-container">Inner Content B</div>' in html
        
    def test_three_level_nested_pane_containers(self):
        """Test three levels of nested pane containers."""
        # Create containers for each level
        outer_container = PaneContainer(id='level1-container')
        middle_container = PaneContainer(id='level2-container')
        inner_container = PaneContainer(id='level3-container')
        
        # Add panes to the innermost (level 3) container
        inner_container.add_pane("Level 3 Content A", "L3 Tab A")
        inner_container.add_pane("Level 3 Content B", "L3 Tab B")
        
        # Add panes to the middle (level 2) container, including the inner container
        middle_container.add_pane("Level 2 Content", "L2 Tab A")
        middle_container.add_pane(inner_container, "L2 Nested Tab")
        
        # Add panes to the outer (level 1) container, including the middle container
        outer_container.add_pane("Level 1 Content", "L1 Tab A")
        outer_container.add_pane(middle_container, "L1 Nested Tab")
        
        # Render the HTML
        html = outer_container.render()
        
        # 1. Verify level 1 (outer) container structure
        assert '<div id="level1-container" class="pane-container" data-container-id="level1-container">' in html
        assert '<li class="navbartab"><a href="#level1-container-l1-tab-a" target="_self">L1 Tab A</a></li>' in html
        assert '<li class="navbartab"><a href="#level1-container-l1-nested-tab" target="_self">L1 Nested Tab</a></li>' in html
        
        # 2. Verify level 2 (middle) container structure
        assert '<div id="level2-container" class="pane-container" data-container-id="level2-container">' in html
        assert '<li class="navbartab"><a href="#level2-container-l2-tab-a" target="_self">L2 Tab A</a></li>' in html
        assert '<li class="navbartab"><a href="#level2-container-l2-nested-tab" target="_self">L2 Nested Tab</a></li>' in html
        
        # 3. Verify level 3 (inner) container structure
        assert '<div id="level3-container" class="pane-container" data-container-id="level3-container">' in html
        assert '<li class="navbartab"><a href="#level3-container-l3-tab-a" target="_self">L3 Tab A</a></li>' in html
        assert '<li class="navbartab"><a href="#level3-container-l3-tab-b" target="_self">L3 Tab B</a></li>' in html
        
        # 4. Verify content in each level
        assert '<div class="visible-pane" data-id="level1-container-l1-tab-a" data-pane-name="l1-tab-a" data-container-id="level1-container">Level 1 Content</div>' in html
        assert '<div class="visible-pane" data-id="level2-container-l2-tab-a" data-pane-name="l2-tab-a" data-container-id="level2-container">Level 2 Content</div>' in html
        assert '<div class="visible-pane" data-id="level3-container-l3-tab-a" data-pane-name="l3-tab-a" data-container-id="level3-container">Level 3 Content A</div>' in html
        assert '<div class="hidden-pane" data-id="level3-container-l3-tab-b" data-pane-name="l3-tab-b" data-container-id="level3-container">Level 3 Content B</div>' in html