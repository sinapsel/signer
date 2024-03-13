<script>

import RowsCollection from '@c/RowsCollection.vue';
import CertItem from '@c/CertItem.vue';
import { defineAsyncComponent, reactive, ref } from 'vue';
import fetchCerts from '@q/fetch-certs.js';

export default {
    async setup() {
        const { exec, response, error, fetching } = fetchCerts();
        await exec();

        return {
            response,
            exec,
            error,
            fetching
        };
    },
    components: {
        RowsCollection, CertItem
    },
    mounted() {
        M.AutoInit();
    }
}

</script>

<template>
    <h2>List</h2>
    <RowsCollection>
        <CertItem v-for="row in response" :data="row"/>
    </RowsCollection>
</template>