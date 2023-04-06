<script setup lang="ts">

import {onMounted, ref} from "vue";
import sleep from 'sleep-promise';

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

onMounted(async () => {
  for (const fio of fios) {
    await sleep(55);
    showedFios.value.push(fio);
  }
});

</script>

<template>
  <div class="home__view">
    <div class="home__content">
      <div class="about">
        <span class="about__course">Formalized models and methods</span>
        <span class="about__course">For solving analytical problems</span>
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

.about {
  display: flex;
  align-items: center;
  flex-direction: column;
  flex-wrap: wrap;
}

.about__course {
  font-size: 4.5rem;
  line-height: 4.5rem;
  letter-spacing: 0.1rem;
  font-weight: bolder;
}

.pages {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  grid-auto-rows: max-content;
  grid-column-gap: 25px;
  grid-row-gap: 25px;
}

.page__link {
  text-align: center;
  text-decoration: none;
  color: white;
  font-size: 1.7rem;
  font-weight: normal;
}

.page__link:hover {

}
</style>
