from fastapi import status

class AppError(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str):
        super().__init__(message)
        
        self.message = message or "App error"

class NotFound(AppError):
    status_code = status.HTTP_404_NOT_FOUND

class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT

class RequestNotFound(NotFound):
    pass

