import os
import sys
from datetime import datetime
from blaise import __version__ as release

# Add the project root to sys.path so autodoc can import it
#sys.path.insert(0, os.path.abspath('../src'))

project = 'blaise'
author = 'Tom Flannaghan'
copyright = f'{datetime.now():%Y}, {author}'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',   # for Google/NumPy style docstrings
    'sphinx.ext.autosummary',
]

autosummary_generate = True
templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']