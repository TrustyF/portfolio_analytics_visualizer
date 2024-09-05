<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

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
    'portfolio': 'bi-file-earmark-person-fill',
    'trusty_corner': 'bi-film',
  }
  return mapping[src]
}

</script>

<template>
  <div class="country_wrapper">
    <h3 class="overline">{{ `${data['geo']['country_emoji']} ${data['geo']['state_prov']}` }}</h3>
    <h4 class="underline">{{
        `${time} - ${data['geo']['zipcode']} - ${data['source']}`
      }}</h4>
    <h2 :class="`${source_icon(data['source'])} source`" style="font-size: 1em"></h2>
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
.source {
  position: absolute;
  right: 0;
  top: 0;
  padding: 5px;
  /*background-color: #282828;*/
}
.overline {
  white-space: nowrap;
  color: white;
}

.underline {
  white-space: nowrap;
  font-size: 0.7em;
}

.country_wrapper h3 {
  font-weight: 900;
  font-size: 0.9em;
}

.flag {
  height: 15px;
}
</style>