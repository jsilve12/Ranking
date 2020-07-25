""" Endpoints for fetching information related to rounds """
from fastapi import APIRouter
from .utils import get_cursor

router = APIRouter()


@router.get('/')
async def get_rounds():
    return get_cursor().execute('SELECT * FROM round').fetchall()


@router.get('/{round_id}')
async def get_round(round_id):
    return get_cursor().execute('SELECT * FROM round WHERE id=%s',
                                (round_id, )).fetchall()

# EOF
