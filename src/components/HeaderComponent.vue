<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps({
  value: {
    type: String,
    default: null,
  },
});

</script>

<template>
  <div class="country_wrapper">
    <h3 style="white-space: nowrap;">{{ value }}</h3>
  </div>
</template>

<style scoped>
.country_wrapper {
  /*color: white;*/
  display: flex;
  flex-flow: row;
  width: 100%;
  align-items: center;
  justify-content: flex-start;

  gap: 10px;
  padding: 10px;
  background-color: #383838;
  border-radius: 10px;
}
.country_wrapper h3 {
  font-weight: 900;
  font-size: 0.9em;
}
.flag {
  height: 15px;
}
</style>