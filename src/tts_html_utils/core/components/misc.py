#Standard Library Imports
import pdb

#Installed dependency imports
#None yet

#Teamtools Studio Imports
from tts_utilities.logger import create_logger

#This Library Imports
from tts_html_utils.core.components.base import HtmlComponentSimple, HtmlComponentSingleSimple
from tts_html_utils.core.components.favicon import favicon_data

logger = create_logger(name='html_utils.core.components.base')

class HTML(HtmlComponentSimple):
    """
    The root container for the entire document.

    **Concept:**
    This is the outermost shell of a webpage. Every other element (Head, Body, etc.) 
    lives inside this tag.

    **Usage Note:**
    You rarely need to instantiate this yourself. The `HtmlCompiler` typically 
    creates this automatically when you build a page.
    """
    TAG = 'html'

class Head(HtmlComponentSimple):
    """
    The "Settings" section of the document.

    **Concept:**
    The `<head>` contains metadata—information *about* the page rather than content 
    *on* the page. It holds the title, CSS links, scripts, and browser instructions.
    Nothing put here is displayed in the main browser window.

    **Usage Note:**
    Like `HTML`, this is usually managed automatically by the `HtmlCompiler`.
    """
    TAG = 'head'

class Body(HtmlComponentSimple):
    """
    The "Canvas" of the document.

    **Concept:**
    The `<body>` contains everything the user actually sees: text, images, buttons, 
    and tables. If you are building a component to display data, it eventually 
    lives inside here.

    **Usage Note:**
    Managed automatically by the `HtmlCompiler`. You typically just add children 
    to the compiler, and it places them in the Body for you.
    """
    TAG = 'body'

class Header(HtmlComponentSimple):
    """
    A semantic container for introductory content.

    **Concept:**
    Not to be confused with `<head>`. The `<header>` is a visible section of the page, 
    usually containing the logo, navigation bar, and page title. It helps screen readers 
    and search engines understand the structure of your content.
    """
    TAG = 'header'

class Footer(HtmlComponentSimple):
    """
    A semantic container for the bottom of a page or section.

    **Concept:**
    Usually contains copyright notices, contact info, or links to privacy policies. 
    Like `<header>`, this is a "semantic" tag—it behaves exactly like a `Div` 
    visually, but it tells search engines "this is the end of the content."
    """
    TAG = 'footer'

class Style(HtmlComponentSimple):
    """
    A container for raw CSS code.

    **Concept:**
    Allows you to write CSS rules directly within the HTML file rather than linking 
    to an external `.css` file.
    
    **Usage Note:**
    The `HtmlCompiler` uses this to inject CSS dependencies. You generally shouldn't 
    need to use this manually; prefer creating `.css` files and linking them.
    """
    TAG = 'style'

class Script(HtmlComponentSimple):
    """
    A container for raw JavaScript code.

    **Concept:**
    Allows you to write JavaScript logic directly within the HTML file. 

    **Usage Note:**
    The `HtmlCompiler` uses this to inject JS dependencies. For complex logic, 
    prefer creating `.js` files and letting the compiler link them.
    """
    TAG = 'script'

class Title(HtmlComponentSimple):
    """
    The browser tab name.

    **Concept:**
    Defines the text that appears in the browser tab, bookmarks, and search engine results. 
    It does not appear in the page content itself.
    """
    TAG = 'title'

class Div(HtmlComponentSimple):
    """
    The generic "Lego Brick" of the web.

    **Concept:**
    The `<div>` (Division) is a generic container used to group other elements together 
    for styling or layout purposes. It has no semantic meaning (unlike `<header>` or `<footer>`).
    
    Most modern web layouts are essentially nested structures of Divs.
    """
    TAG = 'div'

class TtsFavicon(Script):
    """
    Injects the Teamtools Studio logo into the browser tab.

    **How it works:**
    Instead of requiring you to manage a physical `.ico` or `.png` file on the server, 
    this class contains the base64-encoded image data of the logo. It uses a small 
    JavaScript snippet to create the link tag dynamically and attach it to the document head.
    """
    def __init__(self):
        super().__init__()
        self.js_includes = [('\n'.join([
                      "const favicon = document.createElement('link');",
                      "favicon.rel = 'icon';",
                      "favicon.type = 'image/png';",
                      f"favicon.href = '{favicon_data}';",
                      "document.head.appendChild(favicon);",
                    ]), {})]


class HorizontalBreak(HtmlComponentSingleSimple):
    """
    A thematic break (Horizontal Rule).

    **Concept:**
    Renders a horizontal line across the container. Used to visually separate 
    different topics or sections of content.

    **Alias:** `HR`
    """

    TAG = 'hr'
    DEFAULT_CLASS=['faded']

HR = HorizontalBreak

class LineBreak(HtmlComponentSingleSimple):
    """
    A forced line break.

    **Concept:**
    Forces the text following it to start on a new line. 
    
    **Usage Note:**
    Use sparingly. For spacing between paragraphs, it is usually better to use 
    CSS margins or separate `<p>` (Paragraph) tags rather than multiple `<br>` tags.

    **Alias:** `BR`
    """
    TAG = 'br'

BR = LineBreak

class Link(HtmlComponentSimple):
    """
    A hyperlink (Anchor tag).

    **Concept:**
    The fundamental connector of the web. Links one page (or section) to another.

    **Alias:** `A`

    :param text: The clickable text the user sees.
    :type text: str
    :param href: The destination URL. If None, defaults to the `text` (useful if pasting raw URLs).
    :type href: str, optional
    :param new_tab: If True, clicking the link opens a new browser tab (`target="_blank"`). 
                    If False, it navigates the current tab. Defaults to True.
    :type new_tab: bool, optional
    :param kwargs: Additional keyword arguments passed to the `HtmlComponent` constructor.
    """

    TAG='a'
    def __init__(self, text, href=None, new_tab=True, **kwargs):
        if href is None: href = text
        attr = {'href': href, 'target': '_blank' if new_tab else '_self'}
        if 'attr' in kwargs.keys():
            attr = {**attr, **kwargs['attr']}
            del kwargs['attr']
        super().__init__(children=text, attr=attr, **kwargs)

A = Link

class Button(HtmlComponentSimple):
    """
    A clickable button element.

    **Concept:**
    Used for actions (like "Submit", "Calculate", "Toggle"), as opposed to Links 
    which are used for navigation.

    :param text: The label displayed on the button.
    :type text: str
    :param button_type: The HTML behavior type. 
                        - 'button': A generic clickable button (requires JS to do anything).
                        - 'submit': Submits a parent form.
                        - 'reset': Resets a parent form.
    :type button_type: str, optional
    :param kwargs: Additional keyword arguments passed to the `HtmlComponent` constructor.
    """

    TAG='button'
    def __init__(self, text, button_type='button', **kwargs):
        attr = {'type': button_type}
        if 'attr' in kwargs.keys():
            attr = {**attr, **kwargs['attr']}
            del kwargs['attr']
        super().__init__(children=text, attr=attr, **kwargs)