import pandas as pd
import uvicorn
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def getdata():
    data = pd.read_csv('backend/api/data/bondarenko/somedata.csv')
    return data.to_json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)