""" Endpoints for fetching information related to Activities """
from fastapi import APIRouter
from .utils import get_cursor

router = APIRouter()


@router.get('/')
async def get_activities():
    return get_cursor().execute('SELECT * FROM activity').fetchall()


@router.get('/{activity_id}')
async def get_activity(activity_id):
    return get_cursor().execute('SELECT * FROM activity WHERE id=%s',
                                (activity_id)).fetchall()


@router.get('/{activity_id}/season')
async def get_seasons(activity_id):
    return get_cursor().execute(
        'SELECT * FROM season WHERE activity_id=%s', (activity_id, )).fetchall()


@router.get('/{activity_id}/teams')
async def get_teams(activity_id):
    return get_cursor().execute(
        'SELECT * FROM team WHERE activity=%s', (activity_id, )).fetchall()


@router.get('/{activity_id}/tournaments')
async def get_tournaments(activity_id):
    return get_cursor().execute(
        f'''SELECT * FROM tournament
        LEFT JOIN season ON season.id=tournament.id
        WHERE season.activity_id=%s''',
        (activity_id, )).fetchall()


@router.get('/{activity_id}/rounds')
async def get_rounds(activity_id):
    return get_cursor().execute(
    f'''SELECT * FROM round
    LEFT JOIN tournament ON tournament.id=round.tournament_id
    LEFT JOIN season ON season.id=tournament.season_id
    WHERE season.activity_id=%s''',
    (activity_id, )).fetchall()

#EOF
