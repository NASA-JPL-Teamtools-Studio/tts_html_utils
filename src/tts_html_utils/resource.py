#Standard Library Imports
from pathlib import Path
import pdb

#Installed dependency imports
# UPDATE: Added select_autoescape to fix B701 XSS vulnerability
from jinja2 import FileSystemLoader, Environment, select_autoescape

#Teamtools Studio Imports
from tts_utilities.logger import create_logger

#This Library Imports
#None yet

logger = create_logger(name='html_utils.resource')

#================================================
# :: Constants
#================================================
# MM_REPORT_TEMPLATES_DIR = Path(mm_report_simreport_file).parent.parent / 'templates'

# These constants define the location of the library's assets on the file system.
# This ensures that no matter where this code is run from, it can always find its 
# internal stylesheets and templates relative to the current file.
HTML_RESOURCES_DIR = Path(__file__).parent / 'resources'
HTML_TEMPLATES_DIR = HTML_RESOURCES_DIR / 'html_templates'
JS_TEMPLATES_DIR = Path(__file__).parent / 'javascript'

#================================================
# :: Generic Retrieval
#================================================
# def get_mm_report_template(fname):
#     target = MM_REPORT_TEMPLATES_DIR / fname
#     if not target.exists():
#         raise ValueError(f'HTML template file "{fname}" does not exist in mm_report_utilities')
#     return target

def get_template(fname):
    """
    Locates an HTML template file within the library's internal `html_templates` directory.

    **Concept:**
    Instead of writing hardcoded HTML strings in Python code, we store them as 
    separate `.html` files. This function grabs the path to one of those files 
    so it can be loaded by the Jinja2 engine.

    :param fname: The filename of the template (e.g., 'table_component.html').
    :type fname: str
    :return: The full absolute path to the file.
    :rtype: Path
    :raises ValueError: If the file does not exist.
    """
    target = HTML_TEMPLATES_DIR / fname
    if not target.exists():
        raise ValueError(f'HTML template file "{fname}" does not exist in HTML Utilities')
    return target

def get_stylesheet(fname):
    """
    Locates a CSS stylesheet within the library's internal resources.

    :param fname: The filename of the stylesheet (e.g., 'default_styles.css').
    :type fname: str
    :return: The full absolute path to the file.
    :rtype: Path
    :raises ValueError: If the file does not exist.
    """
    target = HTML_RESOURCES_DIR / fname
    if not target.exists():
        raise ValueError(f'Stylesheet file "{fname}" does not exist in HTML Utilities')
    return target

def get_script(fname):
    """
    Locates a JavaScript file within the library's internal `scripts` directory.

    :param fname: The filename of the script (e.g., 'sort_table.js').
    :type fname: str
    :return: The full absolute path to the file.
    :rtype: Path
    :raises ValueError: If the file does not exist.
    """
    target = HTML_RESOURCES_DIR / 'scripts' / fname
    if not target.exists():
        raise ValueError(f'Script file "{fname}" does not exist in HTML Utilities')
    return target

def get_js_template(fname):
    """
    Locates a JavaScript template within the library's internal `javascript` directory.

    **Note:** A "JS Template" is a JavaScript file that contains Python variables (Jinja syntax).
    Example: `var data = {{ python_data_variable }};`
    These need to be rendered before the browser can understand them.

    :param fname: The filename of the JS template.
    :type fname: str
    :return: The full absolute path to the file.
    :rtype: Path
    :raises ValueError: If the file does not exist.
    """
    target = JS_TEMPLATES_DIR / fname
    if not target.exists():
        raise ValueError(f'Script file "{fname}" does not exist in HTML Utilities')
    return target

#================================================
# jinja2 rendering
#================================================
def render_html_from_template(template_dir, template_name, **template_kwargs):
    """
    The core rendering engine.

    This function uses **Jinja2** to take a template file (HTML with holes in it) 
    and a dict of python variables (the data to fill the holes) and produces a final 
    HTML string.

    **Security Note (XSS):**
    We enable `autoescape=True` for HTML and XML files. This prevents Cross-Site Scripting 
    attacks. If a user tries to inject a variable containing `<script>alert('hack')</script>`, 
    Jinja automatically converts it to safe text (`&lt;script&gt;...`) so it displays 
    as text rather than executing as code.

    :param template_dir: The directory where the template file resides.
    :type template_dir: str or Path
    :param template_name: The name of the specific file to load.
    :type template_name: str
    :param template_kwargs: Key-value pairs representing variables to inject into the template.
    :return: The fully rendered HTML string.
    :rtype: str
    """
    # UPDATE: Enable autoescape for HTML and XML files to prevent XSS
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template(template_name)
    return template.render(template_kwargs)

# def render_html_from_mm_template(template_name, **template_kwargs):
#     return render_html_from_template(MM_REPORT_TEMPLATES_DIR, template_name, **template_kwargs)

def render_html_from_stock_template(template_name, **template_kwargs):
    """
    A shortcut wrapper for `render_html_from_template`.

    This function assumes you want to use one of the "Stock" templates provided 
    by this library (located in `HTML_TEMPLATES_DIR`), rather than a custom file.

    :param template_name: The name of the stock template file.
    :type template_name: str
    :param template_kwargs: Variables to inject into the template.
    :return: The rendered HTML string.
    :rtype: str
    """
    return render_html_from_template(HTML_TEMPLATES_DIR, template_name, **template_kwargs)

#================================================
# Compilation shorthand
#================================================
def _sub_compile(resources):
    """
    A helper utility to normalize input resources.

    **The Problem:**
    Sometimes a user provides a file path ("styles.css"). Other times, they provide 
    the raw CSS string itself ("body { color: red; }").

    **The Solution:**
    This function iterates through a list of resources. 
    - If it sees a file path, it opens the file and reads the content.
    - If it sees a raw string, it keeps it as-is.
    
    This allows our components to be flexible—they can accept files or raw text interchangeably.

    :param resources: A mixed list of file paths (Path or str) and/or raw content strings.
    :type resources: list
    :return: A list of strings, where every item is the actual content text.
    :rtype: list[str]
    """
    all_resources = []
    for resource in resources:
        if isinstance(resource, Path) or (len(resource) < 255 and Path(resource).exists()):
            # Assume this is a file we should read
            with open(resource, 'r') as f:
                all_resources.append(f.read())
        elif isinstance(resource, str):
            # Assume this is just the actual style text
            all_resources.append(resource)
        else:
            raise TypeError(f'Unexpected format for resource information: {type(resource)}')
    return all_resources

def compile_styles(styles):
    """
    Extracts the CSS content from a list of style resources.

    :param styles: A list of CSS file paths or raw CSS strings.
    :type styles: list
    :return: A list of strings containing the CSS code.
    :rtype: list[str]
    """
    return _sub_compile(styles)

def compile_scripts(scripts):
    """
    Extracts JavaScript content and wraps it in HTML `<script>` tags.

    This function goes one step further than `compile_styles`. Since JavaScript 
    cannot just be dumped into the page (it must be inside a `<script>` block), 
    this function reads the content and then uses the `script_general.html` 
    template to wrap it properly.

    :param scripts: A list of JS file paths or raw JS strings.
    :type scripts: list
    :return: A list of HTML strings, each containing a full `<script>...</script>` block.
    :rtype: list[str]
    """
    script_texts = _sub_compile(scripts)
    all_script_html = []
    for script_text in script_texts:
        all_script_html.append(
            render_html_from_template('script_general.html', script_text=script_text)
        )
    return all_script_html