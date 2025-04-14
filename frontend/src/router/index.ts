import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  {
    path: '/replay',
    name: 'Replay',
    component: () => import('../views/Replay.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router