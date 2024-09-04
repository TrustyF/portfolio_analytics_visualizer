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

</script>

<template>
  <div class="country_wrapper">
    <!--    <img :src="data['country_flag']" alt="country" class="flag">-->
    <h3 class="overline">{{ `${data['country_emoji']} ${data['state_prov']}` }}</h3>
    <h4 class="underline">{{ `${time} - ${data['zipcode']}` }}</h4>
<!--    <h4 class="underline">{{ ` ${data['isp']}` }}</h4>-->
  </div>
</template>

<style scoped>
.country_wrapper {
  /*color: white;*/
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