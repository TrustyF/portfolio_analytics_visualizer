<script setup>
import CountryComponent from "@/components/CountryComponent.vue";
import {computed, onMounted, ref} from "vue";
import axios from "axios"
import ToggleComponent from "@/components/ToggleComponent.vue";
import {parse_seconds} from "@/helpers.js";

// let dev = import.meta.env.DEV
let dev = false
let curr_api = dev ? 'http://127.0.0.1:5000' : 'https://analytics-trustyFox.pythonanywhere.com'

let event_loading = ref("unloaded")

let is_0_event_hidden = ref(true)
let is_yale_event_hidden = ref(true)
let day_range = ref(15)

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
    'anchor_in_view': 'bi-mouse',
    'image_nav': 'bi-image',
    'expanded': 'bi-hand-index-thumb',
    'search': 'bi-search',
    'search_use': 'bi-search',
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
    'search': `hsla(350,${sat},${bright},${opacity})`,
    'search_use': `hsla(350,${sat},${bright},${opacity})`,
    'expanded': `hsla(100,${sat},${bright},${opacity})`,
  }

  return convert_table[event_name]

}

function format_date(date) {
  return new Date(date + 'Z').toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
}

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

function formatTitle(event) {
  // console.log(JSON.parse(JSON.stringify(event)))

  if (['youtube_pause', 'vimeo_pause'].includes(event['name'])) return parse_seconds(Math.round(event['info']))

  if (event['name'] === 'return_arrow') return 'return arrow'

  return event['info']
}

function formatDate(date) {
  const givenDate = new Date(date);
  const today = new Date();
  const diffTime = today - givenDate;

  return Math.floor(diffTime / (1000 * 60 * 60 * 24));
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
    <toggle-component title="hide yaletown event" :def="is_yale_event_hidden" @toggle="is_yale_event_hidden=$event"/>
    <label for="day_range" style="margin-right: 10px;display: inline-block;width: 20px">{{ day_range }}</label>
    <input id="day_range" style="" type="range" step="1" min="0" max="50" v-model="day_range">
  </div>

  <div class="spinner-border" v-if="event_loading==='loading'" role="status"/>

  <div class="wrapper" v-if="Object.keys(filtered_events).length > 0">

    <div :class="`date_wrapper `" v-for="(users,date) in filtered_events" :key="date">

      <h4 v-show="formatDate(date) > 0">{{ formatDate(date) + " days ago" }}</h4>

      <div class="post_date_wrapper">
        <div class="user_wrapper" v-for="data in sortedUsers(users)" :key="data['uid']" :id="`user_${data['uid']}`"
             v-show="is_0_event_hidden ? data['total_time']>0 : true">

          <div class="new_badge bi-patch-exclamation-fill" v-show="formatDate(date) < 1"></div>

          <country-component :data="data"/>

          <div class="user_feed" v-if="data['events'].length > 0">
            <div v-for="(event,index) in data['events']" :key="event['timestamp']">

              <div class="event_wrapper" :style="`background-color:${event_to_color(event)};`">
                <p :class="`${event_to_icon(event)} event_icon`"
                   :style="`font-size: 1em;background-color:${event_to_color(event)};`"/>

                <p class="event_title">{{ formatTitle(event) }}</p>

                <div :class="`time_sep ${event['diff']>60 && event['info']==='id: 998917047' ? 'completed':''}`"
                >
                  <h4 class="time_title">{{ parse_seconds(Math.round(event['diff'])) }}</h4>
                  <div class="bi-clock-history" style="font-size: 0.7em;line-height: 0.7em"></div>
                </div>

              </div>

              <div class="time_dots" v-show="event['diff'] > 5 && data['events'][index+1]">
                <div class="t_dot" v-for="index in parseInt(Math.min(Math.max(3,(event['diff']/5)),15))"
                     :key="'dot_time_'+index"/>
              </div>

            </div>
          </div>

          <div class="bi-trash3-fill delete">
            <div class="click_padding" @click="delete_uid(data['uid'])"/>
          </div>

        </div>
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

.new_badge {
  color: hsl(400, 70%, 50%);
  position: absolute;
  font-size: 1.5em;
  left: -10px;
  top: -15px;
  text-shadow: 2px 2px 1px rgba(0, 0, 0, 0.60);
}

.user_feed {
  /*outline: 1px solid red;*/
  position: relative;
  display: flex;
  flex-flow: column;
  align-content: flex-start;
  gap: 5px;

  width: 100%;
  max-height: 400px;
  padding: 3px;
  overflow-y: scroll;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
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
  transform: translate(-50%, -50%);
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
  box-shadow: 2px 2px 1px rgba(0, 0, 0, 0.3);
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

.time_dots {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-flow: column;
  z-index: -1;
  gap: 5px;
  margin: 0 0 -5px 0;
}

.t_dot {
  width: 2px;
  height: 2px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.1);
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
