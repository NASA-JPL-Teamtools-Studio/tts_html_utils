import pytest
from pathlib import Path
from tts_html_utils.core.compiler import HtmlCompiler, make_hashable, group_by_path_with_unique_dicts
from tts_html_utils.core.components.base import HtmlComponent
from tts_html_utils.core.components.misc import Div

# --- Helper Function Tests ---

class TestHelpers:
    def test_make_hashable(self):
        """Test converting mutable structures to hashable types."""
        # Dict -> frozenset of items
        d = {'a': 1, 'b': 2}
        h_d = make_hashable(d)
        assert isinstance(h_d, frozenset)
        assert dict(h_d) == d

        # List -> tuple
        l = [1, 2, 3]
        h_l = make_hashable(l)
        assert isinstance(h_l, tuple)
        assert h_l == (1, 2, 3)

        # Set -> frozenset
        s = {1, 2}
        h_s = make_hashable(s)
        assert isinstance(h_s, frozenset)
        
        # Nested structure
        complex_obj = {'a': [1, 2], 'b': {'c': 3}}
        h_complex = make_hashable(complex_obj)
        assert isinstance(h_complex, frozenset) # Root is dict
        
        # Verify we can use it in a set (the whole point of the function)
        test_set = {h_complex}
        assert len(test_set) == 1

    def test_group_by_path_deduplication(self):
        """Test grouping by path and removing duplicate configurations."""
        path_a = Path("a.js")
        path_b = Path("b.js")
        
        config_1 = {'param': 1}
        config_2 = {'param': 2}
        config_1_dup = {'param': 1} # Same as 1

        input_data = [
            (path_a, config_1),
            (path_a, config_1_dup), # Duplicate
            (path_a, config_2),     # Different config, same path
            (path_b, config_1)      # Different path
        ]

        result = group_by_path_with_unique_dicts(input_data)
        
        # Convert list of tuples to dict for easier assertions
        result_map = {p: configs for p, configs in result}

        # Path A should have 2 unique configs (config_1 and config_2)
        assert len(result_map[path_a]) == 2
        # We can't guarantee order of the list, so check existence
        assert config_1 in result_map[path_a]
        assert config_2 in result_map[path_a]

        # Path B should have 1 config
        assert len(result_map[path_b]) == 1
        assert result_map[path_b][0] == config_1

# --- Compiler Tests ---

class MockComponent(HtmlComponent):
    """A helper component to simulate dependencies."""
    def __init__(self, css=None, js=None):
        super().__init__()
        self.css_includes = css if css else []
        self.js_includes = js if js else []
    
    def render(self):
        return ""

class TestHtmlCompiler:
    
    def test_init(self):
        """Test initialization defaults."""
        compiler = HtmlCompiler("My Title")
        assert compiler.title == "My Title"
        # Should have favicon by default
        assert len(compiler.head_components) == 1 
        assert compiler.body_components == []

    def test_add_components_valid(self):
        """Test adding valid components to head and body."""
        compiler = HtmlCompiler("Test")
        div = Div("Body Content")
        
        compiler.add_body_component(div)
        assert div in compiler.body_components

        # Mock a head component
        meta = MockComponent()
        compiler.add_head_component(meta)
        assert meta in compiler.head_components

    def test_add_components_invalid(self):
        """Test type checking for components."""
        compiler = HtmlCompiler("Test")
        with pytest.raises(Exception) as exc:
            compiler.add_body_component("Not a component")
        assert "not an HtmlComponent" in str(exc.value)

        with pytest.raises(Exception) as exc:
            compiler.add_head_component(123)
        assert "not an HtmlComponent" in str(exc.value)

    def test_compile_structure(self):
        """Test basic structural compilation without external dependencies."""
        compiler = HtmlCompiler("Structure Test")
        compiler.add_body_component(Div("Hello World"))
        
        # Render full HTML
        html = compiler.render()
        
        assert "<html>" in html
        assert "<head>" in html
        assert "<title>Structure Test</title>" in html
        
        # Updated assertion to match the hardcoded style in compiler.compile()
        assert '<body style="padding: 10px;">' in html
        assert "<div>Hello World</div>" in html

    def test_dependency_injection_string(self, tmp_path):
        """Test injecting raw string paths (like CDNs)."""
        compiler = HtmlCompiler("CDN Test")
        
        # Component requesting a CDN link
        comp = MockComponent(
            css=[("https://cdn.com/style.css", {})],
            js=[("https://cdn.com/script.js", {})]
        )
        compiler.add_body_component(comp)
        
        html = compiler.render()
        
        # Check direct injection into Head
        assert '<style>https://cdn.com/style.css</style>' in html
        assert '<script src="https://cdn.com/script.js"></script>' in html

    def test_dependency_injection_file_template(self, tmp_path):
        """
        Test injecting local file resources.
        Verifies:
        1. File reading
        2. Jinja2 rendering using the config dict
        3. Injection into <style> and <script> tags
        """
        # 1. Create dummy resource files
        css_file = tmp_path / "style.css"
        css_file.write_text(".my-class { color: {{ color }}; }")
        
        js_file = tmp_path / "script.js"
        js_file.write_text("const value = {{ number }} * 2;")

        # 2. Configure compiler with component requesting these files
        compiler = HtmlCompiler("Resource Test")
        
        comp = MockComponent(
            css=[(css_file, {'color': 'red'})],
            js=[(js_file, {'number': 10})]
        )
        compiler.add_body_component(comp)

        # 3. Render
        html = compiler.render()

        # 4. Verify Jinja rendering occurred
        assert ".my-class { color: red; }" in html
        assert "const value = 10 * 2;" in html

    def test_dependency_deduplication(self, tmp_path):
        """Test that identical dependencies are included only once."""
        css_file = tmp_path / "style.css"
        css_file.write_text("body { background: {{ bg }}; }")

        compiler = HtmlCompiler("Dedupe Test")

        # Two components requesting EXACT same resource + config
        comp1 = MockComponent(css=[(css_file, {'bg': 'white'})])
        comp2 = MockComponent(css=[(css_file, {'bg': 'white'})])
        
        compiler.add_body_component(comp1)
        compiler.add_body_component(comp2)

        html = compiler.render()

        # Should only appear once
        count = html.count("body { background: white; }")
        assert count == 1

    def test_dependency_multiconfig(self, tmp_path):
        """Test that the same file with DIFFERENT configs is included twice."""
        css_file = tmp_path / "style.css"
        css_file.write_text(".box { width: {{ width }}px; }")

        compiler = HtmlCompiler("Multi Config Test")

        comp1 = MockComponent(css=[(css_file, {'width': 100})])
        comp2 = MockComponent(css=[(css_file, {'width': 200})])
        
        compiler.add_body_component(comp1)
        compiler.add_body_component(comp2)

        html = compiler.render()

        assert ".box { width: 100px; }" in html
        assert ".box { width: 200px; }" in html

    def test_render_to_file(self, tmp_path):
        """Test writing output to a file."""
        output_file = tmp_path / "output.html"
        compiler = HtmlCompiler("File Test")
        compiler.add_body_component(Div("File Content"))
        
        compiler.render_to_file(output_file)
        
        assert output_file.exists()
        content = output_file.read_text()
        assert "File Content" in content