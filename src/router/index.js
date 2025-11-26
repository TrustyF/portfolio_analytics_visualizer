import {createRouter, createWebHistory} from 'vue-router'
import HomeView from "@/views/HomeView.vue";
import SessionReplay from "@/components/SessionReplay.vue"; // your component


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "home",
            component: HomeView
        },
        {
            path: "/replay/:sessionId",
            name: "replay",
            component: SessionReplay,
            props: true, // IMPORTANT ✔ converts :sessionId to a prop
        },
    ],
})

export default router
