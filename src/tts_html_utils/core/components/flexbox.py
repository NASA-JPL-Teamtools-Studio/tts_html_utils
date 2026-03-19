#Standard Library Imports
import pdb

#Installed dependency imports
#None yet

#Teamtools Studio Imports
from tts_utilities.logger import create_logger

#This Library Imports
from tts_html_utils.core.components.base import HtmlComponentSimple
from tts_html_utils.core.components.misc import Div

logger = create_logger(name='tts_html_utils.core.components.flexbox')

class FlexContainer(HtmlComponentSimple):
    """
    A flexible container that uses CSS Flexbox for layout.
    
    **Concept:**
    The FlexContainer is a div with display:flex that allows for easy
    arrangement of child elements in rows or columns with precise control
    over sizing and spacing.
    
    :param children: Child components to be arranged in the flex container.
    :type children: list or single HtmlComponent
    :param direction: The flex-direction property. Options: 'row', 'column', 'row-reverse', 'column-reverse'.
    :type direction: str, optional
    :param justify: The justify-content property. Options: 'flex-start', 'flex-end', 'center', 'space-between', 'space-around', 'space-evenly'.
    :type justify: str, optional
    :param align: The align-items property. Options: 'flex-start', 'flex-end', 'center', 'stretch', 'baseline'.
    :type align: str, optional
    :param wrap: The flex-wrap property. Options: 'nowrap', 'wrap', 'wrap-reverse'.
    :type wrap: str, optional
    :param gap: The gap between flex items (e.g., '5px', '1rem').
    :type gap: str, optional
    :param kwargs: Additional keyword arguments passed to the parent Div.
    """
    TAG = 'div'
    
    def __init__(self, children=None, direction='row', justify='flex-start', 
                 align='stretch', wrap='nowrap', gap=None, **kwargs):
        # Build the style dictionary for flexbox
        style = kwargs.get('style', {})
        style.update({
            'display': 'flex',
            'flex-direction': direction,
            'justify-content': justify,
            'align-items': align,
            'flex-wrap': wrap
        })
        
        # Add gap if specified
        if gap:
            style['gap'] = gap
            
        kwargs['style'] = style
        super().__init__(children=children, **kwargs)


class FlexItem(HtmlComponentSimple):
    """
    A flex item that can be placed inside a FlexContainer.
    
    **Concept:**
    FlexItems are divs with flex properties that control how they grow, shrink,
    and what their base size is within a FlexContainer.
    
    :param children: Child components inside this flex item.
    :type children: list or single HtmlComponent
    :param width: The width of the item (e.g., '50%', '200px', 'auto').
    :type width: str, optional
    :param height: The height of the item (e.g., '100px', 'auto').
    :type height: str, optional
    :param grow: The flex-grow property (how much the item can grow). Default is 0 (no growing).
    :type grow: int, optional
    :param shrink: The flex-shrink property (how much the item can shrink). Default is 1 (can shrink).
    :type shrink: int, optional
    :param basis: The flex-basis property (base size before growing/shrinking). Default is 'auto'.
    :type basis: str, optional
    :param align_self: Override the container's align-items for this specific item.
    :type align_self: str, optional
    :param kwargs: Additional keyword arguments passed to the parent Div.
    """
    TAG = 'div'
    
    def __init__(self, children=None, width=None, height=None, grow=None, 
                 shrink=None, basis=None, align_self=None, **kwargs):
        # Build the style dictionary for the flex item
        style = kwargs.get('style', {})
        
        # Add width and height if specified
        if width:
            style['width'] = width
        if height:
            style['height'] = height
            
        # Add flex properties if specified
        if grow is not None or shrink is not None or basis is not None:
            flex_parts = []
            flex_parts.append(str(grow) if grow is not None else '0')
            flex_parts.append(str(shrink) if shrink is not None else '1')
            flex_parts.append(basis if basis is not None else 'auto')
            style['flex'] = ' '.join(flex_parts)
        
        # Add align-self if specified
        if align_self:
            style['align-self'] = align_self
            
        kwargs['style'] = style
        super().__init__(children=children, **kwargs)


class FlexRow(FlexContainer):
    """
    A convenience class for a horizontal flex container.
    
    This is a FlexContainer with direction='row' preset.
    """
    def __init__(self, children=None, **kwargs):
        kwargs['direction'] = 'row'
        super().__init__(children=children, **kwargs)


class FlexColumn(FlexContainer):
    """
    A convenience class for a vertical flex container.
    
    This is a FlexContainer with direction='column' preset.
    """
    def __init__(self, children=None, **kwargs):
        kwargs['direction'] = 'column'
        super().__init__(children=children, **kwargs)
