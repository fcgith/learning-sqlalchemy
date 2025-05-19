from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, resource: str, status_code: int = 400):
        super().__init__(404, resource + " was not found, the resource does not exist or has been moved")


not_found = lambda resource: NotFoundError(resource)


class NoResourceError(HTTPException):
    def __init__(self, resource: str, status_code: int = 400):
        super().__init__(402, f"No {resource} found for this request")


no_resource = lambda resource: NoResourceError(resource)


class NotAuthorizedError(HTTPException):
    def __init__(self, resource: str, status_code: int = 400):
        super().__init__(403, f"Forbidden access - you do not have access to {resource}")


not_authorized = lambda resource: NotAuthorizedError(resource)


class InvalidTokenError(HTTPException):
    def __init__(self, resource: str, status_code: int = 400):
        super().__init__(401, f"Invalid token, please login")


invalid_token = lambda resource: InvalidTokenError(resource)


class InvalidRequestError(HTTPException):
    def __init__(self, resource: str, status_code: int = 400):
        super().__init__(400, f"The request is invalid, please check the request body and try again. {resource}")


invalid_request = lambda resource: InvalidRequestError(resource)


class InternalServerError(HTTPException):
    def __init__(self, resource: str, status_code: int = 500):
        super().__init__(500, f"Internal server error, please try again later. {resource}")


internal_error = lambda resource: InternalServerError(resource)


