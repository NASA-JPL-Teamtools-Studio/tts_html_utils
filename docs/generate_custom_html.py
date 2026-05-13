import datetime
import os
import textwrap
import shutil
import importlib
import pkgutil
import re
from pathlib import Path
import pandas as pd
from tts_data_utils.core.generic import GenericContainer

def generate_project_overview(app):
    """
    Fetches the README.md from the project root, strips out the 
    'About Teamtools Studio' section, and saves it as overview.md.
    """
    # Root README is one level above the docs folder
    readme_path = Path(app.srcdir).parent / "README.md"
    out_file = Path(app.srcdir) / "overview.md"

    if not readme_path.exists():
        print(f"Warning: Root README.md not found at {readme_path}")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to find and remove the 'About Teamtools Studio' section
    # Matches the header and everything until the next '##' header or end of file
    pattern = r"## About Teamtools Studio.*?(\n(?=## )|\Z)"
    cleaned_content = re.sub(pattern, "", content, flags=re.DOTALL)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(cleaned_content)

def generate_requirements_tbale(app):
    """
    Generates a requirements.rst file containing a custom HTML Power Table
    built from a CSV source.
    """
    out_file = os.path.join(app.srcdir, 'requirements.rst')
    in_file = os.path.join(app.srcdir, 'requirements.csv')
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    primary_fields = ['Level', 'ID', 'Name', 'V&V Method', 'Status']
    
    in_df = pd.read_csv(in_file).fillna(' ')
    secondary_fields = [x for x in in_df.columns if x not in primary_fields]
    primary_data = in_df[primary_fields]
    
    subcontainers = []
    for _, row in in_df[secondary_fields].iterrows():
        rows = [{'': c,' ': row[c]} for c in secondary_fields]
        subcontainers.append({'': GenericContainer(raw_data = rows)})
    
    # Generate HTML markup via GenericContainer
    html_markup = GenericContainer(
            raw_data=primary_data.to_dict('records'),
            subcontainers=subcontainers
        ).power_table(
            add_filters='local', 
            add_sorting='local',
            stylesheets=[Path(app.srcdir) / '_static/requirements_table.css']
    ).render(include_js=True, include_css=True)


    # Indent for RST raw directive
    indented_html = textwrap.indent(html_markup, '    ')

    content = f"""
Requirements
=================

This page was generated automatically during the Sphinx build process.

**Build Timestamp:** {now}

.. raw:: html

{indented_html}
"""
    with open(out_file, 'w', encoding="utf-8") as f:
        f.write(content)

def generate_api_docs(app):
    """
    Inspects the library and generates a nested directory structure.
    If a README.md exists in a package directory, it is injected into 
    the top of that package's documentation page.
    """
    package_name = 'tts_html_utils' 
    api_root = Path(app.srcdir) / "api"
    
    # Clean old build to prevent orphan warnings
    if api_root.exists():
        shutil.rmtree(api_root)
    api_root.mkdir(parents=True, exist_ok=True)

    try:
        package = importlib.import_module(package_name)
        # Physical path to the source code to find package-specific READMEs
        pkg_src_path = Path(package.__file__).parent
    except ImportError:
        print(f"ERROR: Could not import {package_name}.")
        return

    # structure[parent_module] = [list of child links]
    structure = {}

    for _, modname, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        parts = modname.split('.')
        relative_parts = parts[1:] 
        
        if not relative_parts:
            parent_key = ""
            current_file_base = parts[0]
        else:
            parent_key = ".".join(parts[:-1])
            current_file_base = relative_parts[-1]

        parent_path = api_root.joinpath(*relative_parts[:-1])
        parent_path.mkdir(parents=True, exist_ok=True)
        
        readme_include = ""
        if ispkg:
            # Package logic: Create folder and index.rst
            target_dir = parent_path / current_file_base
            target_dir.mkdir(exist_ok=True)
            filepath = target_dir / "index.rst"
            ref_name = f"{modname} (Package)"
            link = f"{current_file_base}/index"
            
            # Check for README.md in source directory
            sub_pkg_src = pkg_src_path.joinpath(*relative_parts)
            readme_path = sub_pkg_src / "README.md"

            if readme_path.exists():
                # Calculate the relative path from the .rst file to the actual README.md
                rel_readme = os.path.relpath(readme_path, filepath.parent)
                readme_include = (
                    f".. include:: {rel_readme}\n"
                    f"    :parser: myst_parser.sphinx_\n\n"
                )
        else:
            # Module logic: Create .rst file
            filepath = parent_path / f"{current_file_base}.rst"
            ref_name = modname
            link = current_file_base

        # Track for parent toctree
        if parent_key not in structure:
            structure[parent_key] = []
        structure[parent_key].append(link)

        # Write content
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"{ref_name}\n")
            f.write("=" * len(ref_name) + "\n\n")
            
            if readme_include:
                f.write(readme_include)
                f.write("Technical Reference\n")
                f.write("-------------------\n\n")

            f.write(f".. automodule:: {modname}\n")
            f.write("    :members:\n")
            f.write("    :undoc-members:\n")
            f.write("    :show-inheritance:\n\n")
            
            if ispkg:
                f.write(f".. toctree::\n")
                f.write(f"    :maxdepth: 2\n\n")

    # Second pass: Build the hierarchy via index.rst files
    for parent_mod, children in structure.items():
        if parent_mod == package_name:
            target_index = api_root / "index.rst"
            title = f"{package_name} API"
        elif not parent_mod:
            continue
        else:
            parts = parent_mod.split('.')
            target_index = api_root.joinpath(*parts[1:]) / "index.rst"
            title = parent_mod

        if not target_index.exists():
            with open(target_index, "w", encoding="utf-8") as f:
                f.write(f"{title}\n")
                f.write("=" * len(title) + "\n\n")
                f.write(f".. toctree::\n")
                f.write(f"    :maxdepth: 2\n\n")

        with open(target_index, "a", encoding="utf-8") as f:
            for child in sorted(children):
                f.write(f"    {child}\n")

    # Create the Top-level connector file
    with open(Path(app.srcdir) / "api_reference.rst", "w", encoding="utf-8") as f:
        f.write("API Reference\n")
        f.write("=============\n\n")
        f.write(".. toctree::\n")
        f.write("    :maxdepth: 2\n\n")
        f.write("    api/index\n")

def setup(app):
    """
    Sphinx extension entry point.
    """
    app.connect('builder-inited', generate_project_overview)
    app.connect('builder-inited', generate_requirements_tbale)
    app.connect('builder-inited', generate_api_docs)