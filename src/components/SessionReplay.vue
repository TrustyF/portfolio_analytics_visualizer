<script setup>

import {onMounted, ref} from "vue";
import RRWebPlayer from "rrweb-player";
import {Replayer} from "@rrweb/replay";
import "rrweb-player/dist/style.css";
import {unpack} from "@rrweb/packer";

let props = defineProps({sessionId: Number});

const playerContainer = ref(null);

onMounted(async () => {
  // fetch events from backend
  // const res = await fetch(`http://127.0.0.1:5000/event/session/${props.sessionId}`);
  const res = await fetch(`https://analytics-trustyfox.pythonanywhere.com/event/session/${props.sessionId}`);
  const events = await res.json();

  console.log(events)

  // initialize rrweb player
  const rep = new RRWebPlayer({
    target: playerContainer.value,
    props: {
      events:events,
      width: 950,
      height:1100,
    }
  })
  rep.play()

})

</script>

<template>
  <div class="wrapper">
    <div class="rrweb-player-container" ref="playerContainer"></div>
  </div>
</template>

<style scoped>
.wrapper {
  /*outline: 1px solid red;*/
  position: relative;
}

.rrweb-player-container {
  position: absolute;
  /*left: -500px;*/
  z-index: 999;
}
</style>