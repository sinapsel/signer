<script setup>
import { ref, toRef, computed, onUpdated } from 'vue';

const props = defineProps({
    certList: {
        type: Object
    },
    value: {
        type: String
    }
});

const emits = defineEmits(['update:value']);

const value = ref(props.value);


onUpdated(() => {
    M.AutoInit();
})
</script>

<template>
    <div class="">
        <select v-model="value" @change="$emit('update:value', $event.target.value)">
            <option value="" disabled selected>Choose your certificate</option>
            <option v-for="_cert in certList" :value="_cert.id" :key="_cert.id">{{ _cert.id }}</option>
        </select>
        <label>Private certificate</label>
    </div>

</template>

<style scoped>
p {
    font-size: large;
}
</style>