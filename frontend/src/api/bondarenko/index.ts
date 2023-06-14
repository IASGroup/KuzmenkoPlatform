import axios from "axios";
import settings from "@/settings";

export type ResultResponse<T> = {
    result : T | null,
    isSuccess: boolean,
    errorMessage: string | null
}

export type MainResponse = {
    isSuccess: boolean,
    errorMessage: string | null
}

export type ParseTask = {
  id: string;
  theme_uri: string;
  theme_name: string;
  from_page: number;
  to_page: number;
  current_page: number;
  current_article: number;
  is_done: boolean;
  is_running: boolean;
};

export async function getTasks(): Promise<ResultResponse<Array<ParseTask>>> {
    return (await axios.get(`${settings.BACKEND_URL}/bondarenko/tasks`)).data;
};

export type CreateTaskRequest = {
    themeUri: string,
    themeName: string,
    fromPage: number,
    toPage: number
}

export async function createTask(request: CreateTaskRequest): Promise<ResultResponse<ParseTask>> {
    return (await axios.post(`${settings.BACKEND_URL}/bondarenko/tasks/create`, {
            theme_uri: request.themeUri,
            theme_name: request.themeName,
            from_page: request.fromPage,
            to_page: request.toPage
        }
    )).data as ResultResponse<ParseTask>;
};

export async function runTask(taskId: string): Promise<MainResponse> {
    return (await axios.post(`${settings.BACKEND_URL}/bondarenko/tasks/run/${taskId}`,)).data as MainResponse;
};

export async function stopTask(taskId: string): Promise<MainResponse> {
    return (await axios.post(`${settings.BACKEND_URL}/bondarenko/tasks/stop/${taskId}`,)).data as MainResponse;
};


export type Theme = {
    name: string,
    link: string
}

export type Group = {
    name: string,
    themes: Array<Theme>
}

export async function getGroups(): Promise<ResultResponse<Array<Group>>> {
    return (await axios.get(`${settings.BACKEND_URL}/bondarenko/cyberleninka/parser/themes`)).data as ResultResponse<Array<Group>>;
}

export async function getThemeMaxPage(themeUri: string): Promise<ResultResponse<number>> {
    return (await axios.post(`${settings.BACKEND_URL}/bondarenko/cyberleninka/parser/max-page`, {
        relativeUrl: themeUri
    })).data as ResultResponse<number>
}
