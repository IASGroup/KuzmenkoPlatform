from . import database, models
from fastapi import Depends

async def reset_db_state():
    database.db._state._state.set(database.db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()

def init_database():
    database.db.connect()
    database.db.create_tables([models.Article, models.ParseTask])
    database.db.close()