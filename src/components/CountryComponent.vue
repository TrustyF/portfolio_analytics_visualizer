<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps({
  country: {
    type: String,
    default: null,
  },
});

async function getCountryCode(name) {

  if (!name || !name.length > 0 || name === '/') return null

  return fetch(`https://restcountries.com/v3.1/name/${name.split('/')[0]}`).then(resp => resp.json())
      .then(json => json[0]['flags']['svg'])
      .catch(error => null)
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
  <div class="country_wrapper" v-if="icon">
    <img :src="icon" alt="country" class="flag">
    <h3 style="white-space: nowrap;">{{ country.split('/')[1] }}</h3>
  </div>
</template>

<style scoped>
.country_wrapper {
  /*color: white;*/
  display: flex;
  flex-flow: row;
  width: 100%;
  align-items: center;
  justify-content: flex-start;

  gap: 10px;
  padding: 10px;
  background-color: #383838;
  border-radius: 10px;
}
.country_wrapper h3 {
  font-weight: 900;
  font-size: 0.9em;
}
.flag {
  height: 15px;
}
</style>