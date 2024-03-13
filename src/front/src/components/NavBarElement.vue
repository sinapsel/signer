<script setup>
import { onMounted } from 'vue';


const props = defineProps({
    link: {
        type: String,
        required: false,
        default: '#'
    },
    text: {
        type: String,
        required: false,
        default: ''
    },
    isActive: {
        type: Boolean,
        required: false,
        default: undefined
    }
});

</script>

<template>
    <li :class="{active: props.isActive}">
        <router-link :to="props.link">
            {{ props.text }}
        </router-link>
    </li>
</template>