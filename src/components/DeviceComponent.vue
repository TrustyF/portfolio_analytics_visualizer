<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps({
  device: {
    type: String,
    default: "null",
  },
});

let p_device = computed(() => props.device.split('/')[0].toLowerCase())
let brand = computed(() => props.device.split('/')[1].toLowerCase())
// let platform = computed(() => props.device.split('/')[1].toLowerCase())

</script>

<template>
  <div class="device_wrapper">
    <div class="bi-phone" v-if="p_device==='mobile'"/>
    <div class="bi-laptop" v-if="p_device==='desktop'"/>
    <div class="bi-apple" v-if="brand==='apple'"/>
  </div>
</template>

<style scoped>
.device_wrapper {
  /*position: absolute;*/
  background-color: #383838;
  display: flex;
  flex-flow: row;
  padding: 3px 10px 3px 10px;
  border-radius: 8px;
  gap: 5px;
  justify-items: center;
  align-content: center;
  align-items: center;
}
</style>