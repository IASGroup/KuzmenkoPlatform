<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
</script>

<style>

html {
  overflow-y: auto !important;
}

@font-face {
  font-family: "Inter";
  font-style: normal;
  font-display: auto;
  src: local("Inter"), url("public/fonts/inter/Inter-VariableFont_slnt,wght.ttf") format("truetype");
}
</style>
