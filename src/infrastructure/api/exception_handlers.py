from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain.exceptions.UnauthorizedActionException import (
    UnauthorizedActionException,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(UnauthorizedActionException)
    async def unauthorized_handler(
        request: Request,
        exc: UnauthorizedActionException,
    ):
        return JSONResponse(
            status_code=403,
            content={"detail": str(exc)},
        )