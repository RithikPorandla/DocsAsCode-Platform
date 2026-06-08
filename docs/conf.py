# Sphinx configuration - DocsAsCode

import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "DocsAsCode"
copyright = "2026, Rithik Porandla"
author = "Rithik Porandla"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "myst_parser",
    "sphinxcontrib.httpdomain",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

html_theme_options = {
    "logo_only": False,
    "navigation_depth": 4,
    "collapse_navigation": False,
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
