import routerBuilder from '@r/';
import layouts from '@l/';
import { defineAsyncComponent } from 'vue';

const router = routerBuilder([
    {
        name: 'base',
        path: '/',
        meta: {layout: null},
        children: [
            {
                name: 'home',
                path: '',
                meta: {layout: layouts.base},
                component: () => import('@v/HomePage.vue')
            },
            {
                name: 'certs',
                path: '/certs',
                meta: {layout: layouts.base},
                component: () => import('@v/Certificates.vue')
            }
        ]
    }
]);

export default router;