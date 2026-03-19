#Standard Library Imports
import pdb
from collections import defaultdict
from typing import List, Tuple, Dict, Any
from pathlib import Path
import html

#Installed dependency imports
from jinja2 import Template

#Teamtools Studio Imports
from tts_utilities.logger import create_logger

#This Library Imports
from tts_html_utils.core.components.base import HtmlComponent
from tts_html_utils.core.components.misc import HTML, Head, Body, Footer, Style, Script, TtsFavicon, Title

logger = create_logger(name='html_utils.core.components.base')

def make_hashable(obj: Any):
    """
    Recursively converts mutable objects (dicts, lists) into immutable equivalents 
    (frozensets, tuples) to facilitate uniqueness checks.

    This is necessary because we need to detect duplicate configuration dictionaries 
    when aggregating resources. Since Python `sets` cannot contain mutable dictionaries, 
    we must freeze them first to check if they are identical.

    :param obj: The object to convert.
    :return: An immutable, hashable version of the input.
    """
    if isinstance(obj, dict):
        return frozenset((k, make_hashable(v)) for k, v in obj.items())
    elif isinstance(obj, list):
        return tuple(make_hashable(v) for v in obj)
    elif isinstance(obj, set):
        return frozenset(make_hashable(v) for v in obj)
    else:
        return obj

def group_by_path_with_unique_dicts(tuples: List[Tuple[Path, Dict]]) -> List[Tuple[Path, List[Dict]]]:
    """
    Groups resource requests by file path and removes duplicate configurations.

    This is used to manage dependencies efficiently. For example, if multiple 
    components request the same JavaScript library with identical settings, 
    this ensures the library is only loaded once. If they request the same 
    library with *different* settings, both configurations are preserved.

    :param tuples: A list of (FilePath, ConfigDict) pairs.
    :return: A list of tuples where each FilePath is associated with a list of unique ConfigDicts.
    """
    grouped = defaultdict(set)

    for path, meta in tuples:
        hashable_meta = make_hashable(meta)
        grouped[path].add(hashable_meta)

    result = [
        (path, [dict(items) for items in dicts])
        for path, dicts in grouped.items()
    ]

    return result


class HtmlCompiler:
    """
    Manages the lifecycle of an HTML document, handling component aggregation 
    and dependency resolution.

    This class abstracts away the manual construction of the `<html>` structure. 
    It allows you to add Python component objects from this libary to the 
    Head or Body, and automatically handles the "plumbing"—ensuring that any 
    CSS or JavaScript required by those components is injected into the document 
    correctly and without duplication.

    :param title: The document title (displayed in the browser tab).
    """
    def __init__(self, title):
        self.title = title
        self.head_components = [TtsFavicon()]
        self.body_components = list()
        self.scripts = list()
        self.styles = list()

    def add_head_component(self, component):
        """
        Adds a component to the `<head>` section of the document.

        The Head is used for metadata and configuration that is not directly 
        displayed on the page canvas (e.g., meta tags, third-party analytics scripts, 
        favicons, or social media open graph tags).

        :param component: An `HtmlComponent` appropriate for the head section.
        """
        if isinstance(component, HtmlComponent):
            self.head_components.append(component)
        else:
            raise Exception(f"{component} is not an HtmlComponent")

    def add_body_component(self, component):
        """
        Adds a component to the `<body>` section of the document.

        The Body contains the visible content of the page. Use this for 
        visual elements like layout containers, text, tables, and widgets.

        :param component: An `HtmlComponent` appropriate for the body section.
        """
        if isinstance(component, HtmlComponent):
            self.body_components.append(component)
        else:
            raise Exception(f"{component} is not an HtmlComponent")

    def compile(self):
        """
        Assembles the final object tree for the HTML document.

        This method performs dependency injection and deduplication:
        1. **Aggregation:** Scans all added components to find their required CSS/JS files.
        2. **Deduplication:** Ensures shared resources (like a common plotting library) are not included twice.
        3. **Rendering:** processes any Jinja2 templates found in the resource files.
        4. **Construction:** Builds the root `HTML` object containing the configured `Head` and `Body`.

        :return: The root `HTML` object ready for final string rendering.
        """
        css_includes = []
        js_includes = []

        # 1. Collect dependencies from all components
        for component in self.head_components + self.body_components:
            css_includes += component.aggregate_attributes('css_includes')
            js_includes += component.aggregate_attributes('js_includes')

        # 2. Remove duplicates
        css_includes = group_by_path_with_unique_dicts(css_includes)
        js_includes = group_by_path_with_unique_dicts(js_includes)

        document = HTML()
        head = Head()
        head.add_child(Title(self.title))

        # 3. Process and attach CSS
        for path, dicts in css_includes:
            if isinstance(path, str):
                # Direct string path inclusion (e.g. for CDNs)
                head.add_child(Style(path))
                continue
            
            # Render template-based CSS files
            css_template_text = path.open('r').read()
            template = Template(css_template_text)
            for d in dicts:
                rendered_css = template.render(**d)
                head.add_child(Style(rendered_css))

        # 4. Process and attach JS
        for path, dicts in js_includes:
            if isinstance(path, str):
                # Direct string path inclusion
                head.add_child(Script(attr={'src': path}))
                continue
            
            # Render template-based JS files
            js_template_text = path.open('r').read()
            template = Template(js_template_text)
            for d in dicts:
                rendered_js = template.render(**d)
                head.add_child(Script(rendered_js))

        # 5. Attach explicit components
        for head_component in self.head_components:
            head.add_child(head_component)

        body = Body(style={'padding': '10px'})
        for body_component in self.body_components:
            body.add_child(body_component)

        document.add_child(head)
        document.add_child(body)

        return document

    def render(self):
        """
        Compiles the object tree and serializes it into an HTML string.

        :return: The complete HTML source code.
        """
        return self.compile().render()

    def render_to_file(self, filepath):
        """
        Compiles the HTML and writes it to the specified file path.

        :param filepath: The full destination path for the .html file.
        """
        with open(filepath,'w') as f:
            f.write(self.render())

    def render_to_jnb_iframe(self, width='100%', height='300px'):
        """
        Compiles the HTML and writes it to the specified file path.

        :param filepath: The full destination path for the .html file.
        """
        escaped_html = html.escape(self.render())
        return f'''
                <iframe 
                    srcdoc="{escaped_html}" 
                    style="width: {width}; height: {height}; border: 1px solid #ddd;" 
                    sandbox="allow-scripts allow-same-origin"
                ></iframe>
                '''
