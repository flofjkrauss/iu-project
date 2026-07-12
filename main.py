from __future__ import annotations

from exceptions.InputExceptions import InvalidUserInput
from src.import_csv_data import ImportCsvData
from src.data_visualizer import DataVisualizer
from src.function_matcher import FunctionMatcher

from src.utils import validate_user_input, show_help

"""
Command-line entry point

Run the interactive command-line loop.
"""
def main() -> None:
    print("Interactive mode started.")
    print("Exit with: exit, quit or q")
    db = ImportCsvData()
    visualizer = DataVisualizer()
    matcher = FunctionMatcher(db=db, visualizer=visualizer)
    show_help()
    while True:
        user_input = input("\n>>> ")
        try:
            validate_user_input(user_input=user_input,
                                db=db,
                                visualizer=visualizer,
                                matcher=matcher
                                )                 
        except InvalidUserInput as error:
            print(f"Invalid user input: {error}")
            continue

if __name__ == "__main__":
    main()
