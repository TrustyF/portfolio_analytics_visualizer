<script setup>
import CountryComponent from "@/components/CountryComponent.vue";
import {onMounted, ref} from "vue";
import axios from "axios"
import ToggleComponent from "@/components/ToggleComponent.vue";
import {parse_seconds} from "@/helpers.js";

let dev = import.meta.env.DEV
// let dev = true
let curr_api = dev ? 'http://192.168.1.11:5000' : 'https://analytics-trustyFox.pythonanywhere.com'

let is_0_event_hidden = ref(true)

function event_to_icon(event) {

  let event_name = event['name']

  let convert_table = {
    'page_nav': 'bi-arrow-right',
    'vimeo_play': 'bi-play-fill',
    'vimeo_pause': 'bi-pause-fill',
    'youtube_play': 'bi-play-fill',
    'youtube_pause': 'bi-pause-fill',
    'filter_use': 'bi-funnel',
    'return_arrow': 'bi-arrow-90deg-left',
    'up_arrow': 'bi-arrow-90deg-up',
    'open_new_tab': 'bi-arrow-up-right-square',
    'page_leave': 'bi-door-open',
    'open_movie': 'bi-film',
    'anchor_in_view': 'bi-arrow-down',
    'image_nav': 'bi-image',
  }

  if (event['info'].split(' ').includes('outside,')) return 'bi-house-door'

  return convert_table[event_name]
}

function event_to_color(event) {
  let event_name = event['name']

  let opacity = 0.15;
  let sat = '100%';
  let bright = '50%';

  let convert_table = {
    'page_nav': `hsla(160, ${sat}, ${bright},${opacity})`,
    'vimeo_play': `hsla(50,${sat},${bright},${opacity})`,
    'vimeo_pause': `hsla(35,${sat},${bright},${opacity})`,
    'youtube_play': `hsla(50,${sat},${bright},${opacity})`,
    'youtube_pause': `hsla(35,${sat},${bright},${opacity})`,
    'filter_use': `hsla(312,${sat},${bright},${opacity})`,
    'return_arrow': `hsla(118,${sat},${bright},${opacity})`,
    'up_arrow': `hsla(118,${sat},${bright},${opacity})`,
    'open_new_tab': `hsla(182,${sat},${bright},${opacity})`,
    'page_leave': `hsla(0,${sat},${bright},${opacity})`,
    'open_movie': `hsla(20,${sat},${bright},${opacity})`,
    'anchor_in_view': `hsla(100,${sat},${bright},${opacity})`,
    'image_nav': `hsla(200,${sat},${bright},${opacity})`,
  }

  return convert_table[event_name]

}

function format_date(date) {
  return new Date(date + 'Z').toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
}

let events = ref()

async function fetch_events() {
  const url = `${curr_api}/event/get`
  const params = {}

  events.value = await axios.get(url, {params: params})
      .then(response => response.data)
  console.log(JSON.parse(JSON.stringify(events.value)))
}

function sortEventDates(arr) {
  let objects = Object.values(arr)
  return objects.sort((a, b) => new Date(b['events'][0]['timestamp']) - new Date(a['events'][0]['timestamp']))
}

function sortDates(arr) {
  if (arr === undefined) {
    return arr
  }

  let keys = Object.keys(arr).sort((a, b) => new Date(b) - new Date(a))
  return keys.reduce((sortedObj, key) => {
    sortedObj[key] = arr[key];
    return sortedObj;
  }, {});

}

function formatTitle(event) {
  // console.log(JSON.parse(JSON.stringify(event)))

  if (['youtube_pause', 'vimeo_pause'].includes(event['name'])) return parse_seconds(Math.round(event['info']))

  if (event['name'] === 'return_arrow') return 'return arrow'

  return event['info']
}

function formatDate(date) {
  let form = date.split('-')
  return `${form[2]}/${form[1]}/${form[0]}`
}

async function delete_uid(uid) {
  const url = `${curr_api}/event/delete`
  console.log(uid)
  const params = {
    user_id: uid
  }

  const result = await axios.delete(url, {params: params})
      .then(response => response.data.success)

  if (result) {
    window.document.getElementById(`user_${uid}`).remove()
  }
}

onMounted(() => {
  fetch_events()
})

</script>

<template>

  <div class="settings_wrapper">
    <toggle-component title="hide 0 event" :def="is_0_event_hidden" @toggle="is_0_event_hidden=$event"/>
  </div>

  <div class="wrapper">
    <div :class="`date_wrapper `" v-for="(users,date) in sortDates(events)" :key="date">
      <h4 style="position: absolute;top: -30px">{{ formatDate(date) }}</h4>

      <div class="user_wrapper" v-for="data in sortEventDates(users)" :key="data['uid']" :id="`user_${data['uid']}`"
           v-show="is_0_event_hidden ? data['total_time']>0 : true">

        <country-component :data="data" :time="format_date(data['events'][0]['timestamp'])"/>

        <div class="user_feed">
          <div class="event_wrapper" :style="`background-color:${event_to_color(event)};
              padding-bottom:${event['diff']>20 ? event['diff']*2 : 0}px`"
               v-for="(event) in data['events']" :key="event['timestamp']">

            <p :class="`${event_to_icon(event)} event_icon`"
               :style="`font-size: 1em;background-color:${event_to_color(event)};`"/>

            <p class="event_title">{{ formatTitle(event) }}</p>

            <div :class="`time_sep ${event['diff']>60 && event['info']==='id: 998917047' ? 'completed':''}`"
                 >
              <h4 class="time_title">{{ parse_seconds(Math.round(event['diff'])) }}</h4>
              <div class="bi-clock-history" style="font-size: 0.7em;line-height: 0.7em"></div>
            </div>

          </div>
        </div>

        <div class="bi-trash3-fill delete">
          <div class="click_padding" @click="delete_uid(data['uid'])"/>
        </div>

      </div>

    </div>
  </div>
</template>

<style scoped>
.settings_wrapper {
  position: absolute;
  right: 10px;
  top: 10px;
}

.wrapper {
  /*outline: 1px solid blue;*/
  display: flex;
  flex-flow: column wrap;
  gap: 50px;
  width: 100%;
  margin-top: 10px;
}

.date_wrapper {
  position: relative;
  display: flex;
  flex-flow: row wrap;
  align-items: flex-start;
  /*justify-content: flex-end;*/

  margin-top: 30px;
  gap: 20px;
  border: 1px solid #282828;
  padding: 10px;
  border-radius: 10px;
}

.source_wrapper {
  position: relative;
  /*outline: 1px solid orange;*/
  display: flex;
  flex-flow: column;

  gap: 10px;
  border: 1px solid #282828;
  padding: 10px;
  border-radius: 10px;
}

.user_wrapper {
  position: relative;
  display: flex;
  flex-flow: row wrap;
  gap: 10px;
  background-color: #282828;

  padding: 15px;
  border-radius: 20px;
  width: 260px;
}

.user_feed {
  /*outline: 1px solid red;*/
  position: relative;
  display: flex;
  flex-flow: row wrap;
  align-content: flex-start;
  gap: 10px;

  width: 100%;
  max-height: 300px;
  overflow: scroll;
}
.user_wrapper:hover .delete {
  opacity: 1;
  visibility: visible;
}
.delete {
  position: absolute;
  right: -8px;
  top: -2px;
  font-size: 0.9em;
  line-height: 0.9em;
  padding: 5px;
  border-radius: 50%;
  background-color: #383838;
  /*color: #484848;*/
  transition: 200ms ease;
  opacity: 0;
  visibility: hidden;
}

.click_padding {
  z-index: 10;
  position: absolute;
  /*outline: 1px solid red;*/
  cursor: pointer;
  left: 50%;
  top: 50%;
  transform: translate(-50%,-50%);
  padding: 20px;
}

.event_wrapper {
  position: relative;
  /*padding: 10px;*/
  text-align: center;
  border-radius: 15px;
  /*display: flex;*/
  /*flex-flow: row nowrap;*/
  display: grid;
  grid-template-columns: 1fr 5fr 1fr;
  align-items: center;

  gap: 10px;
  width: 100%;
  height: 30px;
}

.event_wrapper p {
  line-height: normal;
}

.event_title {
  text-align: left;
  line-height: 1;
  font-size: 0.7em;
  color: #d5d5d5;

  margin-top: auto;
  margin-bottom: auto;

  display: block;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;

  gap: 10px;
}

.event_icon {
  display: flex;
  flex-flow: column;
  justify-content: center;
  border-radius: 15px;
  aspect-ratio: 1;
  color: white;
  height: 100%;
}

.time_sep {
  /*outline: 1px solid red;*/
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 5px;
  border-radius: 20px;
  height: fit-content;
  /*background-color: #383838;*/
  padding: 5px;
}

.completed {
  background-color: hsla(160, 100%, 50%, 0.25)
}

.time_title {
  font-size: 0.7em;
  line-height: 0.7em;
  margin-left: 3px;
  white-space: nowrap;
  /*outline: 1px solid orange;*/
}
</style>
