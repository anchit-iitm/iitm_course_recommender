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
app.config.globalProperties.$chartColors = {
  p3: ['#003f5c', '#bc5090', '#ffa600'],
  p4: ['#003f5c', '#7a5195', '#ef5675', '#ffa600',],
  p5: ['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600'],
  p6: ['#003f5c', '#444e86', '#955196', '#dd5182', '#ff6e54', '#ffa600',],
}


app.config.errorHandler = function (err, vm, info) {   
    console.log(err, vm, info)
  }

registerPlugins(app)
app.component('CourseCard', CourseCard)
app.component('vtoast', vtoast)
app.mount('#app')
