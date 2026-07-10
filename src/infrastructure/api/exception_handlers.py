from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain.exceptions.UnauthorizedActionException import UnauthorizedActionException



def register_exception_handlers(app: FastAPI):

    @app.exception_handler(UnauthorizedActionException)
    async def unauthorized_handler(request: Request, exc: UnauthorizedActionException):
        print(exc)

        return JSONResponse(
            status_code=403,
            content={
                "message": str(exc)
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        print(exc)

        return JSONResponse(
            status_code=500,
            content={
                "message": "Error interno del servidor"
            }
        )