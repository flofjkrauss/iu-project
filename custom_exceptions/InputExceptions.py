class InvalidUserInput(Exception):
    """Exception raised when user input cannot be processed."""

    def __init__(self, user_input: str) -> None:
        """Initialize the exception with invalid input and valid options."""  
        message = (f"'{user_input}' is not a valid input. ")
        super().__init__(message)