from ...data.bondarenko.sqlite.utils import init_database
from ...routes.bondarenko import parserRouter, websocketsRouter, tasksRouter

def init_app(fastApiApp):
    init_database()
    fastApiApp.include_router(parserRouter.router)
    fastApiApp.include_router(websocketsRouter.router)
    fastApiApp.include_router(tasksRouter.router)
