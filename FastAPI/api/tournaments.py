""" Endpoints for fetching information related to tournaments """
from fastapi import APIRouter
from .utils import get_cursor

router = APIRouter()


@router.get('/')
async def get_tournaments():
    return get_cursor().execute('SELECT * FROM tournament').fetchall()


@router.get('/{tournament_id}')
async def get_tournament(tournament_id: int):
    return get_cursor().execute('SELECT * FROM tournament WHERE id=%s',
                                (tournament_id, )).fetchall()


@router.get('/{tournament_id}/teams')
async def get_teams(tournament_id: int):
    return get_cursor().execute(
        f'''SELECT * FROM team
        LEFT JOIN round ON (round.team_id=team.id OR round.team_2=team.id)
        LEFT JOIN tournament ON tournament.id=round.tournament_id
        WHERE tournament.id=%s''',
        (tournament_id, )).fetchall()


@router.get('/{tournament_id}/rounds')
async def get_rounds(tournament_id: int):
    return get_cursor().execute(
        f'''SELECT * FROM round
        LEFT JOIN round ON tournament.id=round.tournament_id
        WHERE tournament.id=%s''',
        (tournament_id, )).fetchall()

# EOF
