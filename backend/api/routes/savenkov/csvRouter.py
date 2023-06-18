from fastapi import APIRouter
from ...data.savenkov.models import Articles, Percentage, Categories

router = APIRouter(
    prefix="/savenkov/csv",
    tags=["csv"],
    responses={404: {"description": "Not found"}},
)

@router.get('/categories', summary='Получить все наименования категорий')
async def get_categories():
    categories = Categories()
    return categories.get_all()

@router.get('/percentage/{id_category}', summary='Процентное содержание триграмм в категории')
async def get_percentage(id_category: int):
    percentage = Percentage()
    return percentage.get(id_category)