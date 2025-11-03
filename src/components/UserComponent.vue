<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import axios from "axios";
import {parse_seconds} from "@/helpers.js";
import CountryComponent from "@/components/CountryComponent.vue";
import {clickOutSide as vClickOutSide} from '@mahdikhashan/vue3-click-outside'
import AtlasIconComponent from "@/components/AtlasIconComponent.vue";

let props = defineProps({
  data: Object, date: String
});
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

let events_collapsed = ref(true)
let is_events_hidden = inject('is_events_hidden')

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

function formatTitle(event) {
  // console.log(JSON.parse(JSON.stringify(event)))

  if (['youtube_pause', 'vimeo_pause'].includes(event['name'])) return parse_seconds(Math.round(event['info']))

  if (event['name'] === 'expanded' && event['source'] === 'houdini_icons') return event['info'].split('_')[1]

  return event['info']
}

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
    'expanded': 'bi-hand-index-thumb-fill',
    'search': 'bi-search',
    'search_use': 'bi-search',
    'icon only': 'bi-gear-fill',
    'icon scale': 'bi-gear-fill',
    'copied': 'bi-copy',
    'downloaded_svg': 'bi-download',
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
    'icon only': `hsla(220,${sat},${bright},${opacity})`,
    'icon scale': `hsla(220,${sat},${bright},${opacity})`,
    'copied': `hsla(40,${sat},${bright},${opacity})`,
    'downloaded_svg': `hsla(0,${sat},${bright},${opacity})`,
  }

  return convert_table[event_name]

}

function format_date(date) {
  return new Date(date + 'Z').toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
}

function formatDate(date) {
  const givenDate = new Date(date);
  const today = new Date();
  const diffTime = today - givenDate;

  return Math.floor(diffTime / (1000 * 60 * 60 * 24));
}

function toggleCollapse() {
  events_collapsed.value = !events_collapsed.value
}

function clickOutside() {
  if (!events_collapsed.value) {
    events_collapsed.value = true
  }
}

function groupEvents(events) {

  const result = [];
  for (let i = 0; i < events.length; i++) {
    const currentEvent = events[i];
    for (let j = i + 1; j < events.length; j++) {
      const nextEvent = events[j];
      if (currentEvent.type === nextEvent.type && currentEvent.diff < 15) {
        currentEvent.diff += nextEvent.diff;
        currentEvent.info += `, ${nextEvent.info}`;
        currentEvent.timestamps = currentEvent.timestamps || [currentEvent.timestamp];
        currentEvent.timestamps.push(nextEvent.timestamp);
        events.splice(j, 1);
        j--; // Adjust index due to removal
      }
    }
    result.push(currentEvent);
  }
  return result;
}

</script>

<template>

  <div class="user_wrapper">

    <div class="new_badge bi-patch-exclamation-fill" v-show="formatDate(date) < 1"></div>

    <country-component :class="`${data['events'].length > 0 ? 'clickable':''}`" :data="data" @click="toggleCollapse"
                       v-click-out-side="clickOutside"/>

    <div class="user_feed" v-if="data['events'].length > 0" v-show="!events_collapsed || !is_events_hidden">

      <div v-for="(event,index) in data['events']" :key="event['timestamp']">

        <div class="event_wrapper" :style="`background-color:${event_to_color(event)};`">

          <p :class="`${event_to_icon(event)} event_icon`"
             :style="`font-size: 0.8em;background-color:${event_to_color(event)};`"/>

          <atlas-icon-component :at_id="event.atlas_index"/>

          <p class="event_title">{{ formatTitle(event) }}</p>

        </div>

        <div class="time_dots" v-show="event['diff'] > 5 && data['events'][index+1]">
          <div class="t_dot" v-for="index in parseInt(Math.min(Math.max(3,(event['diff']/5)),10))"
               :key="'dot_time_'+index"/>
        </div>

      </div>
    </div>

    <div class="bi-trash3-fill delete">
      <div class="click_padding" @click="delete_uid(data['uid'])"/>
    </div>

  </div>
</template>

<style scoped>

.user_wrapper {
  position: relative;
  display: flex;
  flex-flow: row wrap;
  gap: 10px;
  background-color: #282828;

  justify-content: center;

  /*padding: 5px;*/
  border-radius: 13px;
  width: 260px;
}

.new_badge {
  color: hsl(400, 70%, 50%);
  position: absolute;
  font-size: 1.3em;
  left: -10px;
  top: -15px;
  text-shadow: 2px 2px 1px rgba(0, 0, 0, 0.5);
  z-index: 10;
}

.user_feed {
  /*outline: 1px solid red;*/
  position: relative;
  display: flex;
  flex-flow: column;
  width: 100%;
  gap: 5px;

  /*width: 95%;*/
  max-height: 800px;
  padding: 30px;
  margin-top: -10px;
  overflow-y: scroll;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}

.user_wrapper:hover .delete {
  opacity: 1;
  visibility: visible;
}

.clickable {
  cursor: pointer;
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
  width: 100%;
  /*padding: 10px;*/
  /*text-align: center;*/
  border-radius: 10px;
  display: flex;
  flex-flow: row;
  align-items: center;

  padding: 0;
  gap: 10px;
  min-height: 30px;
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
  white-space: wrap;
  word-break: break-all;

  gap: 10px;
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

.time_title {
  font-size: 0.7em;
  line-height: 0.7em;
  margin-left: 3px;
  white-space: nowrap;
  /*outline: 1px solid orange;*/
}

.event_icon {
  display: flex;
  flex-flow: column;
  justify-content: center;
  border-radius: 10px;
  padding: 10px;
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
  /*border-radius: 20px;*/
  height: fit-content;
  /*background-color: #383838;*/
  padding: 0 5px 0 0;
}

.completed {
  background-color: hsla(160, 100%, 50%, 0.25)
}

</style>