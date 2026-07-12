# globally used constants

from pathlib import Path

"""
only commands listed here will be recognized as valid user input
"""
COMMANDS = {
    "help": "Show available commands.",
    "import": "Import CSV files under the /input directory. (Expected: train.csv, test.csv, ideal.csv)",
    "exit": "Exit the application.",
    "quit": "Exit the application.",
    "q": "Exit the application.",
    "plot all": "Create HTML plots for all x-y combos stored in the database",
    "plot [table] [y_column]": "Generate a single plot from [table] using x and [y_column] values (i.e. plot ideal_functions 35)",
    "plot [table] grid": "Generate a full grid of all plots of [table]",
    "match": "Match ideal to train functions and evaluate best for test points."
}

"""
table names for SQL database
"""
TABLE_NAMES = {
    "train": "train_data",
    "ideal": "ideal_functions",
    "test": "test_data"
}

"""
project folder
"""
PROJECT_ROOT = Path(__file__).resolve().parent.parent

"""
additional paths with respect to project folder
"""
PATHS = {
    "root": PROJECT_ROOT,
    "db": PROJECT_ROOT / "database" / "project.sqlite3",
    "input": PROJECT_ROOT / "input",
    "visualization": PROJECT_ROOT / "visualizations",
    "database": PROJECT_ROOT / "database" / "project.sqlite3"
}

VALID_PLOT_OUTPUT_OPTIONS = ("save", "show", "both")