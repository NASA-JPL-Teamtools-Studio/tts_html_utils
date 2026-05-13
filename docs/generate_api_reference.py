import inspect
import importlib
import pkgutil
from pathlib import Path

def generate_api_docs(app):
    # Change 'tts_html_utils' to the actual name of your package folder
    package_name = 'tts_html_utils' 
    api_dir = Path(app.srcdir) / "api"
    api_dir.mkdir(exist_ok=True)

    # 1. Start the main API Reference file
    api_ref_content = [
        "API Reference",
        "=============",
        "",
        ".. toctree::",
        "   :maxdepth: 2",
        ""
    ]

    try:
        package = importlib.import_module(package_name)
    except ImportError:
        print(f"Could not import {package_name}. Ensure it is in your sys.path.")
        return

    # 2. Walk through all submodules in your package
    for _, modname, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        # Create a filename for the module (e.g., api/tts_html_utils.core.rst)
        short_name = modname.split(".")[-1]
        mod_file = api_dir / f"{modname}.rst"
        
        # Add to our main toctree
        api_ref_content.append(f"   {modname}")

        # Create the individual module page
        with open(mod_file, "w") as f:
            f.write(f"{modname}\n")
            f.write("=" * len(modname) + "\n\n")
            f.write(f".. automodule:: {modname}\n")
            f.write("   :members:\n")
            f.write("   :undoc-members:\n")
            f.write("   :show-inheritance:\n")

    # 3. Write the index file (api_reference.rst)
    with open(Path(app.srcdir) / "api_reference.rst", "w") as f:
        f.write("\n".join(api_ref_content))

def setup(app):
    app.connect('builder-inited', generate_requirements_tbale)
    app.connect('builder-inited', generate_api_docs) # Register the new function