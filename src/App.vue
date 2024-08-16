<script setup>
import index from '/data_parser/dumps/parsed_dump.json'
import CountryComponent from "@/components/CountryComponent.vue";
import {computed, onBeforeUnmount, onMounted} from "vue";

let sorted_stamps = computed(()=> index)

function parse_date(date){
  return `${date.slice(6, 8)}/${date.slice(4,6)}/${date.slice(0, 4)}`
}

function event_to_icon(event){
  let convert_table = {
    'router_nav':'bi-caret-right-fill',
    'iframe_use':'bi-play-btn',
    'filter_use':'bi-funnel-fill',
    'nav_return_arrow':'bi-arrow-90deg-left',
    'nav_up_arrow':'bi-arrow-90deg-up',
    'open_new_tab':'bi-arrow-up-right-square',
    'page_leave':'bi-door-open',
  }
  return convert_table[event]
}

</script>

<template>
  <div class="wrapper">
    <div class="date_wrapper" v-for="entry in sorted_stamps" :key="entry['date']">
      <h4 style="position: absolute;top: -30px">{{ parse_date(entry['date']) }}</h4>
      <div class="user_wrapper" v-for="(values,user) in entry['users']" :key="user">
        <country-component :country="values['geo']"/>
        <div class="event_wrapper" v-for="(event) in values['events']" :key="event['timestamp']">

          <p :class="event_to_icon(event['event_name'])+ ' ' + 'event_title'">
            {{event['event_info']}}</p>

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
  padding: 10px;
  border-radius: 5px;
  max-height: 500px;
  overflow: scroll;
  align-content: flex-start;
}

.event_wrapper {
  padding: 10px;
  text-align: center;
  background-color: #383838;
  border-radius: 5px;
  display: flex;
  flex-flow: column wrap;
  gap: 5px;
  width: 100%;
}
.event_title {
  display: flex;
  flex-flow: row;
  justify-content: flex-start;
  align-items: center;
  text-align: left;

  gap: 10px;
  word-break: break-word;
}
.time_sep {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  /*margin-bottom: 15px;*/
  /*margin-left: 20px;*/
}

.time_title {
  font-size: 0.8em;
  line-height: 0.8em;
  margin-left: 10px;
  /*outline: 1px solid orange;*/
}
</style>
