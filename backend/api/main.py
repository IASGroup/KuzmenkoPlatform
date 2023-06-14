import pandas as pd
import uvicorn
from typing import Union
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from .utils.bondarenko.utils import init_app as bondarenko_init_app

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bondarenko_init_app(app)

@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)