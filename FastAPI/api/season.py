""" Endpoints for fetching information related to Seasons """
from fastapi import APIRouter
from .utils import get_cursor, use_cursor

router = APIRouter()


@router.get('/')
async def get_seasons():
    return use_cursor(get_cursor(), 'SELECT * FROM season')


@router.get('/{season_id}')
async def get_season(season_id: int):
    return use_cursor(get_cursor(), 'SELECT * FROM season WHERE id=%s',
                      (season_id, ))


@router.get('/{season_id}/teams')
async def get_teams(season_id: int):
    return use_cursor(get_cursor(), 'SELECT * FROM team WHERE season=%s',
                      (season_id, ))


@router.get('/{season_id}/tournaments')
async def get_tournaments(season_id: int):
    return use_cursor(get_cursor(), 'SELECT * FROM tournament WHERE season_id=%s',
                      (season_id, ))


@router.get('/{season_id}/rounds')
async def get_tournaments(season_id: int):
    return use_cursor(
        get_cursor(),
        f'''SELECT * FROM round
        LEFT JOIN tournament ON tournament.id = round.tournament_id
        WHERE tournament.season_id=%s''',
        (season_id, ))

#EOF
