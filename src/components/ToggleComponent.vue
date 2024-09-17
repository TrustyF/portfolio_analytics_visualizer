<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps({
  title: {
    type: String,
    default: null,
  },
  def: {
    type: Boolean,
    default: false,
  },
});
let emits = defineEmits(["toggle"]);

let toggle = ref()

function emit_toggle(){
  toggle.value = !toggle.value
  emits('toggle',toggle.value)
}
onMounted(()=>{
  toggle.value = props.def
})

</script>

<template>
  <div class="toggle_wrapper" @click="emit_toggle">
    <input type="checkbox" v-model="toggle">
    <p>{{ title }}</p>
  </div>
</template>

<style scoped>
.toggle_wrapper {
  display: flex;
  flex-flow: row;
  gap: 5px;
  cursor: pointer;
}
.toggle_wrapper p {
  user-select: none;
}
</style>