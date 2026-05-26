from src.core.exceptions import AppError


class ReviewsValidationError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=422)


class NLPProcessingError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=500)


class LLMSummarizationError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=502)
