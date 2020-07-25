""" Endpoints for fetching information related to Seasons """
from fastapi import APIRouter
from .utils import get_cursor

router = APIRouter()


@router.get('/')
async def get_seasons():
    return get_cursor().execute('SELECT * FROM season').fetchall()


@router.get('/{season_id}')
async def get_season(season_id: int):
    return get_cursor().execute('SELECT * FROM season WHERE id=%s',
                                (season_id, )).fetchall()


@router.get('/{season_id}/teams')
async def get_teams(season_id: int):
    return get_cursor().execute('SELECT * FROM team WHERE season_id=%s',
                                (season_id, )).fetchall()


@router.get('/{season_id}/tournaments')
async def get_tournaments(season_id: int):
    return get_cursor().execute('SELECT * FROM tournament WHERE season_id=%s',
                                (season_id, )).fetchall()


@router.get('/{season_id}/rounds')
async def get_tournaments(season_id: int):
    return get_cursor().execute(
        f'''SELECT * FROM round
        LEFT JOIN tournaments ON tournament.id = round.tournament_id
        WHERE tournament.season_id=%s''',
        (season_id, )).fetchall()

#EOF
