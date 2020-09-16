""" Endpoints for fetching information related to Teams """
from fastapi import APIRouter
from .utils import get_cursor, use_cursor

router = APIRouter()


@router.get('/')
async def get_teams():
    return use_cursor(get_cursor(), 'SELECT * FROM team')


@router.get('/{team_id}')
async def get_team(team_id: int):
    return use_cursor(get_cursor(), 'SELECT * FROM team WHERE id=%s',
                      (team_id, ))


@router.get('/{team_id}/tournaments')
async def get_tournaments(team_id: int):
    return use_cursor(
        get_cursor(),
        f'''SELECT tournament.id, tournament.name FROM tournament
        LEFT JOIN round ON tournament.id=round.tournament_id
        LEFT JOIN team ON (round.team_1=team.id OR round.team_2=team.id)
        WHERE team.id=%s''',
        (team_id, ))


@router.get('/{team_id}/rounds')
async def get_rounds(team_id: int):
    return use_cursor(
        get_cursor(),
        f'''SELECT
            round.*, team1.name AS name1, team1.elo AS elo1, team2.name AS name2, team2.elo as elo2
        FROM round
        LEFT JOIN team AS team1 ON (round.team_1=team1.id)
        LEFT JOIN team AS team2 ON (round.team_2=team2.id)
        WHERE team1.id=%s or team2.id=%s''',
        (team_id, team_id,))

# EOF
