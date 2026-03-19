#Standard Library Imports
import pdb

#Installed dependency imports
#None yet

#Teamtools Studio Imports
from tts_utilities.logger import create_logger

#This Library Imports
from tts_html_utils.core.components.base import HtmlComponent, HtmlComponentSimple

logger = create_logger(name='html_utils.core.components.base')

class UnorderedList(HtmlComponentSimple):
    """
    A standard bulleted list (<ul>).
    
    **Concept:**
    Used for items where the order does not matter. Browsers typically 
    render these with bullet points. This is also a common structural
    element that is used without looking like a literal list.

    **Alias:** `UL`
    """
    TAG = 'ul'

UL = UnorderedList

class OrderedList(HtmlComponentSimple):
    """
    A numbered list (<ol>).

    **Concept:**
    Used for items where the sequence is important. Browsers typically render 
    these with numbers (1, 2, 3...) or letters (a, b, c...). Much less common
    than an unordered list.


    **Alias:** `OL`
    """
    TAG = 'ol'
OL = OrderedList

class ListItem(HtmlComponentSimple):
    """
    A single row within a list (<li>).

    **Concept:**
    Neither `<ul>` nor `<ol>` can directly contain text. They can only contain `<li>` tags.
    This component wraps the actual content of the list entry.

    **Alias:** `LI`
    """
    TAG = 'li'
LI = ListItem

class PowerList(HtmlComponent):
    """
    A smart builder for creating complex, nested lists without the headache.

    **The Problem:**
    Creating nested HTML lists is very repetative. You have to remember to open a `<ul>`, 
    add an `<li>`, open a new `<ul>` *inside* that `<li>` for the sub-items, and then 
    close everything in the exact reverse order.

    **The Solution:**
    `PowerList` works like a text editor's outline mode. You simply add a line, and 
    command it to "indent" (`up_level`) or "outdent" (`down_level`). It tracks 
    where you are in the hierarchy and handles all the tag nesting for you automatically.

    :param children: Initial list items to populate. (Usually better to use `.line()` after init).
    :type children: List, optional
    :param class_name: CSS classes for the root list element.
    :type class_name: str or list of str, optional
    :param extra_class_name: Additional CSS classes to append.
    :type extra_class_name: str or list of str, optional
    :param style: Inline CSS styles for the root list element.
    :type style: dict, optional
    :param ordered: If True, renders as a numbered list (`<ol>`). If False, renders as bullets (`<ul>`). Defaults to False.
    :type ordered: bool
    """
    def __init__(self, children=None, class_name=None, extra_class_name=None, style=None, ordered=False):
        super().__init__(children=children, class_name=class_name, extra_class_name=extra_class_name, style=style)
        self.ordered = ordered

        # 'target' acts as a cursor. It points to the specific list (root or nested)
        # where the next item should be added.
        self.target = [self]

    def line(self, line, class_name=None, extra_class_name=None, style=None):
        """
        Appends a new item to the current level of the list.

        :param line: The content of the item (text or another HtmlComponent).
        :type line: str or HtmlComponent
        :param class_name: CSS classes for this specific list item (`<li>`).
        :type class_name: str or list of str, optional
        :param extra_class_name: Additional CSS classes to append.
        :type extra_class_name: str or list of str, optional
        :param style: Inline CSS styles for this specific list item.
        :type style: dict, optional
        """
        if not isinstance(line, ListItem):
            line = ListItem(children=line, class_name=class_name, extra_class_name=extra_class_name, style=style)

        self.target[-1].add_child(line)


    def up_level(self, label=None, new_list=None, class_name=None, extra_class_name=None, style=None, ordered=None):
        """
        Indents the list (creates a sub-list).

        **How it works:**
        This creates a new list (container) and nests it inside the *last item* you added.
        The internal "cursor" moves to this new list, so subsequent `.line()` calls 
        will appear as sub-items.

        :param label: Optional text to place on the parent item *before* the sub-list starts.
        :type label: str or HtmlComponent, optional
        :param new_list: If you have already built a `UL` or `OL` object, you can pass it here to insert it.
        :type new_list: UL or OL, optional
        :param class_name: CSS classes for the new sub-list container.
        :type class_name: str or list of str, optional
        :param extra_class_name: Additional CSS classes to append.
        :type extra_class_name: str or list of str, optional
        :param style: Inline CSS styles for the new sub-list container.
        :type style: dict, optional
        :param ordered: If True, the sub-list will be numbered. If False, bulleted. Defaults to the parent list's type.
        :type ordered: bool, optional
        """

        if not new_list:
            if ordered is None:
                ordered = self.ordered
            
            # FIX: Pass the styling arguments to the new PowerList
            new_list = PowerList(
                ordered=ordered, 
                class_name=class_name, 
                extra_class_name=extra_class_name, 
                style=style
            )

        if label is not None: 
            self.target[-1].add_child(ListItem(children=[label, new_list]))
        else:
            self.target[-1].add_child(ListItem(children=new_list))
        self.target.append(new_list)

    def down_level(self):
        """
        Outdents the list (returns to the parent level).

        **How it works:**
        Moves the internal "cursor" back up to the parent list.
        """
        if len(self.target) <= 1:
            return # Do nothing if we're at the root level already
        self.target.pop()

    def render(self):
        """
        Converts the internal PowerList structure into standard HTML components
        (`UL`/`OL` and `LI`) and renders them to a string.
        """
        top_list = OrderedList if self.ordered else UnorderedList
        return top_list(children=self.children, class_name=self.class_name, style=self.style).rendered