from fastapi import APIRouter
from urllib3 import request

router = APIRouter(
    prefix="/clusterization",
    tags=["clusterization"],
    responses={404: {"description": "Not found"}},
)

@router.get('')
async def read_users():
    return request('GET', 'https://www.elibrary.ru/item.asp?id=21666593')
