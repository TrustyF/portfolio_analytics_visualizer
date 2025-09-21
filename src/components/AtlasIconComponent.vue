<script setup>

import {computed} from "vue";

let props = defineProps(['at_id']);
let emits = defineEmits(["test"]);


let icon_scale = computed(() => 0.25)
let icon_size = computed(() => `${120 * icon_scale.value}px`)
let image_size = computed(() => `${100 * icon_scale.value}px`)

let ico_atlas_pos = computed(() => {
  let id = props['at_id'] - 1

  let size = -100 * icon_scale.value
  let padding = 2.5 * icon_scale.value
  let y = Math.floor(id / 10) % 10
  let x = id % 10

  return `${(x * size) - padding}px ${(y * size) - padding}px`
})
let ico_atlas = computed(() => {
  let id = props['at_id'] - 1

  let cus_id = Math.floor(id / 100)
  let str_url = `/atlas/atlas_${cus_id}.webp`
  // let url = new URL(str_url, import.meta.url).href
  return `url(${str_url})`
})
</script>

<template>
  <div>
    <p class="atlas_icon"/>
  </div>
</template>

<style scoped>

.atlas_icon {
  max-width: v-bind(icon_size);

  background-size: calc(1000px * v-bind(icon_scale));
  background-image: v-bind(ico_atlas);
  background-position: v-bind(ico_atlas_pos);
  background-repeat: no-repeat;
  width: calc(100px * v-bind(icon_scale));
  aspect-ratio: 1;
}
</style>