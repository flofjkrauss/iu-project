class DbNotConnected(Exception):
    """
    Exception raised when no db instance can be found.
    """
    def __init__(self) -> None:
        message = ("No Database connected")
        super().__init__(message)

