<script setup>
import {RouterLink, RouterView, useRoute, useRouter} from 'vue-router'
import {provide} from "vue";

const route = useRoute()

let dev = false
let curr_api = dev ? 'http://127.0.0.1:5000' : 'https://analytics-trustyFox.pythonanywhere.com'
provide('curr_api', curr_api)

</script>

<template>
  <router-view :key="route.fullPath"/>
</template>

<style scoped>
</style>
