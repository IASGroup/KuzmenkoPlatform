<script setup lang="ts">
import axios from 'axios'
import { onMounted } from 'vue';
import { ref } from 'vue';

let data = ref()
let headers = ref([{}])
let rows = ref([])

onMounted(async () => {
  data = await axios.get('http://localhost:8000')
  let head = data[0]
});
</script>

<template>
  <h1>Bondarenko</h1>
</template>

<style scoped>

</style>