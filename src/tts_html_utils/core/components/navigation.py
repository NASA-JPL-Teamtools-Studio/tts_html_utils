#Standard Library Imports
from pathlib import Path
import pdb

#Installed dependency imports
#None yet

#Teamtools Studio Imports
from tts_utilities.logger import create_logger

#This Library Imports
from tts_html_utils.core.components.list import PowerList, ListItem
from tts_html_utils.core.components.misc import Link

logger = create_logger(name='html_utils.core.components.base')


class Navbar(PowerList):
    """
    Simple class to streamline creation of a navbar, which is essentially an unordered list
    of links.

    Nothing special now, but eventually this will be part of stock templates and will include out of the box CSS

    :param mapping: Dictionary where keys are labels and values are URLs
    :type style: dict

    :param new_tab: Should links open to a new tab or in the current one?
    :type new_tab: bool

    :param kwargs: Additional keyword arguments passed to the `HtmlComponent` constructor.
    """
    def __init__(self, mapping, new_tab=False, **kwargs):
        super().__init__(class_name='navbar', **kwargs)
        self.add_items(mapping, new_tab=new_tab)
        self.css_includes = [(Path(__file__).parent.parent.parent.joinpath('resources/css/navbar.css'),{})]

    def add_items(self, mapping, new_tab=False):
        """
        Add an item to an existing Navbar. This is equivalent to including the item in the mapping parameter of __init__()

        :param mapping: Dictionary where keys are labels and values are URLs
        :type style: dict

        :param new_tab: Should links open to a new tab or in the current one?
        :type new_tab: bool
        """
        for label, href in mapping.items():
            if isinstance(href, dict):
                self.up_level(label=label)
                self.add_items(href)
                self.down_level()
            else:
                self.line(Link(label, href=href, new_tab=new_tab), class_name='navbartab')

