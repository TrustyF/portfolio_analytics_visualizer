<script setup>
import {inject, onMounted, ref} from "vue";
import RRWebPlayer from "rrweb-player";
import "/src/assets/rrweb_style.css";
import {useRouter} from "vue-router";
import CountryComponent from "@/components/CountryComponent.vue";

let props = defineProps({sessionId: Number});

let curr_api = inject('curr_api')
let router = useRouter()

const playerContainer = ref(null);
const session_info = ref({})

function nav(new_id) {
  router.push(`/replay/${new_id}`)
}

function home() {
  router.push('/')
}

function del() {

}

function set_viewed() {
  const res = fetch(`${curr_api}/session/set_viewed/${props.sessionId}`);
}

function reduceTimestampGaps(data, maxGap = 1000) {
  // Parse the data if it's a string
  const events = typeof data === 'string'
      ? data.split('\n').filter(line => line.trim()).map(line => JSON.parse(line))
      : data;

  if (events.length === 0) return events;

  // Sort events by timestamp
  events.sort((a, b) => a.timestamp - b.timestamp);

  const result = [];
  let timeOffset = 0;
  let lastOriginalTime = events[0].timestamp;

  for (let i = 0; i < events.length; i++) {
    const event = {...events[i]};
    const currentTime = event.timestamp;
    const gap = currentTime - lastOriginalTime;

    // If gap exceeds maxGap, compress it
    if (gap > maxGap) {
      timeOffset += gap - maxGap;
    }

    // Apply the accumulated offset
    event.timestamp = currentTime - timeOffset;
    result.push(event);

    lastOriginalTime = currentTime;
  }

  return result;
}

async function init_rrewb_player() {
  // fetch events from backend
  const res = await fetch(`${curr_api}/session/get/${props.sessionId}`);
  const events = await res.json();

  const parsed = events.map((e) => JSON.parse(e))
  const compressed = reduceTimestampGaps(parsed, 1000)
  set_viewed()

  // initialize rrweb player
  const rep = new RRWebPlayer({
    target: playerContainer.value,
    props: {
      events: compressed,
      skipInactive: false,
      inactiveColor: '#d30000',
    }
  })

  rep.play()
  rep.setSpeed(4)
}

async function get_session_info() {
  const res = await fetch(`${curr_api}/session/get_session_info/${props.sessionId}`);
  session_info.value = await res.json()
}

onMounted(() => {
  init_rrewb_player()
  get_session_info()
})

</script>

<template>
  <div class="wrapper">

    <div class="rrweb-player-container" ref="playerContainer"></div>

    <div class="bi-arrow-left arrow" style="top: 250px"
         v-show="session_info['prev_session']"
         @click="nav(session_info['prev_session'])"></div>
    <div class="bi-arrow-right arrow" style="left: auto;right: 0;top: 250px"
         v-show="session_info['next_session']"
         @click="nav(session_info['next_session'])"></div>
    <div class="bi-house-fill arrow" style="top: 100px"
         @click="home()"></div>
    <div class="bi-trash arrow" style="top: 400px"
         @click="del()"></div>

    <div class="country_comp">
      <country-component :data="session_info" v-if="session_info?.id"/>
    </div>
  </div>

</template>

<style scoped>
.wrapper {
  /*outline: 1px solid red;*/
  width: 100%;
  position: relative;
  display: flex;
  flex-flow: column;
  align-items: center;
  justify-content: center;
}

.rrweb-player-container {
  /*position: absolute;*/
  /*z-index: 999;*/
  /*transform: translate(-50%,-50%);*/
}

.arrow {
  padding: 10px 15px 10px 15px;
  cursor: pointer;
  position: absolute;
  left: 0;
  font-size: 2em;
}

.country_comp {
  width: 200px;
  position: absolute;
  left: 0;
  top: 700px;
  /*transform: translateY(200%);*/
}
</style>