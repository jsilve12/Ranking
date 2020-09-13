"""Origin for FastAPI."""

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from .api import activity, season, rounds, teams, tournaments
from .website import index

app = FastAPI()
app.mount('/static', StaticFiles(directory='FastAPI/static'), name='static')


# async def get_token_header(x_token: str = Header(...)):
#     """Get the token from the header."""
#     if x_token != 'Fake Token':
#         raise HTTPException(status_code=403, detail='Invalid Token')


app.include_router(
    activity.router,
    prefix='/api/activity',
    tags=['activity']
)
app.include_router(
    season.router,
    prefix='/api/season',
    tags=['season']
)
app.include_router(
    teams.router,
    prefix='/api/team',
    tags=['team']
)
app.include_router(
    tournaments.router,
    prefix='/api/tournament',
    tags=['tournament']
)
app.include_router(
    rounds.router,
    prefix='/api/round',
    tags=['round']
)
app.include_router(
    index.app,
    tags=['webpage']
)
# EOF
