import pandas as pd
import uvicorn
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def getdata():
    data = pd.read_csv('../api/data/bondarenko/somedata.csv')
    return data.to_json()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)