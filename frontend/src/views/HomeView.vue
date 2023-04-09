<script setup lang="ts">

import {onMounted, ref} from "vue";
import sleep from 'sleep-promise';
import { useLocalStorage } from "@vueuse/core"

const lastShowDate = useLocalStorage("lastShowDate", new Date());
const fios: Array<string> = [
  "Babayev",
  "Bondarenko",
  "Vasiliev",
  "Gulak",
  "Ivanin",
  "Kolotvin",
  "Levkin",
  "Lisovsky",
  "Pozdnyakov",
  "Roopsey",
  "Savenkov",
  "Smirnov",
  "Stuzhny",
  "Sunnitsa",
  "Tolkachev",
  "Telepnev",
];

const showedFios = ref<Array<string>>([]);

const aboutTextHeaders = [
    "Formalized models and methods",
    "For solving analytical problems"
]

const showedAboutTextHeaders = ref<Array<string>>([]);

onMounted(async () => {
  await homeAnimation();
});

async function homeAnimation () {
  for (const about of aboutTextHeaders) {
    await sleep(750);
    showedAboutTextHeaders.value.push(about);
  }
  await sleep(600);
  for (const fio of fios) {
    await sleep(55);
    showedFios.value.push(fio);
  }
}

</script>

<template>
  <div class="home__view">
    <div class="home__content">
      <div class="about">
        <transition-group name="about__list">
          <span class="about__course"
                v-for="(about, i) in showedAboutTextHeaders"
                :key="i"
          >
          {{about}}
        </span>
        </transition-group>
      </div>
      <div class="pages">
        <TransitionGroup name="pages__list">
          <router-link
              class="page__link"
              v-for="(fio, i) in showedFios"
              :key="i"
              :to="fio.toLowerCase()"
          >
            {{ fio }}
          </router-link>
        </TransitionGroup>
      </div>
    </div>
  </div>
</template>

<style scoped>

.home__view {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #202124;
  min-height: 100vh;
  color: white;
  font-family: Inter, serif;
}

.home__content {
  display: grid;
  grid-row-gap: 120px;
  padding: 120px 0 120px 0;
}

.pages__list-enter-active,
.pages__list-leave-active {
  transition: all 0.5s ease;
}

.pages__list-enter-from,
.pages__list-leave-to {
  opacity: 0;
  transform: translateY(50px);
}


.about__list-enter-active,
.about__list-leave-active {
  transition: all 0.9s ease;
}

.about__list-enter-from,
.about__list-leave-to {
  opacity: 0;
  transform: translateY(-50px);
}

.about {
  display: flex;
  align-items: center;
  flex-direction: column;
  flex-wrap: wrap;
}

.about__course {
  font-size: 4.5rem;
  line-height: 5rem;
  letter-spacing: 0.2rem;
  font-weight: bolder;
}

.pages {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  grid-auto-rows: max-content;
  grid-column-gap: 0px;
  grid-row-gap: 25px;
}

.page__link {
  text-align: center;
  text-decoration: none;
  color: white;
  font-size: 1.7rem;
  font-weight: normal;
}
</style>
