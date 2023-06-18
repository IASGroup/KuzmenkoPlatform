from ...routes.savenkov import csvRouter
from ...routes.savenkov import jsonRouter


def init_app(fastApiApp):
    fastApiApp.include_router(csvRouter.router)
    fastApiApp.include_router(jsonRouter.router)
