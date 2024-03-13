import { createRouter, createWebHistory } from "vue-router";
import layouts from "@l/";

const routerBuilder = (routes) => createRouter({
    history: createWebHistory(),
    routes: [...routes, {
        name: 'error',
        path: '/:pathMatch(.*)*',
        meta: {layout: layouts.base},
        component: () => import('@v/NotFound.vue')
    }],
    linkExactActiveClass: "active"
})

export default routerBuilder;