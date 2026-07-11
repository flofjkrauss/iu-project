class InvalidUserInput(Exception):
    """
    Exception raised when user input cannot be processed.
    """
    def __init__(self, user_input: str) -> None:
        message = (f"'{user_input}' is not a valid input. ")
        super().__init__(message)

class FalseValidUserInput(Exception):
    """
    Exception raised when user input was processed, but should not.
    """
    def __init__(self, user_input: str) -> None:
        message = (f"'{user_input}' has been handled as valid user input, but it is not. Are there not existing commands still in COMMAND list?")
        super().__init__(message)