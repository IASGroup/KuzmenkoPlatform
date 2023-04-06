<script setup lang="ts">

const courses = [
  "19-IAS"
];

const fios = [
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
</script>

<template>
  <div class="home__view">
    <div class="home__content">
      <div class="about">
        <span class="about__course">Formalized models and methods</span>
        <span class="about__course">for solving analytical problems</span>
      </div>
      <div class="courses" v-for="(course, i) in courses" :key="i">
        <span class="courses__name">{{ course }}</span>
        <div class="pages">
          <router-link class="page__link" v-for="(fio, i) in fios" :key="i"
                       :to="fio.toLowerCase()">
            {{ fio }}
          </router-link>
        </div>
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
  padding-top: 50px;
}

.home__content {
  background-color: #2d2e33;
  padding: 150px 30px 150px 30px;
  border-radius: 50px;
}

.about {
  display: flex;
  align-items: center;
  flex-direction: column;
  flex-wrap: wrap;
  width: 50vw;
  margin-bottom: 100px;
}

.about__course {
  font-size: 3.5rem;
  line-height: 3.5rem;
}

.courses {
  display: grid;
  grid-row-gap: 5px;
  width: 50vw;
}

.courses__name {
  font-size: 1.7rem;
  max-width: fit-content !important;
}

.pages {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  grid-auto-rows: max-content;
  grid-column-gap: 25px;
  grid-row-gap: 20px;
}

.page__link {
  text-decoration: none;
  color: white;
  font-size: 1.6rem;
}
</style>
