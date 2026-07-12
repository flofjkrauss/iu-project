from __future__ import annotations
import sys

from exceptions.InputExceptions import InvalidUserInput, FalseValidUserInput
from exceptions.DatabaseExceptions import DbNotConnected
from src.import_csv_data import ImportCsvData
from src.data_visualizer import DataVisualizer

"""
Command-line entry point

small interactive loop that reads user input from the
terminal and reacts to simple commands.
"""

COMMANDS = {
    "help": "Show available commands.",
    "import": "Import CSV files under the /input directory. (Expected: train.csv, test.csv, ideal.csv)",
    "exit": "Exit the application.",
    "quit": "Exit the application.",
    "q": "Exit the application.",
    "plot all": "Create HTML plots for all x-y combos stored in the database",
    "plot [table] [y_column]": "Generate a single plot from [table] using x and [y_column] values (i.e. plot ideal_functions 35)",
}

def show_help() -> None:
    """
    Return a formatted help text for all available commands.

    Returns
    -------
    str
        Human-readable help text listing all supported user commands.
    """
    lines = ["Available commands:"]

    for command, description in sorted(COMMANDS.items()):
        lines.append(f"  {command:<10} {description}")

    print("\n".join(lines))

def validate_user_input(user_input: str) -> str:
    """
    Process one user input and returns it, if valid.

    Parameters
    ----------
    user_input:
        Raw text entered by the user.

    Returns
    -------
    str
        valid user input
    """

    cleaned_input = user_input.strip()

    if(user_input not in COMMANDS or not cleaned_input):
        if not user_input.startswith("plot"):
            raise InvalidUserInput(user_input)

    handle_user_input(user_input)
    return None

def handle_user_input(user_input: str) -> None:
    if(user_input == "help"):
        show_help()
    elif (user_input == "exit" or user_input == "quit" or user_input == "q"):
        sys.exit(0)
    elif (user_input=="import"):
        if not db:
            raise DbNotConnected()
        db.load_all_inputs()
        # just for debugging, delete later
        print(db.read_table_by_name("train_data"))
        print(db.read_table_by_name("test_data"))
        print(db.read_table_by_name("ideal_functions"))
    elif(user_input.startswith("plot")):
        response = handle_plot_request(user_input)
        if not response:
            raise InvalidUserInput(user_input)
    else:
        raise FalseValidUserInput(user_input)
    
def handle_plot_request(user_input: str) -> bool:
    """
    Handle plot commands entered by the user.

    Parameters
    ----------
    user_input:
        Raw user input, for example ``plot all`` or
        ``plot ideal_functions y35``.

    Returns
    -------
    bool
        True if the plot request was handled successfully, otherwise False.
    """
    if (user_input == "plot all"):
        visualizer.save_all_xy_plots(
            db.read_table_by_name("train_data"),
            table_name="train_data",
        )
        visualizer.save_all_xy_plots(
            db.read_table_by_name("test_data"),
            table_name="test_data",
        )
        visualizer.save_all_xy_plots(
            db.read_table_by_name("ideal_functions"),
            table_name="ideal_functions",
        )
        return True

    parts = user_input.split()

    if len(parts) != 3:
        print("Invalid plot command. Use: plot <table> <y_column>")
        return False

    _, table_name, y_column = parts

    if table_name not in db.TABLE_NAMES:
        print(f"Possible tables to plot: {db.TABLE_NAMES}")
        return False

    dataframe = db.read_table_by_name(table_name)

    if(y_column=="grid"):
        visualizer.save_table_grid_plot(dataframe, table_name)
        return True

    if y_column not in dataframe.columns:
        possible_columns = [
            column
            for column in dataframe.columns
            if column not in {"id", "x"}
        ]
        print(f"Possible columns to plot for {table_name}: {possible_columns}")
        return False

    if "x" not in dataframe.columns:
        print(f"Table {table_name} does not contain an x column.")
        return False

    visualizer.show_xy_plot(
        dataframe=dataframe,
        table_name=table_name,
        x_column="x",
        y_column=y_column,
    )

    return True


"""
Run the interactive command-line loop.

The loop accepts user input until one of the configured exit commands is
entered. Application-specific commands can later be routed from this
function into separate modules.
"""
def main() -> None:
    print("Interactive mode started.")
    print("Exit with: exit, quit or q")
    global db
    db = ImportCsvData()
    global visualizer
    visualizer = DataVisualizer()
    while True:
        user_input = input("> ")
        try:
            validate_user_input(user_input.strip().lower())         
        
        except InvalidUserInput as error:
            print(f"Invalid user input: {error}")
            continue

if __name__ == "__main__":
    main()
