from ...contracts.bondarenko.responses import ResultResponse, MainResponse
from ...data.bondarenko.sqlite import models
from ...contracts.bondarenko import dtos
from .parseService import get_article_links_on_page, get_article, send_message_to_websocket
from ...data.bondarenko.sqlite.models import Article
import uuid
import pydantic
import asyncio
import json
import io
import pandas as pd
from fastapi.responses import StreamingResponse

running_tasks = {}

async def parse_pages(relativeThemeUrl, fromPage, toPage, ws_clients, task_id):
    for i in range(fromPage, toPage + 1):
        if running_tasks[task_id]['is_cancelled']:
            print(f'{task_id} cancelled')
            running_tasks.pop(task_id)
            return MainResponse.success()
        article_links_response = await get_article_links_on_page(f'{relativeThemeUrl}/{i}')
        articles_in_db = list(Article.select().where(Article.uri << article_links_response.result))
        article_in_db_uris = list(map(lambda x: x.uri,articles_in_db))
        need_parse_uri = list(filter(lambda x: x not in article_in_db_uris, article_links_response.result))
        already_parsed = article_links_response.result.__len__() - need_parse_uri.__len__()
        for uri in need_parse_uri:
            if running_tasks[task_id]['is_cancelled']:
                print(f'{task_id} cancelled')
                running_tasks.pop(task_id)
                return MainResponse.success()
            get_article_response = await get_article(uri)
            article = get_article_response.result
            test = Article.create(
                uri=uri,
                page=i,
                theme_uri=relativeThemeUrl,
                theme_name=article['theme'],
                title=article['title'],
                authors=article['authors'],
                journal=article['journal'],
                keywords=article['keywords'],
                description=article['description'],
                content=article['content']
            )
            already_parsed += 1
            message = {
                "task_id": task_id,
                "current_article_number": already_parsed,
                "all_article_number": article_links_response.result.__len__(),
                "page": i
            }
            await send_message_to_websocket(topic='parsing', message=json.dumps(message), ws_clients=ws_clients)
            await asyncio.sleep(0.2)
        models.ParseTask.update(last_parsed_page=i).where(models.ParseTask.id == task_id).execute()
    running_tasks.pop(task_id)
    models.ParseTask.update(is_done=True).where(models.ParseTask.id == task_id).execute()
    done_task_message = {
        "task_id": task_id
    }
    await send_message_to_websocket(topic='parsing-end', message=json.dumps(done_task_message), ws_clients=ws_clients)        
    return MainResponse.success()

async def get_all_tasks() -> dtos.ParseTaskDto:
    tasks = list(models.ParseTask.select())
    tasks_dtos = []
    for task in tasks:
        id_str = str(task.id)
        is_running = id_str in running_tasks
        current_page = task.last_parsed_page
        current_article = 1 if is_running == False else running_tasks[id_str]['current_article_number']
        dto = dtos.ParseTaskDto(
            id=id_str,
            theme_uri=task.theme_uri,
            theme_name=task.theme_name,
            from_page=task.from_page,
            to_page=task.to_page,
            current_page=current_page,
            current_article=current_article,
            is_done=task.is_done,
            is_running=is_running
        )
        tasks_dtos.append(dto) 
    return ResultResponse.success(tasks_dtos)

async def create_new_task(theme_uri: str, theme_name: str, from_page: int, to_page: int) -> dtos.ParseTaskDto:
    id = str(uuid.uuid4())
    models.ParseTask.create(
        id = id,
        theme_uri=theme_uri,
        theme_name=theme_name,
        from_page=from_page,
        to_page=to_page,
        is_done=False,
        last_parsed_page=from_page
    )
    return ResultResponse.success(dtos.ParseTaskDto(
        id=id,
        theme_uri=theme_uri,
        from_page=from_page,
        theme_name=theme_name,
        to_page=to_page,
        current_page=from_page,
        current_article=1,
        is_done=False,
        is_running=False
    ))

async def get_taks(task_id: str):
    return null

async def stop_task(task_id: str):
    task = running_tasks[task_id]
    task['is_cancelled'] = True
    return MainResponse.success()

async def run_task(task_id: str, ws_clients):
    task_model = models.ParseTask.get_by_id(task_id)
    running_tasks[str(task_model.id)] = { 'current_article_number' : 1, 'is_cancelled': False }
    asyncio.create_task(parse_pages(
        relativeThemeUrl=task_model.theme_uri,
        fromPage=task_model.last_parsed_page,
        toPage=task_model.to_page,
        ws_clients=ws_clients,
        task_id=str(task_model.id),
    ))
    return MainResponse.success()

async def get_csv(task_id: str):
    task = models.ParseTask().get_by_id(task_id)
    aricles = Article.select().where(models.Article.theme_uri == task.theme_uri and models.Article.page >= task.from_page and models.Article.page <= task.to_page)
    df = pd.DataFrame(list(aricles.dicts()))
    stream = io.StringIO()
    df.to_csv(stream, index=False, sep='~')
    headers = {
        'Content-Disposition': 'attachment; filename="result.csv"'
    }
    return StreamingResponse(iter([stream.getvalue()]), media_type="text/csv", headers=headers)