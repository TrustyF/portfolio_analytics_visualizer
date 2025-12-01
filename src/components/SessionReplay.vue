<script setup>

import {onMounted, ref} from "vue";

import {Replayer} from "@rrweb/replay";
import RRWebPlayer from "rrweb-player";
import "/src/assets/rrweb_style.css";
import {useRouter} from "vue-router";

let router = useRouter()

let props = defineProps({sessionId: Number});

const playerContainer = ref(null);

function nav(dir) {
  router.push(`/replay/${+props.sessionId + +dir}`)
}

function home() {
  router.push('/')
}

function del() {

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
    const event = { ...events[i] };
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

onMounted(async () => {
  // fetch events from backend
  // const res = await fetch(`http://127.0.0.1:5000/event/session/${props.sessionId}`);
  const res = await fetch(`https://analytics-trustyfox.pythonanywhere.com/event/session/${props.sessionId}`);
  const events = await res.json();

  const parsed = events.map((e) => JSON.parse(e))
  const compressed = reduceTimestampGaps(parsed,1000)

  // initialize rrweb player
  const rep = new RRWebPlayer({
    target: playerContainer.value,
    props: {
      events: compressed,
      skipInactive:false,
      inactiveColor: '#d30000',
    }
  })
  // console.log(events)
  // const rep = new Replayer(parsed, {
  //   root: playerContainer.value,
  //   skipInactive: true,
  //   width:950,
  //   height:1000,
  // })
  rep.play()

})

</script>

<template>
  <div class="wrapper">
    <div class="rrweb-player-container" ref="playerContainer"></div>

    <div class="bi-arrow-left arrow" @click="nav(-1)"></div>
    <div class="bi-arrow-right arrow" style="left: auto;right: 0" @click="nav(1)"></div>
    <div class="bi-house-fill arrow" style="top: 100px" @click="home()"></div>
    <div class="bi-trash arrow" style="top: 400px" @click="del()"></div>
  </div>
</template>

<style scoped>
.wrapper {
  /*outline: 1px solid red;*/
  width: 100%;
  position: relative;
  display: flex;
  justify-content: center;
}

.rrweb-player-container {
  /*position: absolute;*/
  z-index: 999;
  /*transform: translate(-50%,-50%);*/
}

.arrow {
  padding: 10px 15px 10px 15px;
  cursor: pointer;
  position: absolute;
  left: 0;
  font-size: 2em;
}
</style>