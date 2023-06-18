<template>
  <v-card>
    <h1 class="text-center">Статистические данные по дампу википедии</h1>
    <v-card class="ml-5 mr-5 mb-5 px-5">
      <h2 class="text-center">Процентное содержание статей в категориии по биграммам</h2>
      <v-autocomplete
          class="w-100"
          clearable
          label="Выберите Категорию"
          variant="underlined"
          :items="displayedItems"
          item-title="name"
          item-value="id"
          v-model="selectedIdCategory"
      />
      <h3>Выберите группу категорий</h3>
      <v-pagination
          class="w-100"
          v-model="currentPage"
          :length="totalPages"
          @input="onPageChange"
      />
      <div id="percentageBigrams"/>
    </v-card>
    <v-spacer></v-spacer>
    <v-card class="h-50 w-100 px-5 my-10 mx-5">
      <h2 class="text-center">Кластеризация по уникальности биграмм</h2>
      <v-row class="w-100">
        <v-col class="w-50">
          <h3 class="text-center">2-х мерный вид</h3>
          <div id="clustering_2d"/>
        </v-col>
        <v-col class="w-50">
          <h3 class="text-center">3-х мерный вид</h3>
          <div id="clustering_3d"/>
        </v-col>
      </v-row>
    </v-card>
    <v-spacer></v-spacer>
    <v-card class="h-50 w-100 px-5 my-10 mx-5">
      <h2 class="text-center">Кластеризация по уникальности биграмм с использованием методов по уменьшению размерности признаков объектов</h2>
      <v-row class="w-100">
        <v-col class="w-50">
          <h3 class="text-center">PCA</h3>
          <div id="clustering_pca"/>
        </v-col>
        <v-col class="w-50">
          <h3 class="text-center">T-sne</h3>
          <div id="clustering_tsne"/>
        </v-col>
      </v-row>
    </v-card>
    <v-spacer></v-spacer>
    <v-card class="mx-5">
      <h2 class="text-center">Кластеризация по количеству биграмм и триграмм в статье</h2>
      <div id="сlustering_count_n_grams_in_article"/>
    </v-card>
  </v-card>
</template>

<script setup lang="ts">
import {onMounted, ref, watch} from 'vue';
import {
  PercentageСontentArticle,
  Category,
  getClustering2d,
  getClustering3d,
  getClusteringPca,
  getClusteringTsne,
  getClusteringCountNGramsInArticle,
  getCategories,
  getPercentage,
} from '@/api/pozdnyakov';

const itemsPerPage = 100
const selectedIdCategory = ref(0)
const displayedItems = ref<Array<Category>>([])
let categories:Array<Category> = []
let currentPage = ref(1)
let totalPages = Math.ceil(38637 / itemsPerPage)



onMounted(async () => {
  categories = JSON.parse(await getCategories()) as Category[]
  displayedItems.value = categories.slice(0,itemsPerPage)

  getClustering2d().then(value => Plotly.newPlot(document.getElementById("clustering_2d"),JSON.parse(value)))
  getClustering3d().then(value => Plotly.newPlot(document.getElementById("clustering_3d"),JSON.parse(value)))
  getClusteringPca().then(value => Plotly.newPlot(document.getElementById("clustering_pca"),JSON.parse(value)))
  getClusteringTsne().then(value => Plotly.newPlot(document.getElementById("clustering_tsne"),JSON.parse(value)))
  getClusteringCountNGramsInArticle().then(value => Plotly.newPlot(document.getElementById("сlustering_count_n_grams_in_article"),JSON.parse(value)))

})
watch(selectedIdCategory, async()=>{
  let percentageСontentArticle = JSON.parse(await getPercentage(selectedIdCategory.value)) as PercentageСontentArticle[]
  Plotly.newPlot(document.getElementById("percentageBigrams"), [{
    values: percentageСontentArticle.map(value => value.percent) as string[],
    labels: percentageСontentArticle.map(value => value.title) as string[],
    type: 'pie'
  }], {
  });
})
watch(currentPage, () => {
  updateDisplayedItems();
});
function updateDisplayedItems() {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  displayedItems.value = categories.slice(start, end);
}
function onPageChange(page: number) {
  currentPage.value = page;
}
</script>

<style scoped>

</style>