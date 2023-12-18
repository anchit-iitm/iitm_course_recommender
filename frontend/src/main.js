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
import CourseCard from './components/CourseCard.vue'
import vtoast from './components/vtoast.vue'

// Composables
import { createApp } from 'vue'

const app = createApp(App)
app.config.globalProperties.$hostname = 'http://localhost:3000'
app.config.globalProperties.$api = 'http://localhost:5000/api/v1'
// app.config.errorHandler = (error) => vtoast.show({message: error, color: 'error'})

registerPlugins(app)
app.component('CourseCard', CourseCard)
app.component('vtoast', vtoast)
app.mount('#app')
