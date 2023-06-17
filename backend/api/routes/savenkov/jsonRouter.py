from fastapi import APIRouter
from ...data.pozdnyakov.models import plot_clustering_2d, plot_clustering_count_bigrams, \
    plot_clustering_pca, plot_clustering_tsne, plot_clustering_3d

router = APIRouter(
    prefix="/savenkov/json",
    tags=["json"],
    responses={404: {"description": "Not found"}},
)


@router.get('/clustering_2d', summary='Кластеризация в 2х мерном пространстве')
async def get_clustering_2d():
    return plot_clustering_2d()


@router.get('/clustering_3d', summary='Кластеризация в 3х мерном пространстве')
async def get_clustering_3d():
    return plot_clustering_3d()


@router.get('/clustering_pca', summary='Кластеризация в c использованием PCA')
async def get_clustering_pca():
    return plot_clustering_pca()


@router.get('/clustering_tsne', summary='Кластеризация в c использованием TSNE')
async def get_clustering_tsne():
    return plot_clustering_tsne()


@router.get('/clustering_count_bigrams', summary='Кластеризация по количеству биграмм и триграмм в категории')
async def get_clustering_count_bigrams():
    return plot_clustering_count_bigrams()