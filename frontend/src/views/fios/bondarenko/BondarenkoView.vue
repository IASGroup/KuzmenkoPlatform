<script setup lang="ts">
import { onMounted } from "vue";
import axios from "axios";
import settings from "@/settings";
import { ref } from "vue";
import { ParseTask, getTasks, runTask, stopTask, CreateTaskRequest, createTask, getGroups, Group, getThemeMaxPage } from '@/api/bondarenko';
const wsConnection = ref<WebSocket>();
const tasks = ref<Array<ParseTask>>([]);
const tasksLoading = ref<boolean>(false);

type WSParsingMessage = {
  task_id: string,
  current_article_number: number,
  all_article_number: number,
  page: number
}

type WSParsingEndMessage = {
  task_id: string
}

onMounted(async () => {
  tasksLoading.value = true;
  wsConnection.value = new WebSocket('ws://localhost:8000/bondarenko/ws');
  wsConnection.value.onmessage = (e: any) => {
    const data = JSON.parse(e.data);
    if (data.topic == 'parsing') {
      const message = JSON.parse(data.message) as WSParsingMessage;
      const findedTasks = tasks.value.filter(x => x.id == message.task_id);
      if (findedTasks.length == 1) {
        findedTasks[0].current_article = message.current_article_number;
        findedTasks[0].current_page = message.page;
      }
      console.log(message);
    } else if (data.topic == 'parsing-end') {
      const message = JSON.parse(data.message) as WSParsingEndMessage;
      const findedTasks = tasks.value.filter(x => x.id == message.task_id);
      if (findedTasks.length == 1) {
        findedTasks[0].current_article = 20;
        findedTasks[0].current_page = findedTasks[0].to_page;
        findedTasks[0].is_done = true;
        findedTasks[0].is_running = false;
      }
      console.log(message);
    }
  }

  const getTasksResponse = await getTasks();
  tasks.value = getTasksResponse.isSuccess ? getTasksResponse.result || [] : [];
  tasksLoading.value = false;
});

const createTaskDialogOpen = ref<boolean>(false);

function getTaskPagesCompletePercente(task: ParseTask): number {
  return task.is_done ? 100 : task.from_page - task.to_page != 0 ? (task.current_page - task.from_page) / (task.to_page - task.from_page) * 100 : 0
}

function getTaskArticleCompletePercente(task: ParseTask): number {
  return task.is_done ? 100 : 1 - 20 != 0 ? (task.current_article - 1) / (20 - 1) * 100 : 0
}

let groupsLoading = ref(false);
let groups = ref<Array<Group>>([]);

let selectedTheme = ref<{ name: string, link: string } | null>(null);
let newTaskStep = ref('menu');

async function selectTheme() {
  newTaskStep.value = 'selectTheme';
  selectedTheme.value = null;
  groupsLoading.value = true;
  const getGroupsResponse = await getGroups();
  groups.value = getGroupsResponse.result || [];
  await new Promise((r) => setTimeout(r, 100));
  groups.value = [
    {
      "name": "Медицинские науки",
      "themes": [
        {
          "name": "Фундаментальная медицина",
          "link": "/article/c/basic-medicine"
        },
        {
          "name": "Клиническая медицина",
          "link": "/article/c/clinical-medicine"
        },
        {
          "name": "Науки о здоровье",
          "link": "/article/c/health-sciences"
        },
        {
          "name": "Биотехнологии в медицине",
          "link": "/article/c/health-biotechnology"
        }
      ]
    },
    {
      "name": "Естественные и точные науки",
      "themes": [
        {
          "name": "Математика",
          "link": "/article/c/mathematics"
        },
        {
          "name": "Компьютерные и информационные науки",
          "link": "/article/c/computer-and-information-sciences"
        },
        {
          "name": "Физика",
          "link": "/article/c/physical-sciences"
        },
        {
          "name": "Химические науки",
          "link": "/article/c/chemical-sciences"
        },
        {
          "name": "Науки о Земле и смежные экологические науки",
          "link": "/article/c/earth-and-related-environmental-sciences"
        },
        {
          "name": "Биологические науки",
          "link": "/article/c/biological-sciences"
        }
      ]
    },
    {
      "name": "Техника и технологии",
      "themes": [
        {
          "name": "Строительство и архитектура",
          "link": "/article/c/civil-engineering"
        },
        {
          "name": "Электротехника, электронная техника, информационные технологии",
          "link": "/article/c/electrical-electronic-information-engineering"
        },
        {
          "name": "Механика и машиностроение",
          "link": "/article/c/mechanical-engineering"
        },
        {
          "name": "Химические технологии",
          "link": "/article/c/chemical-engineering"
        },
        {
          "name": "Технологии материалов",
          "link": "/article/c/materials-engineering"
        },
        {
          "name": "Медицинские технологии",
          "link": "/article/c/medical-engineering"
        },
        {
          "name": "Энергетика и рациональное природопользование",
          "link": "/article/c/environmental-engineering"
        },
        {
          "name": "Экологические биотехнологии",
          "link": "/article/c/environmental-biotechnology"
        },
        {
          "name": "Промышленные биотехнологии",
          "link": "/article/c/industrial-biotechnology"
        },
        {
          "name": "Нанотехнологии",
          "link": "/article/c/nano-technology"
        }
      ]
    },
    {
      "name": "Гуманитарные науки",
      "themes": [
        {
          "name": "История и археология",
          "link": "/article/c/history-and-archaeology"
        },
        {
          "name": "Языкознание и литературоведение",
          "link": "/article/c/languages-and-literature"
        },
        {
          "name": "Философия, этика, религиоведение",
          "link": "/article/c/philosophy-ethics-and-religion"
        },
        {
          "name": "Искусствоведение",
          "link": "/article/c/arts-history-of-arts-performing-arts-music"
        }
      ]
    },
    {
      "name": "Сельскохозяйственные науки",
      "themes": [
        {
          "name": "Сельское хозяйство, лесное хозяйство, рыбное хозяйство",
          "link": "/article/c/agriculture-forestry-and-fisheries"
        },
        {
          "name": "Животноводство и молочное дело",
          "link": "/article/c/animal-and-dairy-science"
        },
        {
          "name": "Ветеринарные науки",
          "link": "/article/c/veterinary-science"
        },
        {
          "name": "Агробиотехнологии",
          "link": "/article/c/agricultural-biotechnology"
        }
      ]
    },
    {
      "name": "Социальные науки",
      "themes": [
        {
          "name": "Психологические науки",
          "link": "/article/c/psychology"
        },
        {
          "name": "Экономика и бизнес",
          "link": "/article/c/economics-and-business"
        },
        {
          "name": "Науки об образовании",
          "link": "/article/c/educational-sciences"
        },
        {
          "name": "Социологические науки",
          "link": "/article/c/sociology"
        },
        {
          "name": "Право",
          "link": "/article/c/law"
        },
        {
          "name": "Политологические науки",
          "link": "/article/c/political-science"
        },
        {
          "name": "Социальная и экономическая география",
          "link": "/article/c/social-and-economic-geography"
        },
        {
          "name": "СМИ (медиа) и массовые коммуникации",
          "link": "/article/c/media-and-communications"
        }
      ]
    }
  ];

  groupsLoading.value = false;
};

function themeSelected(theme: { name: string, link: string }) {
  selectedTheme.value = theme;
  newTaskStep.value = 'menu';
}

let selectedPages = ref<Array<number>>([]);
let maxPageLoading = ref(false);
let maxPage = ref<number | null>(null);
let selectedRange = ref<Array<number>>([]);

async function selectPagesRange(relativeThemeUri: string) {
  maxPageLoading.value = true;
  newTaskStep.value = 'selectPages';
  selectedPages.value = [];
  const getThemeMaxPageResponse = await getThemeMaxPage(relativeThemeUri);
  maxPage.value = getThemeMaxPageResponse.result || 1;
  selectedRange.value = [1, maxPage.value];
  maxPageLoading.value = false;
}

function pagesSelected(range: Array<number>) {
  console.log(range);
  selectedPages.value = Array.from({ length: (range[1] - range[0] + 1) }, (v, k) => k + range[0]);
  newTaskStep.value = 'menu';
  console.log(selectedPages.value);
  isReadyToCreateTask.value = true;
}

let isReadyToCreateTask = ref<boolean>(false)

function resetNewTaskVariables() {
  selectedTheme.value = null;
  selectedPages.value = [];
  selectedRange.value = [];
  newTaskStep.value = 'menu';
  isReadyToCreateTask.value = false;
}

function onChangeNewTaskDialog(isOpen: boolean) {
  if (!isOpen) {
    resetNewTaskVariables();
  }
}

async function createTaskLocal(createTaskRequest: CreateTaskRequest) : Promise<ParseTask> {
  const createTaskResponse = await createTask(createTaskRequest);
  const task = createTaskResponse.result as ParseTask;
  tasks.value.push(task);
  return task;
}

async function runTaskLocal(task: ParseTask): Promise<void> {
  await runTask(task.id);
  task.is_running = true;
}

async function createAndRunTaskLocal(createTaskRequest: CreateTaskRequest) {
  const task = await createTaskLocal(createTaskRequest);
  await runTaskLocal(task);
  createTaskDialogOpen.value = false;
}

async function stopTaskLocal(task: ParseTask): Promise<void> {
  await stopTask(task.id);
  task.is_running = false;
}

async function downloadTaskCSV(task: ParseTask): Promise<void> {
  const csvResponse = await axios.get(`${settings.BACKEND_URL}/bondarenko/tasks/${task.id}/csv`);
  let blob = new Blob([csvResponse.data], { type: 'text/csv' });
  let link = document.createElement('a');
  link.href = window.URL.createObjectURL(blob);
  link.download = `${task.id}.csv`;
  link.click();
}

</script>

<template>
  <div class="bondarenko__view">
    <v-card>
      <v-layout style="min-height: 100vh;">
        <v-navigation-drawer permanent location="right">
          <v-list density="compact" nav class="text-button">
            <v-list-item disabled="true" prepend-icon="" />
            <v-divider />
            <v-list-item prepend-icon="mdi-remote-desktop" value="home">Парсинг</v-list-item>
            <v-list-item prepend-icon="mdi-sine-wave" value="account">Аналитика</v-list-item>
          </v-list>
        </v-navigation-drawer>
        <v-main>
          <v-card class="pa-6">
            <div class="card__header bg-indigo-darken-1 d-flex flex-row justify-space-between pa-4">
              <div class="text-button">Парсинг данных</div>
              <div>
                <v-dialog width="unset" v-model="createTaskDialogOpen"
                  @update:model-value="(value: boolean) => onChangeNewTaskDialog(value)">
                  <template v-slot:activator="{ props }">
                    <v-btn color="white" class="mr-3" flat v-bind="props">Новая задача</v-btn>
                  </template>
                  <v-card flat min-height="60vh" min-width="900px">
                    <v-card-title class="bg-indigo-darken-1">
                      {{ newTaskStep === 'menu' ?
                        'Создание новой задачи парсинга'
                        : newTaskStep === 'selectPages' ?
                          'Выберите диапазон страниц'
                          : 'Выберите тематику научных статей'
                      }}
                    </v-card-title>
                    <v-progress-linear :active="groupsLoading || maxPageLoading" color="indigo-darken-1" height="6"
                      indeterminate></v-progress-linear>
                    <v-timeline side="end" v-if="newTaskStep === 'menu'" class="pa-16">
                      <v-timeline-item fill-dot :dot-color="selectedTheme ? 'green' : 'orange'"
                        :icon="selectedTheme ? 'mdi-check' : 'mdi-lightning-bolt'" icon-color="white">
                        <template v-slot:opposite class="pa-0">
                          <p style="max-width: 350px; overflow-wrap: break-word;">{{ selectedTheme?.name }}</p>
                        </template>
                        <v-btn @click="selectTheme">Выбрать тему</v-btn>
                      </v-timeline-item>
                      <v-timeline-item fill-dot :dot-color="selectedPages.length !== 0 ? 'green' : 'orange'"
                        :icon="selectedPages.length !== 0 ? 'mdi-check' : 'mdi-lightning-bolt'" icon-color="white">
                        <template v-slot:opposite class="pa-0" v-if="selectedPages.length !== 0">
                          <p style="max-width: 350px; overflow-wrap: break-word;">{{ `${selectedRange[0]} →
                                                      ${selectedRange[1]}` }}</p>
                        </template>
                        <v-btn :disabled="selectedTheme == null" @click="selectPagesRange(selectedTheme!.link)">Выбрать
                          страницы</v-btn>
                      </v-timeline-item>
                    </v-timeline>
                    <div v-if="!groupsLoading && newTaskStep == 'selectTheme'" class="pa-4"
                      style="display: grid; grid-template-columns: 1fr 1fr; grid-gap: 30px;">
                      <div v-for="(group, groupKey) in groups" :key="groupKey">
                        <p class="text-button bg-indigo-darken-1 pl-5 rounded">{{ group.name }}</p>
                        <v-list>
                          <v-list-item v-for="(theme, themeKey) in group.themes" :key="themeKey">
                            <v-btn flat @click="themeSelected(theme)">{{ theme.name }}</v-btn>
                          </v-list-item>
                        </v-list>
                      </div>
                    </div>
                    <div v-if="!maxPageLoading && newTaskStep == 'selectPages'">
                      <v-row class="ma-10 pa-0 d-flex justify-space-between align-center">
                        <v-col class="pa-0 ma-0" cols="1">
                          <v-text-field class="pagesRange__field" hide-details v-model="selectedRange[0]" single-line />
                        </v-col>
                        <v-col class="pa-0 mt-0 mb-0 ml-5 mr-5">
                          <v-range-slider class="mt-5" color="indigo-darken-1" :min="1" :max="maxPage"
                            v-model="selectedRange" step="1" thumb-label="always" />
                        </v-col>
                        <v-col class="pa-0 ma-0" cols="1"><v-text-field class="pagesRange__field" hide-details
                            v-model="selectedRange[1]" /></v-col>
                      </v-row>
                    </div>
                    <v-spacer></v-spacer>
                    <v-card-actions class="ma-0 pa-0">
                      <v-btn v-if="newTaskStep === 'menu'" :disabled="!isReadyToCreateTask" height="52px" block
                        class="rounded-0" color="white" style="background-color: #3949AB;" @click="createAndRunTaskLocal({
                          themeUri: selectedTheme!.link,
                          themeName: selectedTheme!.name,
                          fromPage: selectedRange![0],
                          toPage: selectedRange![1]
                        })">
                        Создать и запустить
                      </v-btn>
                      <v-btn v-if="newTaskStep === 'selectPages'" block height="52px" class="rounded-0" color="white"
                        style="background-color: #3949AB;" @click="pagesSelected(selectedRange)">Продолжить</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </div>
            </div>
            <v-card-item>
              <p class="h-3">Список задач</p>
              <v-progress-linear v-if="tasksLoading" indeterminate color="indigo-darken-1"></v-progress-linear>
              <template v-else>
                <div v-if="tasks.length == 0" class="d-flex justify-center">
                  <p>Задачи не найдены</p>
                </div>
                <v-list v-else>
                  <v-list-item v-for="(task, key) in tasks" :key="key">
                    <div class="pa-2 align-center" style="display: grid; grid-template-columns: 20% 50% 20%; gap: 5%">
                      <div class="text-wrap">{{ task.theme_name }}</div>
                      <div style="display: grid; grid-template-columns: 25% 70%; gap: 5%;" :style="task.is_running == false ? { 'color': '#BDBDBD' } : {}">
                        <div class="d-flex flex-column align-center">
                          <div class="w-100">
                            <div class="d-flex flex-row justify-space-between" style="font-size: 0.7rem;">
                              <div>{{ 1 }}</div>
                              <div>{{ task.is_done ? 20 : task.current_article }}</div>
                              <div>{{ 20 }}</div>
                            </div>
                          </div>
                          <v-progress-linear :stream="task.is_running" :color="task.is_running ? 'indigo-darken-1' : 'grey-lighten-1'" class="mt-1 mb-1"
                            :model-value="getTaskArticleCompletePercente(task)" />
                          <div class="d-flex justify-center">загрузка статей</div>
                        </div>
                        <div class="d-flex flex-column align-center">
                          <div class="w-100">
                            <div class="d-flex flex-row justify-space-between" style="font-size: 0.7rem;">
                              <div>{{ task.from_page }}</div>
                              <div>{{ task.current_page }}</div>
                              <div>{{ task.to_page }}</div>
                            </div>
                          </div>
                          <v-progress-linear :stream="task.is_running" :color="task.is_running ? 'indigo-darken-1' : 'grey-lighten-1'" class="mt-1 mb-1"
                            :model-value="getTaskPagesCompletePercente(task)" />
                          <div class="d-flex justify-center">загрузка страниц</div>
                        </div>
                      </div>
                      <div class="pa-0 ma-0" style="display: grid; grid-gap: 20px; grid-auto-flow: column;">
                        <v-btn :disabled="task.is_done"
                          @click="task.is_running ? stopTaskLocal(task) : runTaskLocal(task)">{{ task.is_done ?
                            'Выполнена'
                            : task.is_running ? 'Остановить' : 'Запустить' }}</v-btn>
                        <v-btn @click="downloadTaskCSV(task)" :disabled="!task.is_done" :color="task.is_done ? 'green' : ''">
                          <v-icon icon="mdi-download-outline" />
                        </v-btn>
                      </div>
                    </div>
                  </v-list-item>
                </v-list>
              </template>
            </v-card-item>
          </v-card>
        </v-main>
      </v-layout>
    </v-card>
  </div>
</template>

<style>
.bondarenko__view {
  font-family: Inter, serif !important;
}

.pagesRange__field .v-field__input {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  text-align: center !important;
}</style>