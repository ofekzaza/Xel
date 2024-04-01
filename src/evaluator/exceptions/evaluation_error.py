class EvaluationError(RuntimeError):
    """
    Base exception for known evaluation error,
    so it can be cached and replaced with its message for the user
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
