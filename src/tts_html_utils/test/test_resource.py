import pytest
import pdb
from pathlib import Path
from unittest.mock import patch, mock_open
from tts_html_utils.resource import (
    get_template, get_stylesheet, get_script, get_js_template,
    render_html_from_template, render_html_from_stock_template,
    compile_styles, compile_scripts,
    HTML_TEMPLATES_DIR, HTML_RESOURCES_DIR, JS_TEMPLATES_DIR
)

# --- Path Resolution Tests ---

class TestResourceRetrieval:
    
    def test_constants_structure(self):
        """Verify the directory constants point to valid locations."""
        # Verify the path logic is relative to the library structure
        assert 'resources' in str(HTML_RESOURCES_DIR)
        assert 'html_templates' in str(HTML_TEMPLATES_DIR)
        assert 'javascript' in str(JS_TEMPLATES_DIR)

    @patch('tts_html_utils.resource.Path.exists')
    def test_get_template(self, mock_exists):
        """Test finding a template file."""
        mock_exists.return_value = True
        path = get_template("test.html")
        assert path == HTML_TEMPLATES_DIR / "test.html"

    @patch('tts_html_utils.resource.Path.exists')
    def test_get_template_missing(self, mock_exists):
        """Test error when template is missing."""
        mock_exists.return_value = False
        with pytest.raises(ValueError) as exc:
            get_template("missing.html")
        assert "does not exist" in str(exc.value)

    @patch('tts_html_utils.resource.Path.exists')
    def test_get_stylesheet(self, mock_exists):
        """Test finding a stylesheet file."""
        mock_exists.return_value = True
        path = get_stylesheet("style.css")
        assert path == HTML_RESOURCES_DIR / "style.css"

    @patch('tts_html_utils.resource.Path.exists')
    def test_get_script(self, mock_exists):
        """Test finding a script file."""
        mock_exists.return_value = True
        path = get_script("app.js")
        assert path == HTML_RESOURCES_DIR / 'scripts' / "app.js"

    @patch('tts_html_utils.resource.Path.exists')
    def test_get_js_template(self, mock_exists):
        """Test finding a JS template file."""
        mock_exists.return_value = True
        path = get_js_template("dynamic.js")
        assert path == JS_TEMPLATES_DIR / "dynamic.js"

# --- Rendering Tests ---

class TestRendering:
    
    def test_render_simple(self, tmp_path):
        """Test basic Jinja2 rendering."""
        # Create a dummy template
        tpl_dir = tmp_path / "templates"
        tpl_dir.mkdir()
        tpl_file = tpl_dir / "hello.html"
        tpl_file.write_text("Hello {{ name }}!")

        result = render_html_from_template(tpl_dir, "hello.html", name="World")
        assert result == "Hello World!"

    def test_render_autoescape_xss(self, tmp_path):
        """
        SECURITY TEST: Verify that select_autoescape protects against XSS.
        We attempt to inject a script tag. It should be escaped.
        """
        tpl_dir = tmp_path / "templates"
        tpl_dir.mkdir()
        tpl_file = tpl_dir / "xss.html"
        tpl_file.write_text("User input: {{ user_input }}")

        malicious_input = "<script>alert('hacked')</script>"
        result = render_html_from_template(tpl_dir, "xss.html", user_input=malicious_input)

        # Result should NOT contain the raw script tag
        assert "<script>" not in result
        # It SHOULD contain the escaped version
        assert "&lt;script&gt;" in result

# --- Compilation Tests ---

class TestCompilation:

    def test_compile_styles_mixed_input(self):
        """Test compiling a mix of file paths and raw strings."""
        
        # We patch Path.exists. Since it is an instance method, the mock 
        # call doesn't pass the path object to the side effect.
        # We use a simple return_value and control the flow by changing 
        # the resource types.
        with patch('tts_html_utils.resource.Path.exists') as mock_exists:
            # First, we test with a Path object. _sub_compile checks 
            # isinstance(resource, Path) first, so it won't call exists().
            # Second, for the string, we want exists() to be False so it 
            # treats it as raw CSS.
            mock_exists.return_value = False

            with patch('builtins.open', mock_open(read_data="body { color: blue; }")):
                resources = [
                    Path("styles/file.css"), # Triggers the 'isinstance(resource, Path)' branch
                    "div { color: red; }"    # Triggers 'elif isinstance(resource, str)' because exists is False
                ]

                result = compile_styles(resources)

                assert "body { color: blue; }" in result
                assert "div { color: red; }" in result

    @patch('tts_html_utils.resource.render_html_from_template')
    def test_compile_scripts_wrapping(self, mock_render):
        """Test that scripts are wrapped in script tags via template."""
        mock_render.return_value = "<script>console.log('hi')</script>"
        
        scripts = ["console.log('hi')"]
        result = compile_scripts(scripts)
        
        assert len(result) == 1
        assert result[0] == "<script>console.log('hi')</script>"
        
        # Verify it called the correct template
        mock_render.assert_called_with('script_general.html', script_text="console.log('hi')")