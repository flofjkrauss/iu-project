from __future__ import annotations
import sys
from src.constants import COMMANDS, TABLE_NAMES

from src.import_csv_data import ImportCsvData
from src.function_matcher import FunctionMatcher
from src.data_visualizer import DataVisualizer

from exceptions.InputExceptions import InvalidUserInput, FalseValidUserInput
from exceptions.DatabaseExceptions import DbNotConnected

# helper functions
def show_help() -> None:
    """
    Print usage help
    """
    lines = ["Available commands:"]

    for command, description in sorted(COMMANDS.items()):
        lines.append(f"  {command:<25} {description}")

    print("\n".join(lines))
    return None

def validate_user_input(user_input: str, 
                        db: ImportCsvData, 
                        visualizer: DataVisualizer, 
                        matcher: FunctionMatcher
                        ) -> None:
    """
    Validate user input.
    If the input is valid, it will be processed to handle_user_input and executed.

    Parameters
    ----------
    user_input:
        Raw text entered by the user.
    db:
        database handle
    visualizer:
        handle for the data_visualizer class
    matcher:
        handle for the function_matcher class
    """

    cleaned_input = user_input.strip().lower()

    if(user_input not in COMMANDS or not cleaned_input):
        if not user_input.startswith("plot"):
            raise InvalidUserInput(user_input)
        
    if not db:
            raise DbNotConnected()

    handle_user_input(user_input, db, visualizer, matcher)
    return None

def handle_user_input(user_input: str,                       
                      db: ImportCsvData, 
                      visualizer: DataVisualizer,
                      matcher: FunctionMatcher                      
                      ) -> None:
    """
    Handle user input.
    The input is valid and the corresponding command will now be executed.

    Parameters
    ----------
    user_input:
        Raw text entered by the user.
    db:
        database handle
    visualizer:
        handle for the data_visualizer class
    matcher:
        handle for the function_matcher class
    """
    if(user_input == "help"):
        show_help()
    elif (user_input == "exit" or user_input == "quit" or user_input == "q"):
        sys.exit(0)
    elif (user_input=="import"):        
        db.load_all_inputs()      
    elif(user_input.startswith("plot")):
        response = handle_plot_request(user_input, db, visualizer)
        if not response:
            raise InvalidUserInput(user_input)
    elif(user_input=="match"): 
        train_data = db.read_table_by_name(TABLE_NAMES["train"])
        ideal_data = db.read_table_by_name(TABLE_NAMES["ideal"])
        selected = matcher.select_best_ideal_functions(
            train_data=train_data,
            ideal_data=ideal_data
        )
        db.insert_selection(table_name="selection", dataframe=selected)
        
        visualizer.selection_grid_plot(selection=selected,
                                       train_data=train_data,
                                       ideal_data=ideal_data)
       
        matched = matcher.match_test_data(
            test_data=db.read_table_by_name(TABLE_NAMES["test"]),
            ideal_data=db.read_table_by_name(TABLE_NAMES["ideal"]), 
            selected_functions=selected
            )
        db.insert_selection(table_name="test_match", dataframe=matched)
        print(db.read_table_by_name("test_match"))    
    else:
        raise FalseValidUserInput(user_input)
    
def handle_plot_request(user_input: str, 
                        db: ImportCsvData,
                        visualizer: DataVisualizer                        
                        ) -> bool:
    """
    Handle plot requests

    Parameters
    ----------
    user_input:
        Raw user input, for example 'plot all' or
        'plot ideal y35'.
    db:
        database handle
    visualizer:
        handle for the data_visualizer class

    Returns
    -------
    bool
        True if the plot request was handled successfully, otherwise False.
    """
    if (user_input == "plot all"):
        visualizer.save_all_xy_plots(
            dataframe=db.read_table_by_name(TABLE_NAMES["train"]),
            table_name=TABLE_NAMES["train"]
            )
        visualizer.save_all_xy_plots(
            dataframe=db.read_table_by_name(TABLE_NAMES["test"]),
            table_name=TABLE_NAMES["test"]
            )
        visualizer.save_all_xy_plots(
            dataframe=db.read_table_by_name(TABLE_NAMES["ideal"]),
            table_name=TABLE_NAMES["ideal"]
            )
        return True

    parts = user_input.split()

    if len(parts) != 3:
        print("Invalid plot command. Use: plot <table> <y_column>")
        return False

    table_name, y_column = parts[1:3]

    if table_name not in TABLE_NAMES:
        print(f"Possible tables to plot: {TABLE_NAMES}")
        return False

    dataframe = db.read_table_by_name(TABLE_NAMES[table_name])

    if y_column == "x": 
        print("You want a straight line? Here is one:")
        print("________________________________________")
        return False
    
    if y_column=="grid":
        visualizer.table_grid_plot(
            dataframe=dataframe,
            table_name=TABLE_NAMES[table_name]
            )
        return True

    if y_column not in dataframe.columns:
        possible_columns = []
        for column in dataframe.columns:
            if column != "x":
                possible_columns.append(column)
        
        print(f"Possible columns to plot for {TABLE_NAMES[table_name]}: {possible_columns}")
        return False

    if "x" not in dataframe.columns:
        print(f"Table {TABLE_NAMES[table_name]} does not contain an x column.")
        return False

    visualizer.xy_plot(
        dataframe=dataframe,
        table_name=TABLE_NAMES[table_name],
        x_column="x",
        y_column=y_column,
        output="show"
    )

    return True