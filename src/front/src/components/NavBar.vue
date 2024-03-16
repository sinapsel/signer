<script setup>
import NavBarElement from './NavBarElement.vue';
import { useRoute, useRouter } from 'vue-router';
import { ref, computed, onMounted, watch, unref } from 'vue';
import useFetch from '@h/use-fetch';
import { checkCookie, clearCookie} from '@h/cookies.js'

const navLinks = [
    { link: '/', text: 'Home' },
    { link: '/verify', text: 'Verify' },
    { link: '/certs', text: 'Trusted Certificates' },
    { link: '/sign', text: 'Sign' }
];

const route = useRoute();
const router = useRouter();

const login = ref('');
const password = ref('');
const token = computed(() => btoa(login.value + ':' + password.value));
const basicAuthHeaders = computed(() => {return {'Authorization': 'Basic ' + token.value}});

const { exec: auth,
  status: verifyStatus,
  response: verifyResponse,
  fetching: isAuthLoading } = useFetch('/auth/login', {method: 'POST', headers: basicAuthHeaders});

const {exec: unLogin, 
    fetching: isUnauthLoading} = useFetch('/auth/logout')


async function doAuth() {
    if (!login.value || !password.value) {
        M.toast({html: 'empty login or password!'}); 
        return;
    }
    await auth();
} 

async function unlogin() {
    await unLogin().then(() =>  setTimeout(()=> clearCookie(), 200));
}

watch(isAuthLoading, (newVal, oldVal) => {
    if (newVal) return;
    password.value = '';

    if (verifyStatus.value != 200) {
        M.toast({html: verifyResponse?.value?.detail || 'Something went wrong'}); 
        return;
    }

});

watch(isUnauthLoading, (newVal, oldVal) => {
    if (newVal) return;
    router.go();
});

onMounted(() => {
    M.AutoInit();

})

</script>

<template>

    <nav>
        <div class="nav-wrapper teal darken-4">
            <router-link :to="'/'"><span class="brand-logo center">Signer <i
                        class="material-icons">create</i></span></router-link>
            <a href="#" data-target="mobile-nav" class="sidenav-trigger"><i class="material-icons">menu</i></a>
            <ul class="left hide-on-med-and-down">
                <NavBarElement v-for="{ link, text } in navLinks" :link="link" :text="text"
                    :isActive="route.path === link" />
            </ul>

            <ul class="right hide-on-med-and-down">
                <li><a class="waves-effect waves-light btn modal-trigger teal darken-3" href="#modalLogin">Login<i
                            class="material-icons right">{{ checkCookie() ? 'lock' : 'lock_open' }}</i></a></li>
            </ul>
        </div>
    </nav>

    <ul class="sidenav" id="mobile-nav">
        <NavBarElement v-for="{ link, text } in navLinks" :link="link" :text="text" :isActive="route.path === link" />
    </ul>

    <div id="modalLogin" class="modal">
        <div class="modal-content">
            <div v-if="checkCookie()">
                <p>Already authorized</p>
                <a class="waves-effect waves-light btn-large teal darken-4" @click="unlogin">Log out</a>
            </div>
            <div v-else>
                <form  @submit.prevent="doAuth">
                    <div class="row">
                    <div class="input-field col s12">
                        <input id="login" autofocus type="text" class="validate" v-model="login">
                        <label for="login">Login</label>
                    </div>
                </div>
                <div class="row">
                    <div class="input-field col s12">
                        <input id="password" type="password" class="validate" v-model="password">
                        <label for="password">Password</label>
                    </div>
                </div>
                <a class="waves-effect waves-light btn-large teal darken-4" @click="doAuth">Login</a>
                </form>
            </div>
        </div>
        <div class="modal-footer">
            <a href="#!" class="modal-close waves-effect waves-green btn-flat">Close</a>
        </div>
    </div>

</template>

<style scoped></style>

<script>

</script>