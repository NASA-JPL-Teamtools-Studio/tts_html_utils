#Standard Library Imports
from abc import ABC, abstractmethod
from uuid import uuid4
import pdb

#Installed Dependecy Imports
#none yet

#Teamtools Studio Imports
from tts_utilities.util import as_list
from tts_utilities.logger import create_logger
from bs4 import BeautifulSoup

#This Library Imports
# None

logger = create_logger(name='html_utils.core.components.base')

#================================================
# :: Base Component
#================================================
class HtmlComponent(ABC):
    """
    The fundamental blueprint for all HTML elements in this library.

    **The Concept:**
    HTML is hierarchical (a tree). A `<div>` contains a `<table>`, which contains 
    `<tr>` rows, which contain `<td>` cells. This class provides the machinery 
    to replicate that structure in Python.

    **How it works:**
    Every specific HTML tag (like `Div`, `Span`, or `Img`) inherits from this class.
    This base class handles the logic shared by *all* of them, such as:
    1. **Parent/Child Relationships:** Tracking what is inside what.
    2. **Attribute Management:** Handling IDs, CSS classes, and inline styles.
    3. **Dependency bubbling:** If a button deep inside a table requires a specific 
       JavaScript file, this class allows that requirement to bubble up to the 
       top of the document so the `HtmlCompiler` can see it.

    **Note:** This is an "Abstract Base Class" (ABC). You cannot create a generic `HtmlComponent` 
    directly. You must use one of its subclasses that represents a real HTML tag.

    :param children: Any nested components that go *inside* this element.
    :type children: List of HtmlComponent objects (or plain strings), optional
    :param class_name: Primary CSS class(es) to control the look/feel.
    :type class_name: str or list of str, optional
    :param extra_class_name: Additional CSS classes to append. Useful when extending components 
                             where you want to keep the base class but add a modifier.
    :type extra_class_name: str or list of str, optional
    :param tag: The actual HTML tag name (e.g., 'div', 'a', 'span'). Defaults to the class's `TAG` constant.
    :type tag: str, optional
    :param id: The unique HTML `id` attribute for this element.
    :type id: str, optional
    :param style: Inline CSS styles (e.g., `{'color': 'red', 'margin': '10px'}`).
    :type style: dict, optional
    :param attr: A dictionary of any other HTML attributes not covered above (e.g., `{'href': '...', 'onclick': '...'}`).
    :type attr: dict, optional
    """
    TAG = None
    DEFAULT_CLASS = []
    STYLESHEETS = []

    def __init__(self, children=None, class_name=None, extra_class_name=None, tag=None, id=None, style=None, attr=None):
        self.id = id
        self.tag = tag or self.TAG
        self.parent_id = None
        self.children = []
        self.js_includes = []
        self.css_includes = []
        self.attr = attr if attr is not None else {}

        for child in as_list(children or []):
            self.add_child(child)

        self._class = [] + as_list(class_name or self.DEFAULT_CLASS)
        if extra_class_name is not None:
            self._class += as_list(extra_class_name)

        self.style = style or {}

    def aggregate_attributes(self, attr, lst=None):
        """
        The "Harvester" method.

        This function recursively dives down into every child (and grandchild) 
        of this component to find specific attributes (usually 'js_includes' or 
        'css_includes').

        **Why?** When you render a full page, the top-level document needs to know about 
        every JavaScript file required by every tiny widget deep in the page structure.
        This method bubbles those requirements up to the surface.

        :param attr: The name of the attribute to collect (e.g., `'js_includes'`).
        :type attr: str
        :param lst: The accumulator list. If None, a new list is created.
        :type lst: list, optional
        :return: A list containing the collected attributes from this component and all descendents.
        """
        if lst is None: lst = []
        v = getattr(self, attr, None)
        if v is not None: lst += v #support elements without the given attr set
        for child in self.children:
            if not isinstance(child, HtmlComponent): continue
            try:
                child.aggregate_attributes(attr, lst=lst)
            except:
                pdb.set_trace()
        return lst

    def add_child(self, child):
        """
        Nests a new element inside this one.

        :param child: The component to insert.
        :type child: HtmlComponent or str
        """
        self.children.append(child)
        if isinstance(child, HtmlComponent):
            child.parent_id = self.id

    @property
    def class_name(self):
        """
        Returns the final, space-separated string of CSS classes.

        This combines the default classes (from `DEFAULT_CLASS`) with any specific 
        classes added during initialization or via `add_class`. This string is 
        what actually gets written to the HTML `class="..."` attribute.
        """
        return " ".join(self._class)

    def add_class(self, new_class):
        """
        Appends a new CSS class to the existing list of classes.
        Useful for dynamically highlighting an element (e.g., adding 'active' or 'error').

        :param new_class: The CSS class string to add.
        :type new_class: str
        """
        if new_class not in self._class:
            self._class.append(new_class)

    @property
    def rendered(self):
        """
        A convenience property that triggers the full rendering process.
        Accessing `.rendered` is equivalent to calling the `.render()` method.

        :return: The fully compiled HTML string for this component.
        :rtype: str
        """
        return self.render()

    @abstractmethod
    def render(self):
        """
        This method transforms the abstract Python object into an actual HTML string.
        Since this is the base class, it doesn't know *how* to render itself yet. 
        Specific implementations (like `HtmlComponentSimple`) provide the logic here.
        """
        pass

    @property
    def content(self):
        """
        A convenience property that returns the *inner* HTML of the component.
        
        Example: If the component is `<div><b>Hello</b></div>`, `.content` returns `<b>Hello</b>`.
        """
        return self.render_content()

    def render_content(self):
        """
        A hook for how an individual component should render its content as a string.
        Most compoenents inherit from HtmlComponentSimple, which inherits from this. 
        HtmlComponentSimple defines render_content itself, but it can always be
        overridden by a descendent class.
        """
        raise NotImplementedError(f'This class does not implement content rendering')

    def recurse_stylesheets(self):
        """
        Crawls the component tree to find all stylesheets declared by children.

        Similar to `aggregate_attributes`, this ensures that if a nested component 
        defines a custom `STYLESHEET`, that sheet is bubbled up and included in the 
        document head.
        """
        child_sheets = self.STYLESHEETS
        for child in self.children:
            if isinstance(child, HtmlComponent):
                child_sheets += child.recurse_stylesheets()
        return child_sheets

    def pretty_print(self):
        """
        A debugging tool that prints the HTML in a readable, indented format.
        
        Raw HTML strings are often one massive, unreadable line. This uses 
        BeautifulSoup to break it into indented lines so you can see the structure 
        visually.
        """
        html = self.render()
        soup = BeautifulSoup(html, 'html.parser')
        return soup.prettify()


class HtmlComponentSimple(HtmlComponent):
    """
    The implementation for standard "Container" HTML tags.

    **Concept:**
    Most HTML tags work like containers: they open, they hold content, and they close.
    Examples: `<div>...</div>`, `<p>...</p>`, `<b>...</b>`.
    
    This class implements the `render` logic for this open-close pattern.
    """

    def _render_open(self):
        """
        Internal helper: specific logic to build the *opening* tag.

        It takes the Python dictionaries for style/attributes and converts them 
        into string format.
        """
        # 1. Start with the tag itself
        parts = [self.tag]

        # 2. Add ID if present
        if self.id:
            parts.append(f'id="{self.id}"')

        # 3. Add Class if present
        if self.class_name:
            parts.append(f'class="{self.class_name}"')

        # 4. Add Style if present
        if self.style:
            style_str = ' '.join(f'{k}: {v};' for k, v in self.style.items())
            parts.append(f'style="{style_str}"')

        # 5. Add other attributes if present
        if self.attr:
            attr_str = ' '.join(f'{k}="{v}"' for k, v in self.attr.items())
            parts.append(attr_str)

        # 6. Join with spaces and wrap in brackets
        # ' '.join(parts) ensures there is exactly one space between attributes
        # and no trailing space before the closing bracket.
        return f'<{" ".join(parts)}>'

    def render(self):
        """
        Generates the full HTML string for this element and all its children.

        Structure: `<tag> [All Children Rendered Here] </tag>`
        """
        return f'{self._render_open()}{self.content}</{self.tag}>'

    def render_content(self):
        """
        Iterates through the children list, asks them to render themselves, 
        and concatenates the results.
        """
        out = ''
        for child in self.children:
            if isinstance(child, HtmlComponent):
                out += child.rendered
            else:
                out += str(child)
        return out

class HtmlComponentSingleSimple(HtmlComponentSimple):
    """
    The implementation for "Void" or "Self-Closing" HTML tags.

    **Concept:**
    Some HTML tags do not contain other elements. They are standalone instructions.
    Examples: 
    - `<img>`: Just places an image.
    - `<br>`: Just creates a line break.
    - `<input>`: Just creates a text box.

    These tags **must not** have a closing tag (e.g., `</img>` is invalid HTML).
    This class overrides the render method to ensure we only print the opening tag.
    """
    def render(self):
        """
        Renders the tag without a closing partner or internal content.
        
        Structure: `<tag attribute="value">`
        """
        return self._render_open()

    def render_content(self):
        """
        Disabled for HtmlComponentSingleSimple, but still here in case it's called
        so it raises a useful exception.
        """
        raise NotImplementedError(f'No content allowed for Singleton HTML elements')