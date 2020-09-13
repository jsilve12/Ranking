""" Endpoints for fetching information related to tournaments """
from fastapi import APIRouter
from .utils import get_cursor, use_cursor

router = APIRouter()


@router.get('/')
async def get_tournaments():
    return use_cursor(get_cursor(), 'SELECT * FROM tournament')


@router.get('/{tournament_id}')
async def get_tournament(tournament_id: int):
    return use_cursor(get_cursor(), 'SELECT * FROM tournament WHERE id=%s',
                      (tournament_id, ))


@router.get('/{tournament_id}/teams')
async def get_teams(tournament_id: int):
    return use_cursor(
        get_cursor(),
        f'''SELECT team.* FROM team
        LEFT JOIN round ON (round.team_1=team.id OR round.team_2=team.id)
        LEFT JOIN tournament ON tournament.id=round.tournament_id
        WHERE tournament.id=%s''',
        (tournament_id, ))


@router.get('/{tournament_id}/rounds')
async def get_rounds(tournament_id: int):
    return use_cursor(
        get_cursor(),
        f'''SELECT round.* FROM round
        LEFT JOIN tournament ON tournament.id=round.tournament_id
        WHERE tournament.id=%s''',
        (tournament_id, ))

# EOF
