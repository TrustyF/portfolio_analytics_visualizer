<script setup>
import {computed, onMounted, provide, ref} from "vue";
import axios from "axios"
import SessionComponent from "@/components/SessionComponent.vue";

// let dev = import.meta.env.DEV
let dev = false
let curr_api = dev ? 'http://127.0.0.1:5000' : 'https://analytics-trustyFox.pythonanywhere.com'

provide('curr_api', curr_api)

let all_sessions = ref([])
// let filtered_sessions = computed(() => groupDates(sessions.value))

async function fetch_sessions() {

  const url = `${curr_api}/event/get_sessions`
  await axios.get(url)
      .then(response => {
        all_sessions.value = response.data
        console.log(response.data)
      })
}

function formatDate(date) {
  const givenDate = new Date(date);
  const today = new Date();
  const diffTime = today - givenDate;

  return Math.floor(diffTime / (1000 * 60 * 60 * 24));
}


onMounted(() => {
  fetch_sessions()
})

</script>

<template>
  <div class="wrapper" v-if="all_sessions">

<!--    <div :class="`date_wrapper `" v-for="(session,date) in filtered_sessions" :key="date">-->

<!--      <h4 v-show="formatDate(date) > 0">{{ formatDate(date) + " days ago" }}</h4>-->

      <div class="post_date_wrapper">
        <session-component v-for="session in all_sessions"
                        :data="session"
                        :key="session['sid']"/>
      </div>

<!--    </div>-->

  </div>

</template>

<style scoped>
.settings_wrapper {
  position: fixed;
  z-index: 10;
  right: 10px;
  bottom: 10px;
}

.wrapper {
  /*outline: 1px solid blue;*/
  display: flex;
  flex-flow: column wrap;
  gap: 50px;
  width: 100%;
  align-items: flex-start;
  justify-content: center;
}

.date_wrapper {
  position: relative;
  display: flex;
  flex-flow: column wrap;
  align-items: flex-start;

  gap: 20px;
  border-radius: 10px;
}

.post_date_wrapper {
  position: relative;
  display: flex;
  flex-flow: row wrap;
  align-items: flex-start;

  gap: 20px;
  border-radius: 10px;
}

.event_wrapper p {
  line-height: normal;
}

</style>
