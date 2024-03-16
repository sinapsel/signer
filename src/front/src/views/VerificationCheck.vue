<script setup>

import CircleLoader from '@c/CircleLoader.vue';
import { computed, onMounted, toRef, unref, toRefs } from 'vue';
import useFetch from '@h/use-fetch';

const props = defineProps({
  uid: {
    type: String,
    required: true
  }
});

const { uid } = toRefs(props);

const url = computed(() => `/verification/id/${uid.value}`);

const { exec: fetchCheck,
  status: verifyStatus,
  response: verifyResponse,
  error: verifyError,
  fetching: isVerificationLoading } = useFetch(url);

  
onMounted(async () => {
  await fetchCheck();
})

const result = computed(() => {
  if (verifyStatus.value === 425) return {status: 'PENDING', cardStyle: 'blue-grey darken-1'};
  if (verifyStatus.value === 500) return {status: 'FATAL ERROR', cardStyle: 'deep-orange accent-4'}; 
  if (verifyResponse.value.success) return {status: 'SUCCESS', cardStyle: 'green darken-1'}
  if (!verifyResponse.value.success) return {status: 'ERROR', cardStyle: 'orange darken-4'}
});
</script>

<template>
  <h2>Check</h2>

  <CircleLoader v-if="isVerificationLoading"/>

  <div class="row" v-else v-show="result">
    <div class="col s12 m12">
      <div class="card" :class="[result?.cardStyle]">
        <div class="card-content white-text">
          <span class="card-title">{{ result?.status }}</span>
          <p v-html="verifyResponse?.result?.replace('\n', '<br>') || verifyResponse?.detail?.info"></p>
        </div>
        <div class="card-action">
          <a href="#" @click="fetchCheck">Refresh</a>
        </div>
      </div>
    </div>
  </div>
</template>