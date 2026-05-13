# The tts_html_utils `core.components` package

This package is somewhat self explanatory. `base.py` provides an abstract base class that handles all of the logic for combining HTML elements into hierarchical trees and rendering each element into a string that can be understood by a web browser. It also allows developers to contribute snippets of JavaScript or CSS for limited interactive functionality. Developers should take care to use UUIDs liberally when writing new JS functionality so multiple copies of an element on the same page will not trigger each other.

All other components are extensions of the HtmlComponent abstract base class.

The rest of the package is fairly self explanatory to developers with modest web development experience. If you don't understand them immediately that's OK, but you should probably do some training on a place like W3 Schools or even just asking an LLM what's going on here.