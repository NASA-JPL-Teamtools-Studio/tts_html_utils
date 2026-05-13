# The tts_html_utils `core` package

The core package is where most of the pythonic functionality of tts_html_utils lives. It has 3 main components:

1. `components`: A subpackage with class definitions for all common HTML tags adn the fundamental rendering logic in components.base.
2. `compiler`: The compiler is the orchestrator of the library. It takes a hierarchy of nested python objects and renders them into a single file suitable for emailing or attaching to a report. The compiler traverses an entire tree of `HtmlComponent`s, capturing any required JS or CSS for each, deduplicating those resources and placing them all in <head> instead of being strewn throughout the library.
3. `palette`: Palette is a place to define shared color sets and label them with operator-friendly names. This maps a concept like EvrPalette['warning_lo'] to the CSS snippet needed to colorize HTML in the way that users expect (in this case, coloring a yellow background with black text). This is meant to be extensible to any mission allowing lead developers to set standards for style across all subsystems using Teamtools Studio products.