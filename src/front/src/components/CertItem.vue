<script setup>
import { toRef, computed } from 'vue';

const props = defineProps({
    data: {
        type: Object
    }
});

const currentDate = new Date();

const expired = computed(() => {
    return new Date(props.data.expire) <= currentDate;
});

const signType = computed(() => {
    return props.data.type === 'pub' ? 'public' : 'private';
})
</script>

<template>
    <li>
    <div class="collapsible-header">
      <i class="material-icons">vpn_key</i>
      {{ props.data.id }}
      <span class="new badge" :class="expired ? 'red' : 'green'" data-badge-caption="">{{ props.data.expire }}</span>
      <a :href="`/api/certs/uid/${props.data.id}?ascii=true`" class="secondary-content teal-text darken-4"><i class="material-icons">file_download</i></a></div>
    <div class="collapsible-body">
        <p><em>FINGERPRINT:</em> <b>{{ props.data.fingerprint }}</b></p>
        <p><em>type:</em> {{ signType }}</p>
        <p><em>algorithm:</em> {{ props.data.algo }}</p>
        <p><em>created:</em> {{ props.data.started }}</p>
        <p><em>credential:</em> {{ props.data.credentials }}</p>
    </div>
  </li>
</template>

<style scoped>
p {
    font-size: large;
}
</style>