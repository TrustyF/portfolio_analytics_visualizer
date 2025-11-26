<script setup>
import {RouterLink, RouterView, useRoute, useRouter} from 'vue-router'
const route = useRoute()
</script>

<template>
<router-view :key="route.fullPath" />
</template>

<style scoped>
</style>
