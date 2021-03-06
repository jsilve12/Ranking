""" Endpoints for fetching information related to Activities """
from fastapi import APIRouter
from .utils import get_cursor, use_cursor

router = APIRouter()


@router.get('/')
async def get_activities():
    return use_cursor(get_cursor(), 'SELECT * FROM activity')


@router.get('/{activity_id}')
async def get_activity(activity_id: int):
    return use_cursor(
        get_cursor(), 'SELECT * FROM activity WHERE id=%s',
        (activity_id, ))[0]


@router.get('/{activity_id}/season')
async def get_seasons(activity_id: int):
    return use_cursor(
        get_cursor(),
        'SELECT * FROM season WHERE activity_id=%s', (activity_id, ))


@router.get('/{activity_id}/teams')
async def get_teams(activity_id: int):
    return use_cursor(
        get_cursor(),
        'SELECT * FROM team WHERE activity=%s', (activity_id, ))


@router.get('/{activity_id}/tournaments')
async def get_tournaments(activity_id: int):
    return use_cursor(
        get_cursor(),
        f'''SELECT * FROM tournament
        LEFT JOIN season ON season.id=tournament.id
        WHERE season.activity_id=%s''',
        (activity_id, ))


@router.get('/{activity_id}/rounds')
async def get_rounds(activity_id: int):
    return use_cursor(
        get_cursor(),
        f'''SELECT * FROM round
        LEFT JOIN tournament ON tournament.id=round.tournament_id
        LEFT JOIN season ON season.id=tournament.season_id
        WHERE season.activity_id=%s''',
        (activity_id, ))

#EOF
