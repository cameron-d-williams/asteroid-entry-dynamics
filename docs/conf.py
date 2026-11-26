"""Configure Sphinx for the Asteroid Entry Dynamics documentation."""

from importlib.metadata import version as package_version

# Project information.
project = "Asteroid Entry Dynamics"
author = "Cameron Williams"
copyright = f"2026, {author}"
release = package_version("asteroid-entry-dynamics")
language = "en"

# Sphinx extensions.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "numpydoc",
]

# Source configuration.
root_doc = "index"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# API documentation.
autosummary_generate = True
autoclass_content = "class"
autodoc_typehints = "signature"
autodoc_member_order = "bysource"

# NumPy docstring configuration.
numpydoc_show_class_members = False

numpydoc_validation_checks = {
    "all",
    "EX01",
    "SA01",
    "ES01",
}

# External documentation cross-references.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
}

# Unresolved external NumPy type annotation references.
nitpick_ignore = {
    ("py:class", "numpy._typing._array_like.NDArray"),
    ("py:class", "numpy.float64"),
}

# HTML output.
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_title = project

html_theme_options = {
    "show_nav_level": 2,
    "show_toc_level": 2,
    "navigation_depth": 4,
}
