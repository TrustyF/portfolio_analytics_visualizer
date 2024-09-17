<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import {parse_seconds} from "@/helpers.js";
import portfolio from '@/assets/portfolio.ico'
import trusty_corner from '@/assets/trusty_corner.ico'
import shufflers from '@/assets/shufflers.ico'

let props = defineProps({
  data: {
    type: String,
    default: null,
  },
  time: {
    type: String,
    default: null,
  },
});

function source_icon(src) {
  let mapping = {
    'portfolio': portfolio,
    'trusty_corner': trusty_corner,
    'shufflers': shufflers,
  }
  return mapping[src]
}

function source_color(src) {
  let mapping = {
    'portfolio': 'green',
    'trusty_corner': 'purple',
    'shufflers': 'yellow',
  }
  return mapping[src]
}

function getFlagEmoji(countryCode) {
  const codePoints = countryCode
      .toUpperCase()
      .split('')
      .map(char => 127397 + char.charCodeAt());
  return String.fromCodePoint(...codePoints);
}


</script>

<template>
  <div :class="`country_wrapper ${source_color(data['source'])}`">
    <h3 class="overline">{{ `${getFlagEmoji(data['geo']['country_code2'])} ${data['geo']['state_prov']}` }}</h3>
    <h4 class="underline">{{
        `${time} - ${data['geo']['zipcode']} - ${data['source']}`
      }}</h4>
    <img :src="`${source_icon(data['source'])}`" class="source" style="font-size: 1em" alt="source">

    <div class="user_total_time">
      <h4 class="underline">{{ parse_seconds(Math.round(data['total_time'])) }}</h4>
      <div class="bi-clock-history" style="font-size: 0.7em;line-height: 0.7em"></div>
    </div>

  </div>
</template>

<style scoped>
.country_wrapper {
  /*color: white;*/
  position: relative;
  display: flex;
  flex-flow: column;
  width: 100%;
  align-items: flex-start;
  justify-content: flex-start;

  /*gap: 3px;*/
  padding: 10px;
  background-color: #383838;
  border-radius: 10px;
  overflow: hidden;
}

.user_total_time {
  position: absolute;
  z-index: 10;

  display: flex;
  align-items: center;
  right: 0;
  bottom: 0;
  gap: 5px;

  opacity: 0.5;
  font-size: 0.8em;

  padding: 3px;
  /*background-color: #383838;*/
  border-radius: 5px;
}

.source {
  position: absolute;
  right: 0;
  top: 0;
  margin: 5px;
  width: 15px;
  object-fit: cover;
  opacity: 0.7;
  /*background-color: #282828;*/
}

.overline {
  white-space: nowrap;
  color: white;
  opacity: 0.8;
}

.underline {
  white-space: nowrap;
  font-size: 0.7em;
}

.bg_flag {
  position: absolute;
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
  /*opacity: 0.05;*/
  filter: opacity(0.1);
}

.country_wrapper h3 {
  font-weight: 900;
  font-size: 0.9em;
}

.flag {
  height: 15px;
}

.green {
  background-color: #06402d;
}

.purple {
  background-color: #2a1240;
}

.yellow {
  background-color: #403512;
}

</style>