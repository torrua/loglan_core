# Configuration file for Sphinx

# -- Project information -----------------------------------------------------
project = "Loglan-Core"
copyright = "2024, torrua"
author = "torrua"
release = "0.5.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",  # Optional: to include source code in the documentation
]
html_theme = "sphinx_rtd_theme"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Autodoc configuration ---------------------------------------------------
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
