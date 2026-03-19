#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Debug script to print the exact HTML output of a PaneContainer
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tts_html_utils.core.components.structure import PaneContainer
from tts_html_utils.core.components.misc import Div

def main():
    """Print the exact HTML output of a PaneContainer"""
    pc = PaneContainer(id='pane-container-a')
    pc.add_pane("Content A", "My Tab")
    pc.add_pane("Content B", "Other Tab")
    
    html = pc.render()
    
    print("\nExact HTML output:")
    print("=================")
    print(html)
    print("\nHTML output with line breaks for readability:")
    print("===========================================")
    # Add line breaks for readability
    html_readable = html.replace("><", ">\n<")
    print(html_readable)

if __name__ == "__main__":
    main()
