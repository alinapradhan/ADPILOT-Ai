from fastapi import HTTPException, status


class AuthorizationError(HTTPException):
    def __init__(self, detail: str = "Not authorized for this client/account") -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class DataProviderError(HTTPException):
    def __init__(self, detail: str = "Provider request failed") -> None:
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)
