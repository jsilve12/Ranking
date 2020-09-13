""" Endpoints for fetching information related to rounds """
from fastapi import APIRouter
from .utils import get_cursor, use_cursor

router = APIRouter()


@router.get('/')
async def get_rounds():
    return use_cursor(get_cursor(), 'SELECT * FROM round')


@router.get('/{round_id}')
async def get_round(round_id: int):
    return use_cursor(get_cursor(), 'SELECT * FROM round WHERE id=%s',
                      (round_id, ))

# EOF
