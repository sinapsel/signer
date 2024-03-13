<script setup>
import { ref, reactive, computed, defineAsyncComponent } from 'vue';
import { RouterView, useRoute } from 'vue-router';
import { empty as emptyLayout } from '@l/';

const route = useRoute();

const layout = computed(() => {
  return route.meta.layout || emptyLayout;
});
</script>

<template>
  <Suspense>
    <component :is="layout">
      <RouterView />
    </component>
  </Suspense>

</template>

<style scoped></style>
