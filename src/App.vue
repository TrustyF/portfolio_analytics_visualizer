<script setup>
import index from '/data_parser/dumps/parsed_dump.json'
import CountryComponent from "@/components/CountryComponent.vue";
import {computed, onBeforeUnmount, onMounted} from "vue";

let sorted_stamps = computed(() => index)

function parse_date(date) {
  return `${date.slice(6, 8)}/${date.slice(4, 6)}/${date.slice(0, 4)}`
}

function event_to_icon(event) {

  let event_name = event['event_name']

  let convert_table = {
    'router_nav': 'bi-arrow-right',
    'iframe_use': 'bi-play-btn',
    'filter_use': 'bi-funnel',
    'nav_return_arrow': 'bi-arrow-90deg-left',
    'nav_up_arrow': 'bi-arrow-90deg-up',
    'open_new_tab': 'bi-arrow-up-right-square',
    'page_leave': 'bi-door-open',
  }

  if (event['event_info'].split(' ').includes('outside,')) return 'bi-arrow-down'

  return convert_table[event_name]
}

function event_to_color(event) {
  let event_name = event['event_name']

  let opacity = 0.25;
  let sat = '100%';
  let bright = '50%';

  let convert_table = {
    'router_nav': `hsla(160, ${sat}, ${bright},${opacity})`,
    'iframe_use': `hsla(50,${sat},${bright},${opacity})`,
    'filter_use': `hsla(312,${sat},${bright},${opacity})`,
    'nav_return_arrow': `hsla(118,${sat},${bright},${opacity})`,
    'nav_up_arrow': `hsla(118,${sat},${bright},${opacity})`,
    'open_new_tab': `hsla(182,${sat},${bright},${opacity})`,
    'page_leave': `hsla(0,${sat},${bright},${opacity})`,
  }

  return convert_table[event_name]

}

</script>

<template>
  <div class="wrapper">
    <div class="date_wrapper" v-for="entry in sorted_stamps" :key="entry['date']">
      <h4 style="position: absolute;top: -30px">{{ parse_date(entry['date']) }}</h4>
      <div class="user_wrapper" v-for="(values,user) in entry['users']" :key="user">
        <country-component :country="values['geo']"/>
        <div class="event_wrapper" v-for="(event) in values['events']" :key="event['timestamp']"
             >

          <p :class="`${event_to_icon(event)} event_icon`" :style="`font-size: 1em;background-color:${event_to_color(event)}`"/>

          <p class="event_title">{{ event['event_name']==='router_nav' ? event['event_info'].split(',')[1] : event['event_info']}}</p>

          <div class="bi-clock-history time_sep" v-if="event['diff']>0">
            <h4 class="time_title">{{ Math.round(event['diff']) }}</h4>
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
  /*outline: 1px solid orange;*/
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  align-items: flex-start;

  gap: 20px;
  border: 1px solid #282828;
  padding: 30px;
  border-radius: 10px;
}

.user_wrapper {
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
}

.event_wrapper {
  position: relative;
  /*padding: 10px;*/
  text-align: center;
  border-radius: 5px;
  /*display: flex;*/
  /*flex-flow: row nowrap;*/
  display: grid;
  grid-template-columns: 1fr 6fr 1fr;
  gap: 10px;
  width: 100%;
}

.event_wrapper p {
  font-size: 0.9em;
  line-height: normal;

  white-space: nowrap;
  overflow: hidden;
  /*text-overflow: ellipsis;*/
  /*overflow-x: scroll;*/
}

.event_title {
  /*outline: 1px solid red;*/
  display: flex;
  flex-flow: row;
  justify-content: flex-start;
  align-items: center;
  text-align: left;
  line-height: 1;
  font-size: 1.5em;

  gap: 10px;
}

.event_icon {
  display: flex;
  flex-flow: column;
  justify-content: center;
  border-radius: 50%;
  aspect-ratio: 1;
  color: white;
}

.time_sep {
  /*outline: 1px solid red;*/
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.time_title {
  font-size: 0.7em;
  line-height: 0.7em;
  margin-left: 3px;
  /*outline: 1px solid orange;*/
}
</style>
