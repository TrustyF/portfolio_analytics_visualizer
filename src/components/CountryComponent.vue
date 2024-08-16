<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps({
  country: {
    type: String,
    default: null,
  },
});

async function getCountryCode(name) {

  if (!name || !name.length > 0 || name === '/') return name

  return fetch(`https://restcountries.com/v3.1/name/${name.split('/')[0]}`).then(resp => resp.json())
      .then(json => json[0]['flag'])
      .catch(error => name)
}

let icon = ref('')

async function set_val() {
  icon.value = await getCountryCode(props.country)
}

onMounted(() => {
  set_val()
})
</script>

<template>
  <div class="country_wrapper">
    <h4>{{ icon }}</h4>
    <h3 style="white-space: nowrap;">{{ country.split('/')[1] }}</h3>
  </div>
</template>

<style scoped>
.country_wrapper {
  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  justify-content: center;
  gap: 10px;
  overflow: hidden;
  font-size: 1em;
}

.country_wrapper h4 {
  font-size: 2em;
}
</style>