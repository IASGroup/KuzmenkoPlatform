import pandas as pd
import os
import json

PATH = f'{os.path.dirname(os.path.abspath(__file__))}'


class Articles:
    def __init__(self):
        path = f'{PATH}/csv/files/articles.csv'
        self.__articles_df = pd.read_csv(path)

    def get_all(self) -> str:
        return self.__articles_df.to_json(orient='records', force_ascii=False)

    def get_current(self, id_article: int) -> str:
        return self.__articles_df[self.__articles_df['id'] == id_article] \
            .to_json(orient='records', force_ascii=False)

    def get_name(self, id_article: int) -> str:
        return self.__articles_df[self.__articles_df['id'] == id_article] \
            .values[0][1]

    def get_range(self, ids_article: list[int]):
        return self.__articles_df[self.__articles_df['id'].isin(ids_article)] \
            .to_json(orient='records', force_ascii=False)


class Categories:
    def __init__(self):
        path = f'{PATH}/csv/files/categories.csv'
        self.__categories_df = pd.read_csv(path)

    def get_all(self) -> str:
        return self.__categories_df.to_json(orient='records', force_ascii=False)

    def get_current(self, id_category: int) -> str:
        return self.__categories_df[self.__categories_df['id'] == id_category] \
            .to_json(orient='records', force_ascii=False)

    def get_range(self, ids_category: list[int]):
        return self.__categories_df[self.__categories_df['id'].isin(ids_category)] \
            .to_json(orient='records', force_ascii=False)


class Percentage:
    def __init__(self):
        path = f'{PATH}/csv/files/percentageBigramsArticlesInCategory.csv'
        self.__percentage_df = pd.read_csv(path)

    def get(self, id_category: int) -> str:
        category: str = self.__percentage_df[self.__percentage_df["id_category"] == id_category] \
            .values[0][1].replace("'", "\"")
        articles: list = json.loads(category)

        articles_df = Articles()

        result = [
            {
                "id_article": article.get("id_article"),
                "title": articles_df.get_name(article.get("id_article")),
                "percent": article.get("percent")
            }
            for article in articles
        ]

        return json.dumps(result, ensure_ascii=False)


def plot_clustering_2d() -> str:
    path = f'{PATH}/json/files/plot_clustering_2d.json'
    with open(path, "r") as file:
        json_data = json.load(file)

    return json.dumps(json_data)


def plot_clustering_3d() -> str:
    path = f'{PATH}/json/files/plot_clustering_3d.json'
    with open(path, "r") as file:
        json_data = json.load(file)

    return json.dumps(json_data)


def plot_clustering_count_n_grams_in_article() -> str:
    path = f'{PATH}/json/files/plot_clustering_count_n_grams_in_article.json'
    with open(path, "r") as file:
        json_data = json.load(file)

    return json.dumps(json_data)


def plot_clustering_pca() -> str:
    path = f'{PATH}/json/files/plot_clustering_pca.json'
    with open(path, "r") as file:
        json_data = json.load(file)

    return json.dumps(json_data)


def plot_clustering_tsne() -> str:
    path = f'{PATH}/json/files/plot_clustering_tsne.json'
    with open(path, "r") as file:
        json_data = json.load(file)

    return json.dumps(json_data)