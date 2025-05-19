from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, resource: str = "", status_code: int = 400):
        super().__init__(404, resource + " was not found, the resource does not exist or has been moved")


not_found = NotFoundError()


class NoResourceError(HTTPException):
    def __init__(self, resource: str = "", status_code: int = 400):
        super().__init__(402, f"Not found")


no_resource = NoResourceError()


class NotAuthorizedError(HTTPException):
    def __init__(self, resource: str = "", status_code: int = 400):
        super().__init__(403, f"Forbidden access - you do not have access to this resource")


not_authorized = NotAuthorizedError()


class InvalidTokenError(HTTPException):
    def __init__(self, resource: str = "", status_code: int = 400):
        super().__init__(401, f"Invalid token, please login")


invalid_token = InvalidTokenError()


class InvalidRequestError(HTTPException):
    def __init__(self, resource: str = "", status_code: int = 400):
        super().__init__(400, f"The request is invalid, please check the request body and try again. {resource}")


invalid_request = InvalidRequestError("")


class InternalServerError(HTTPException):
    def __init__(self, resource: str, status_code: int = 500):
        super().__init__(500, f"Internal server error, please try again later. {resource}")


internal_error = InternalServerError("")


