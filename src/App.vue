<script setup>
import {computed, onMounted, provide, ref} from "vue";
import axios from "axios"
import ToggleComponent from "@/components/ToggleComponent.vue";
import {parse_seconds} from "@/helpers.js";
import UserComponent from "@/components/UserComponent.vue";

// let dev = import.meta.env.DEV
let dev = false
let curr_api = dev ? 'http://127.0.0.1:5000' : 'https://analytics-trustyFox.pythonanywhere.com'

provide('curr_api',curr_api)

let event_loading = ref("unloaded")

let is_0_event_hidden = ref(true)
let is_yale_event_hidden = ref(true)
let day_range = ref(25)

let events = ref([])
let filtered_events = computed(() => groupDates(events.value))

async function fetch_events() {

  event_loading.value = "loading"
  const url = `${curr_api}/event/get`
  const params = {}

  events.value = await axios.get(url, {params: params})
      .then(response => response.data)

  event_loading.value = "loaded"
  console.log('loaded', events.value)

}

function groupDates(arr) {
  arr.sort((a, b) => new Date(b['date']) - new Date(a['date']))

  const yesterday = new Date()
  yesterday.setDate(new Date().getDate() - day_range.value)

  arr = arr.filter(item => new Date(item['date']) > yesterday)
  if (is_yale_event_hidden.value) arr = arr.filter(item => item['geo']['zipcode'] !== 'V6Z')

  const reduced = arr.reduce((acc, item) => {
    const date = item.date;
    if (!acc[date]) {
      acc[date] = [];
    }
    acc[date].push(item);
    return acc;
  }, {});

  return reduced
}

function sortedUsers(arr) {
  arr.sort((a, b) => {
    return new Date(b['first_touch']) - new Date(a['first_touch'])
  })
  return arr
}


function formatDate(date) {
  const givenDate = new Date(date);
  const today = new Date();
  const diffTime = today - givenDate;

  return Math.floor(diffTime / (1000 * 60 * 60 * 24));
}


onMounted(() => {
  fetch_events()
})

</script>

<template>

  <div class="settings_wrapper">
    <toggle-component title="hide 0 event" :def="is_0_event_hidden" @toggle="is_0_event_hidden=$event"/>
    <toggle-component title="hide yaletown event" :def="is_yale_event_hidden" @toggle="is_yale_event_hidden=$event"/>
    <label for="day_range" style="margin-right: 10px;display: inline-block;width: 20px">{{ day_range }}</label>
    <input id="day_range" style="" type="range" step="1" min="0" max="50" v-model="day_range">
  </div>

  <div class="spinner-border" v-if="event_loading==='loading'" role="status"/>

  <div class="wrapper" v-if="Object.keys(filtered_events).length > 0">

    <div :class="`date_wrapper `" v-for="(users,date) in filtered_events" :key="date">

      <h4 v-show="formatDate(date) > 0">{{ formatDate(date) + " days ago" }}</h4>

      <div class="post_date_wrapper">
        <user-component :data="user_data"
                        :date="date"
                        v-for="user_data in sortedUsers(users)"
                        :key="user_data['uid']"
                        :id="`user_${user_data['uid']}`"
                        v-show="is_0_event_hidden ? user_data['total_time']>0 : true"/>
      </div>

    </div>

  </div>

  <div v-else-if="event_loading==='loaded'">
    <h4>No new events</h4>
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
