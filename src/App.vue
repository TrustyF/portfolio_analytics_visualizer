<script setup>
import CountryComponent from "@/components/CountryComponent.vue";
import {computed, onBeforeUnmount, onMounted, ref} from "vue";
import DeviceComponent from "@/components/DeviceComponent.vue";
import axios from "axios"
import HeaderComponent from "@/components/HeaderComponent.vue";

let dev = import.meta.env.DEV
let curr_api = dev ? 'http://192.168.1.11:5000' : 'https://analytics-trustyFox.pythonanywhere.com'

function parse_seconds(time) {
  let min = Math.floor(time / 60);
  let sec = time % 60;

  if (min > 10) return '+10'

  return String(min) + ':' + String(sec).padStart(2, '0');
}

function event_to_icon(event) {

  let event_name = event['name']

  let convert_table = {
    'page_nav': 'bi-arrow-right',
    'vimeo_play': 'bi-play-fill',
    'vimeo_pause': 'bi-pause-fill',
    'filter_use': 'bi-funnel',
    'return_arrow': 'bi-arrow-90deg-left',
    'up_arrow': 'bi-arrow-90deg-up',
    'open_new_tab': 'bi-arrow-up-right-square',
    'page_leave': 'bi-door-open',
  }

  if (event['info'].split(' ').includes('outside,')) return 'bi-house-door'

  return convert_table[event_name]
}

function event_to_color(event) {
  let event_name = event['name']

  let opacity = 0.25;
  let sat = '100%';
  let bright = '50%';

  let convert_table = {
    'page_nav': `hsla(160, ${sat}, ${bright},${opacity})`,
    'vimeo_play': `hsla(50,${sat},${bright},${opacity})`,
    'vimeo_pause': `hsla(35,${sat},${bright},${opacity})`,
    'filter_use': `hsla(312,${sat},${bright},${opacity})`,
    'return_arrow': `hsla(118,${sat},${bright},${opacity})`,
    'up_arrow': `hsla(118,${sat},${bright},${opacity})`,
    'open_new_tab': `hsla(182,${sat},${bright},${opacity})`,
    'page_leave': `hsla(0,${sat},${bright},${opacity})`,
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

  events.value = await axios.get(url, {params: params,timeout:2000})
      .then(response => response.data)
  console.log(JSON.parse(JSON.stringify(events.value)))
}

onMounted(() => {
  fetch_events()
})

</script>

<template>
  <div class="wrapper">
    <div :class="`date_wrapper `" v-for="(users,date) in events" :key="date">
      <h4 style="position: absolute;top: -30px">{{ date }}</h4>

        <div class="user_wrapper" v-for="(data,user) in users" :key="user">
          <country-component :data="data" :time="format_date(data['events'][0]['timestamp'])"/>
          <div class="event_wrapper" v-for="(event) in data['events']" :key="event['timestamp']">

            <p :class="`${event_to_icon(event)} event_icon`"
               :style="`font-size: 1em;background-color:${event_to_color(event)}`"/>

            <p class="event_title">{{ event['info'] !== 'null' ? event['info'] : event['name'] }}</p>

            <div :class="`time_sep ${event['diff']>60 && event['info']==='id: 998917047' ? 'completed':''}`"
                 v-if="event['diff']>5">
              <h4 class="time_title">{{ parse_seconds(Math.round(event['diff'])) }}</h4>
              <div class="bi-clock-history" style="font-size: 0.7em;line-height: 0.7em"></div>
            </div>

          </div>
        </div>


    </div>
  </div>
</template>

<style scoped>
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
  /*width: 250px;*/
  padding: 15px;
  border-radius: 10px;
  max-height: 500px;
  overflow: scroll;
  align-content: flex-start;
  width: 260px;
}

.event_wrapper {
  position: relative;
  /*padding: 10px;*/
  text-align: center;
  border-radius: 5px;
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
  font-size: 0.8em;
  line-height: normal;

  /*white-space: nowrap;*/
  /*overflow: hidden;*/
}

.event_title {
  text-align: left;
  line-height: 1;
  font-size: 1.5em;

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
  border-radius: 25%;
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
  background-color: #383838;
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
