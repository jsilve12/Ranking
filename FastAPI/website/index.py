""" Main Website Landing Page """
from fastapi import APIRouter
from fastapi.response import HTMLResponses
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@router.get('/{activity_id}/{season_id}')
async def get_season(activity_id: int, season_id: int):
    return templates.TemplateResponse('index.html', {'activity': activity_id, 'season': season_id})
