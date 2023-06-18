import os
import pathlib
from ...data.bondarenko.sqlite.utils import init_database
from ...routes.bondarenko import parserRouter, websocketsRouter, tasksRouter

def init_app(fastApiApp):
    path = f'{pathlib.Path(__file__).parent.parent.parent}/data/bondarenko/sqlite/database'
    if not os.path.exists(path):
        os.mkdir(path)
    init_database()
    fastApiApp.include_router(parserRouter.router)
    fastApiApp.include_router(websocketsRouter.router)
    fastApiApp.include_router(tasksRouter.router)
