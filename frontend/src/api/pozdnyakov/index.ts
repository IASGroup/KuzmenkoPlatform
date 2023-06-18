import axios from "axios";
import settings from "@/settings";

export type PercentageСontentArticle = {
    id_article: number,
    title: string,
    percent: number
}
export type Category = {
    id: number,
    name: string
}
export async function getClustering2d(): Promise<string>{
    return (await axios.get(`${settings.BACKEND_URL}/pozdnyakov/json/clustering_2d`)).data;
}
export async function getClustering3d(): Promise<JSON>{
    return (await axios.get(`${settings.BACKEND_URL}/pozdnyakov/json/clustering_3d`)).data;
}
export async function getClusteringPca(): Promise<JSON>{
    return (await axios.get(`${settings.BACKEND_URL}/pozdnyakov/json/clustering_pca`)).data;
}

export async function getClusteringTsne(): Promise<JSON>{
    return (await axios.get(`${settings.BACKEND_URL}/pozdnyakov/json/clustering_tsne`)).data;
}
export async function getClusteringCountNGramsInArticle(): Promise<JSON>{
    return (await axios.get(`${settings.BACKEND_URL}/pozdnyakov/json/clustering_count_n_grams_in_article`)).data;
}
export async function getCategories(): Promise<string>{
    return (await axios.get(`${settings.BACKEND_URL}/pozdnyakov/csv/categories`)).data;
}

export async function getPercentage(id_category: number): Promise<string>{
    return (await axios.get(`${settings.BACKEND_URL}/pozdnyakov/csv/percentage/${id_category}`)).data;
}
