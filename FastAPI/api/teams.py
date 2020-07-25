""" Endpoints for fetching information related to Teams """
from fastapi import APIRouter
from .utils import get_cursor

router = APIRouter()


@router.get('/')
async def get_teams():
    return get_cursor().execute('SELECT * FROM team').fetchall()


@router.get('/{team_id}')
async def get_team(team_id: int):
    return get_cursor().execute('SELECT * FROM team WHERE id=%s',
                                (team_id, )).fetchall()


@router.get('/{team_id}/tournaments')
async def get_tournaments(team_id: int):
    return get_cursor().execute(
        f'''SELECT * FROM tournament
        LEFT JOIN round ON tournament.id=round.tournament_id
        LEFT JOIN team ON (round.team_1=team.id OR round.team_2=team.id)
        WHERE team.id=%s''',
        (team_id, )).fetchall()


@router.get('/{team_id}/rounds')
async def get_rounds(team_id: int):
    return get_cursor().execute(
        f'''SELECT * FROM round
        LEFT JOIN team ON (round.team_1=team.id OR round.team_2=team.id)
        WHERE team.id=%s''',
        (team_id, )).fetchall()

# EOF
