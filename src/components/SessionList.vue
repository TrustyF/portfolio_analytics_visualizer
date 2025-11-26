<script setup>

let props = defineProps({'components': {type: Array, default: () => []},});
let emits = defineEmits(["test"]);

import { ref, onMounted } from 'vue'

const sessions = ref([])

onMounted(async () => {
  // Fetch session list from backend
  const res = await fetch('/sessions') // returns array of session IDs
  sessions.value = await res.json()
})

</script>

<template>
  <div></div>
</template>

<style scoped>

</style>