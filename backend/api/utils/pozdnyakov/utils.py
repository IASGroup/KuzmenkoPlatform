from ...routes.pozdnyakov import csvRouter
from ...routes.pozdnyakov import jsonRouter


def init_app(fastApiApp):
    fastApiApp.include_router(csvRouter.router)
    fastApiApp.include_router(jsonRouter.router)
