iu-project Documentation
========================

Project Overview
----------------

``iu-project`` is a Python command-line application for working with CSV input
data, storing processed information in an SQL database, and creating visual
outputs from plotted functions.

Project Structure
-----------------

.. code-block:: text

   iu-project/
   ├── custom_exceptions/   Own exception modules.
   ├── input/               Given CSV input files.
   ├── database/            SQL database storage.
   ├── docs/                Documentation files.
   ├── src/                 Source modules.
   ├── tests/               Unit tests.
   ├── visualization/       Image files of plotted functions.
   └── main.py              Program entry point.

Main Components
---------------

``custom_exceptions/``
   Contains project-specific exception classes, for example validation errors
   for invalid user input.

``input/``
   Contains CSV files used as input data for the application.

``database/``
   Contains the local SQL database files used by the application.

``docs/``
   Contains this Sphinx documentation.

``src/``
   Contains the main application logic.

``tests/``
   Contains unit tests for the project.

``visualization/``
   Contains generated image files and plotted function outputs.

``main.py``
   Starts the command-line application.

API Documentation
-----------------

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   modules