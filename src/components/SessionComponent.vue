<script setup>

import CountryComponent from "@/components/CountryComponent.vue";
import {useRouter} from "vue-router";

let props = defineProps({data: Object});
let emits = defineEmits(["test"]);

const router = useRouter()

function open_session(id) {
  router.push({ name: "replay", params: { sessionId: id } });
}

</script>

<template>
  <div class="session_wrapper" :class="{viewed:data['viewed']}" @click="open_session(data['id'])">
    <country-component :data="data"/>
  </div>
</template>

<style scoped>
.session_wrapper {
  cursor: pointer;
  width: 200px;
}
.viewed {
  opacity: 50%;
}
</style>