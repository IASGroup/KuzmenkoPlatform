from fastapi import APIRouter, Depends, WebSocket
from ...contracts.bondarenko.responses import ResultResponse, MainResponse
from ...services.bondarenko.parseService import get_themes as _get_themes, get_max_pages as _get_max_pages, send_message_to_websocket as _send_message_to_websocket
from ...data.bondarenko.sqlite.utils import get_db, reset_db_state
from fastapi_cache.decorator import cache
import requests
from bs4 import BeautifulSoup
from .websocketsRouter import get_ws_clients
from pydantic import BaseModel
from typing import List
import asyncio

router = APIRouter(
    prefix="/bondarenko/cyberleninka/parser",
    tags=["parser"],
    responses={404: {"description": "Not found"}},
)

@router.get('/themes', summary='Получить список научных тем cyberleninka', dependencies=[Depends(get_db)])
async def get_themes():
    return await _get_themes()

class GetMaxPagesRequest(BaseModel):
    relativeUrl: str

@router.post('/max-page', summary='Получить максимальную страницу научной темы', dependencies=[Depends(get_db)])
async def get_max_page(request: GetMaxPagesRequest):
    return await _get_max_pages(request.relativeUrl)