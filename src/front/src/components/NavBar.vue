<script setup>
import NavBarElement from './NavBarElement.vue';
import {useRoute} from 'vue-router';
import {computed, onMounted} from 'vue';

const navLinks = [
    { link: '/', text: 'Home' },
    { link: '/verify', text: 'Verify' },
    { link: '/certs', text: 'Trusted Certificates' },
    { link: '/sign', text: 'Sign' }
];

const route = useRoute();

</script>

<template>

    <nav>
        <div class="nav-wrapper teal darken-4">
            <router-link :to="'/'"><span class="brand-logo center">Signer <i class="material-icons">create</i></span></router-link>
            <a href="#" data-target="mobile-nav" class="sidenav-trigger"><i class="material-icons">menu</i></a>
            <ul class="left hide-on-med-and-down">
                <NavBarElement v-for="{ link, text } in navLinks" :link="link" :text="text" :isActive="route.path === link" />
            </ul>
        </div>
    </nav>
    
    <ul class="sidenav" id="mobile-nav">
        <NavBarElement v-for="{ link, text } in navLinks" :link="link" :text="text" :isActive="route.path === link" />
    </ul>

</template>

<style scoped></style>

<script>

</script>