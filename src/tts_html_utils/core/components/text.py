#Standard Library Imports
import pdb

#Installed dependency imports
#None yet

#Teamtools Studio Imports
from tts_utilities.logger import create_logger

#This Library Imports
from tts_html_utils.core.components.base import HtmlComponentSimple

logger = create_logger(name='html_utils.core.components.base')

class Heading1(HtmlComponentSimple):
    """
    Heading 1 (<h1>). See HtmlComponentSimple and HtmlComponent for more information on 
    parameters. https://www.w3schools.com/tags/tag_hn.asp

    Also aliased in this libarary to H1
    """
    TAG = 'h1'

class Heading2(HtmlComponentSimple):
    """
    Heading 2 (<h2>). See HtmlComponentSimple and HtmlComponent for more information on 
    parameters. https://www.w3schools.com/tags/tag_hn.asp

    Also aliased in this library to H2
    """
    TAG = 'h2'

class Heading3(HtmlComponentSimple):
    """
    Heading 3 (<h3>). See HtmlComponentSimple and HtmlComponent for more information on 
    parameters. https://www.w3schools.com/tags/tag_hn.asp

    Also aliased in this library to H3
    """
    TAG = 'h3'

class Heading4(HtmlComponentSimple):
    """
    Heading 4 (<h4>). See HtmlComponentSimple and HtmlComponent for more information on 
    parameters. https://www.w3schools.com/tags/tag_hn.asp

    lso aliased in this library to H4
    """
    TAG = 'h4'


class Heading5(HtmlComponentSimple):
    """
    Heading 5 (<h5>). See HtmlComponentSimple and HtmlComponent for more information on 
    parameters. https://www.w3schools.com/tags/tag_hn.asp

    lso aliased in this library to H5
    """
    TAG = 'h5'


class Heading6(HtmlComponentSimple):
    """
    Heading 6 (<h6>). See HtmlComponentSimple and HtmlComponent for more information on 
    parameters. https://www.w3schools.com/tags/tag_hn.asp

    lso aliased in this library to H6
    """
    TAG = 'h6'

class Paragraph(HtmlComponentSimple):
    """
    Paragraph (<p>). See HtmlComponentSimple and HtmlComponent for more information on 
    parameters. https://www.w3schools.com/tags/tag_p.asp
    """
    TAG = 'p'

class Span(HtmlComponentSimple):
    """
    Span (<span>). See HtmlComponentSimple and HtmlComponent for more information on 
    parameters. https://www.w3schools.com/tags/tag_span.asp
    """
    TAG = 'span'

class Strong(HtmlComponentSimple):
    """
    String (<strong>). See HtmlComponentSimple and HtmlComponent for more information on 
    parameters. https://www.w3schools.com/tags/tag_strong.asp
    """
    TAG = 'strong'

class Pre(HtmlComponentSimple):
    """
    Preformatted (<pre>). See HtmlComponentSimple and HtmlComponent for more information on 
    parameters. https://www.w3schools.com/tags/tag_pre.asp
    """
    TAG = 'pre'

H1 = Heading1
H2 = Heading2
H3 = Heading3
H4 = Heading4
H5 = Heading5
H6 = Heading6
P = Paragraph