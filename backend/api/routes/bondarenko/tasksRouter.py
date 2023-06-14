from fastapi import APIRouter, Depends, WebSocket
import pydantic
from ...contracts.bondarenko import dtos
from ...services.bondarenko import tasksService
from ...data.bondarenko.sqlite.utils import get_db, reset_db_state
from .websocketsRouter import get_ws_clients
from ...contracts.bondarenko.responses import ResultResponse, MainResponse

router = APIRouter(
    prefix="/bondarenko/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

@router.post('/create', summary='Создать задачу парсинга', dependencies=[Depends(get_db)])
async def create_task(request : dtos.CreateParseTaskRequestDto):
    return await tasksService.create_new_task(request.theme_uri, request.theme_name, request.from_page, request.to_page)

@router.post('/run/{task_uuid}', summary='Запустить задачу парсинга', dependencies=[Depends(get_db)])
async def run_task(task_uuid, ws_client=Depends(get_ws_clients)):
    return await tasksService.run_task(task_uuid, ws_client)

@router.post('/stop/{task_uuid}', summary='Остановить задачу парсинга страниц', dependencies=[Depends(get_db)])
async def stop_task(task_uuid):
    return await tasksService.stop_task(task_uuid)

@router.get('', summary='Получить задачи парсинга', dependencies=[Depends(get_db)])
async def get_all_tasks():
    return await tasksService.get_all_tasks()

@router.get('/{task_uuid}/csv', summary='Получить csv файл', dependencies=[Depends(get_db)])
async def get_scv(task_uuid):
    return await tasksService.get_csv(task_uuid);