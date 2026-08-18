<script setup>
import {inject, onMounted, onUnmounted, ref} from "vue";
import RRWebPlayer from "rrweb-player";
import "/src/assets/rrweb_style.css";
import {useRouter} from "vue-router";
import CountryComponent from "@/components/CountryComponent.vue";
import {unpack} from "@rrweb/packer/unpack";

let props = defineProps({sessionId: Number});

let curr_api = inject('curr_api')
let router = useRouter()

const playerContainer = ref(null);
const session_info = ref(null)
const reduceGapsEnabled = ref(localStorage.getItem('reduceTimestampGaps') !== 'false')
const notEnoughEvents = ref(false)

function toggleReduceGaps() {
  reduceGapsEnabled.value = !reduceGapsEnabled.value
  localStorage.setItem('reduceTimestampGaps', reduceGapsEnabled.value)
  if (parsedEvents) renderPlayer()
}
const PlayerContainerObserver = new ResizeObserver(entries => {
  for (let entry of entries) scaleToFitParent(entry.target)
})

function nav(new_id) {
  router.push(`/replay/${new_id}`)
}

function home() {
  router.push('/')
}

function set_viewed() {
  const res = fetch(`${curr_api}/session/set_viewed/${props.sessionId}`);
}

function reduceTimestampGaps(events, maxGap = 1000) {
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

let parsedEvents = null;

function renderPlayer() {
  playerContainer.value.innerHTML = ''

  if (parsedEvents.length < 2) {
    notEnoughEvents.value = true
    return
  }
  notEnoughEvents.value = false

  const compressed = reduceGapsEnabled.value ? reduceTimestampGaps(parsedEvents, 1000) : parsedEvents

  // initialize rrweb player
  const rep = new RRWebPlayer({
    target: playerContainer.value,
    props: {
      events: compressed,
      skipInactive: false,
      inactiveColor: '#d30000',
    }
  })

  rep.setSpeed(8)
}

async function init_rrewb_player() {
  // fetch events from backend
  const res = await fetch(`${curr_api}/session/get/${props.sessionId}`);
  const events = await res.json();

  parsedEvents = events.map((e) => unpack(e))
  set_viewed()

  renderPlayer()
}

async function get_session_info() {
  const res = await fetch(`${curr_api}/session/get_session_info/${props.sessionId}`);
  session_info.value = await res.json()
}

function scaleToFitParent(container) {
  const parent = container.parentElement;

  // Get dimensions
  const parentWidth = parent.clientWidth;
  const parentHeight = parent.clientHeight;
  const containerWidth = container.scrollWidth;
  const containerHeight = container.scrollHeight;

  // Calculate scale ratios
  const scaleX = parentWidth / containerWidth;
  const scaleY = parentHeight / containerHeight;

  // Use the smaller scale to fit both dimensions
  const scale = Math.min(scaleX, scaleY);

  // Apply transform
  container.style.transform = `scale(${scale})`;
  container.style.transformOrigin = 'top left'; // Adjust as needed
}

onMounted(() => {
  init_rrewb_player()
  get_session_info()
  PlayerContainerObserver.observe(playerContainer.value)
  window.addEventListener('resize', () => scaleToFitParent(playerContainer.value))
})

onUnmounted(() => {
  PlayerContainerObserver.disconnect()
  if (playerContainer.value) {
    const container = playerContainer.value.el || document.getElementsByClassName('rrweb-player-container')[0]
    if (container) container.innerHTML = ''
    playerContainer.value = null
  }
})

</script>

<template>
  <div class="wrapper">

    <div class="nav">
      <div class="bi-arrow-left arrow" style="top: 250px"
           v-show="!session_info || session_info['prev_session']"
           @click="nav(session_info['prev_session'])">
<!--        <h1 class="arrow_text">{{ session_info?.['prev_session'] }}</h1>-->
      </div>
      <div class="bi-arrow-right arrow" style="left: auto;right: 0;top: 250px"
           v-show="!session_info || session_info['next_session']"
           @click="nav(session_info['next_session'])">
<!--        <h1 class="arrow_text">{{ session_info?.['next_session'] }}</h1>-->
      </div>
      <div class="bi-house-fill arrow" style="top: 100px"
           @click="home()"></div>

      <div :class="`arrow ${reduceGapsEnabled ? 'bi-hourglass-split' : 'bi-hourglass'}`" style="top: 400px"
           :title="`Reduce timestamp gaps: ${reduceGapsEnabled ? 'on' : 'off'}`"
           @click="toggleReduceGaps()"></div>

      <div class="country_comp">
        <country-component :data="session_info" v-if="session_info?.id"/>
      </div>
    </div>

    <div class="player_wrapper">
      <div class="rrweb-player-container" ref="playerContainer"/>
      <div class="not_enough_events" v-if="notEnoughEvents">
        <p>Not enough activity to replay this session.</p>
      </div>
    </div>

  </div>

</template>

<style scoped>
.wrapper {
  /*outline: 1px solid red;*/
  width: 100%;
  height: 90vh;
  position: relative;
  display: flex;
  flex-flow: column;
}

.player_wrapper {
  /*outline: 1px solid blue;*/
  position: relative;
  width: 100%;
  height: 100%;
}

.rrweb-player-container {
  position: absolute;
  left: 0;
  top: 0;
  /*outline: 3px solid green;*/
  /*height: 100%;*/
  /*width: 100%;*/
}

.not_enough_events {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.6;
}

.nav {
  display: flex;
  flex-flow: row;
  gap: 10px;
  align-items: center;
  justify-content: flex-start;
  margin-bottom: 10px;
}

.arrow {
  padding: 10px 15px 10px 15px;
  cursor: pointer;
  /*position: absolute;*/
  left: 0;
  font-size: 2em;
  text-align: center;
}

.arrow_text {
  font-size: 0.5em;
}

.country_comp {
  width: 200px;
}
</style>