"""Origin for FastAPI."""

from fastapi import Depends, FastAPI, Header, HTTPException
from .api import activity, season, rounds, teams, tournaments

app = FastAPI()


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
# EOF
