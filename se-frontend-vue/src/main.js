/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

const app = createApp(App)
app.config.globalProperties.$hostname = 'http://localhost:3000'
app.config.globalProperties.$api = 'http://localhost:5000/api/v1'

registerPlugins(app)

app.mount('#app')
