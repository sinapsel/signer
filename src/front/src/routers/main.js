import routerBuilder from '@r/';
import layouts from '@l/';
import { defineAsyncComponent } from 'vue';
import { checkCookie } from '@h/cookies'

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
            },
            {
                name: 'verify',
                path: '/verify',
                meta: {layout: layouts.base},
                component: () => import('@v/Verification.vue')
            },
            {
                name: 'verify-check',
                path: '/verify/check/:uid([a-z0-9]{32})',
                meta: {layout: layouts.base},
                props: route => ({uid: route.params.uid}),
                component: () => import('@v/VerificationCheck.vue')
            },
            {
                name: 'sign',
                path: '/sign',
                meta: {layout: layouts.base, private: true},
                component: () => import('@v/Signaturing.vue')
            },
            {
                name: 'signature-check',
                path: '/sign/check/:uid([a-z0-9]{32})',
                meta: {layout: layouts.base, private: true},
                props: route => ({uid: route.params.uid}),
                component: () => import('@v/SignaturingCheck.vue')
            },
        ]
    }
]);

router.beforeEach(async (to, from, next) => {
    const requireAuth = to.matched.some(r => r.meta?.private);
    if (requireAuth && !checkCookie()) {
        next('/');
    }
    else {
        next();
    }
})

export default router;