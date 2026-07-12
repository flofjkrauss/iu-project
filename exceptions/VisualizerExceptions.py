from src.constants import VALID_PLOT_OUTPUT_OPTIONS

class InvalidPlotOutputOptions(Exception):
    """
    Exception raised when user input cannot be processed.
    """
    def __init__(self, option: str) -> None:
        message = (f"'{option}' is not a valid output option for plots.  Valid output options are: {VALID_PLOT_OUTPUT_OPTIONS}")
        super().__init__(message)