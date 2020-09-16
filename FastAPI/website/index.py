""" Main Website Landing Page """
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = APIRouter()
templates = Jinja2Templates(directory='FastAPI/templates')

@app.get('/activity/{activity_id}/{season_id}', response_class=HTMLResponse)
async def get_season(activity_id: int, season_id: int, request: Request):
    return templates.TemplateResponse('index.html', {'activity': activity_id, 'season': season_id, 'request': request})

@app.get('/teams/{team_id}', response_class=HTMLResponse)
async def get_team(team_id: int, request: Request):
    return templates.TemplateResponse('team.html', {'team': team_id, 'request': request})
