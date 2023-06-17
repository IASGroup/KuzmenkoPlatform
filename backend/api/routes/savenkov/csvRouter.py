from fastapi import APIRouter
from ...data.savenkov.models import Articles, Percentage, Categories

router = APIRouter(
    prefix="/savenkov/csv",
    tags=["csv"],
    responses={404: {"description": "Not found"}},
)


@router.get('/articles', summary='Получить все наименования статей')
async def get_themes():
    articles = Articles()
    return articles.get_all()


@router.get('/article', summary='Получить наименование конкретной статьи')
async def get_current_themes(id_article: int):
    articles = Articles()
    return articles.get_current(id_article)


@router.post('/article_range', summary='Получить наименования статей в диапазоне')
async def get_range_themes(ids_article: list[int]):
    articles = Articles()
    return articles.get_range(ids_article)


@router.get('/categories', summary='Получить все наименования категорий')
async def get_categories():
    categories = Categories()
    return categories.get_all()


@router.get('/category', summary='Получить наименование конкретной категорий')
async def get_category(id_category: int):
    categories = Categories()
    return categories.get_current(id_category)


@router.post('/category_range', summary='Получить наименования категорий в диапазоне')
async def get_range_categories(ids_category: list[int]):
    categories = Categories()
    return categories.get_range(ids_category)


@router.get('/percentage', summary='Процентное содержание триграмм в категории')
async def get_percentage(id_category: int):
    percentage = Percentage()
    return percentage.get(id_category)