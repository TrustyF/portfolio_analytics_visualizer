import './assets/main.css'
import 'bootstrap-icons/font/bootstrap-icons';
import 'bootstrap-icons/font/bootstrap-icons.css'
import axiosRetry from 'axios-retry';
import axios from "axios";

import { createApp } from 'vue'
import App from './App.vue'

axiosRetry(axios, {
    retryDelay: ((count) => count * 1000),
    retries: 5,
    onRetry: ((retryCount, error) => console.log('retry', retryCount, error.message, error.code)),
    retryCondition: ((error) => true)
});
createApp(App).mount('#app')
