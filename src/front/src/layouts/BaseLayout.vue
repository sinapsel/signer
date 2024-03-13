<script setup>
import { RouterView } from 'vue-router';
import NavBar from '@c/NavBar.vue';
import FooterBar from '@c/FooterBar.vue';

</script>

<template>
    <NavBar/>

    <div class="container">
        <slot></slot>
    </div>

    <FooterBar/>
</template>