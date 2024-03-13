import { defineAsyncComponent } from "vue";

const layouts = {
    base: defineAsyncComponent(() => import('@l/BaseLayout.vue')),
    empty: defineAsyncComponent(() => import('@l/EmptyLayout.vue'))
}

export default layouts;

export const empty = layouts.empty;