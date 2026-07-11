from __future__ import annotations
import sys

from exceptions.InputExceptions import InvalidUserInput, FalseValidUserInput
from exceptions.DatabaseExceptions import DbNotConnected
from src.import_csv_data import ImportCsvData

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
    "q": "Exit the application."
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
    else:
        raise FalseValidUserInput(user_input)

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

    while True:
        user_input = input("> ")
        try:
            validate_user_input(user_input.strip().lower())         
        
        except InvalidUserInput as error:
            print(f"Invalid user input: {error}")
            continue

if __name__ == "__main__":
    main()
