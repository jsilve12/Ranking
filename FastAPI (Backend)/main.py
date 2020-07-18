"""Origin for FastAPI."""

from fastapi import Depends, FastAPI, Header, HTTPException

from .Routers import *
from .API import *

app = FastAPI()


# async def get_token_header(x_token: str = Header(...)):
#     """Get the token from the header."""
#     if x_token != 'Fake Token':
#         raise HTTPException(status_code=403, detail='Invalid Token')


app.include_router(
    seasons.router,
    prefix='/api/seasons/',
    tags=['seasons']
)
app.include_router(
    teams.router,
    prefix='/api/teams/',
    tags=['teams']
)
# EOF
