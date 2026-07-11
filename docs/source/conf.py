import os
import sys

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Coding Assingnment for Programming with Python'
copyright = '2026, Florian Krauß'
author = 'Florian Krauß'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration



sys.path.insert(0, os.path.abspath("../.."))

templates_path = ['_templates']
exclude_patterns = []
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
