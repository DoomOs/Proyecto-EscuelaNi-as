# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ClassManager'
copyright = '2024, Bryan Jancarlo Sosa Mejía'
author = 'Bryan Jancarlo Sosa Mejía'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    
    'myst_parser',
    'sphinx_copybutton',
    'sphinx.ext.autodoc',
    
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
import sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    'collapse_navigation': False,  # Establecer en False para mantener el índice abierto
    'display_version': True,  
}

#html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]


#html_theme = 'furo'
#html_static_path = ['_static']


import os
import sys
import django
sys.path.insert(0, os.path.abspath('../'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'escuela.settings'
django.setup()

# Configuración para Read the Docs
if os.environ.get('READTHEDOCS'):
    html_output = os.path.join(os.environ['READTHEDOCS_OUTPUT'], 'html')
    os.makedirs(html_output, exist_ok=True)
