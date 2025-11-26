<script setup>

import {onMounted, ref} from "vue";
import RRWebPlayer from "rrweb-player";
import "/src/assets/rrweb_style.css";
import {useRouter} from "vue-router";

let router = useRouter()

let props = defineProps({sessionId: Number});

const playerContainer = ref(null);

function nav(dir) {
  router.push(`/replay/${+props.sessionId + +dir}`)
}

function home(){
  router.push('/')
}

function del(){

}

onMounted(async () => {
  // fetch events from backend
  // const res = await fetch(`http://127.0.0.1:5000/event/session/${props.sessionId}`);
  const res = await fetch(`https://analytics-trustyfox.pythonanywhere.com/event/session/${props.sessionId}`);
  const events = await res.json();

  // console.log(events)

  // initialize rrweb player
  const rep = new RRWebPlayer({
    target: playerContainer.value,
    props: {
      events: events,
      width: 950,
      inactiveColor: '#d30000',
    }
  })
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
}

.arrow {
  padding: 10px 15px 10px 15px;
  cursor: pointer;
  position: absolute;
  left: 0;
  font-size: 2em;
}
</style>