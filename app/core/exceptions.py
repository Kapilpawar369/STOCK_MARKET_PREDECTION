# from fastapi import HTTPException, status

# class NotFound(HTTPException):
#     def __init__(self, detail: str = "Resource not found"):
#         super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

# class BadRequest(HTTPException):
#     def __init__(self, detail: str = "Bad request"):
#         super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

# class Unauthorized(HTTPException):
#     def __init__(self, detail: str = "Unauthorized"):
#         super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

# class Forbidden(HTTPException):
#     def __init__(self, detail: str = "Forbidden"):
#         super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

# class PaymentFailed(HTTPException):
#     def __init__(self, detail: str = "Payment failed"):
#         super().__init__(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=detail)


from fastapi import Request
from fastapi.responses import JSONResponse

class CustomError(Exception):
    def __init__(self,message:str,status_code:int=400):
        self.message=message
        self.status_code=status_code

async def custom_error_handler(request: Request, exc: CustomError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "data": {},
            "status": exc.status_code,
            "message": exc.message,
            "error": True,
        }
    )