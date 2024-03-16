<script setup>
import { reactive, toRef, ref, unref, computed, watch, isRef, onMounted } from 'vue';
import useFetch from '@h/use-fetch';
import { useRouter } from 'vue-router';
import CertSelector from '@c/CertSelector.vue';
import CertItem from '@c/CertItem.vue';

const router = useRouter();

const cert = ref('');
const pin = ref('');
const isDetached = ref(true);
const isAscii = ref(true);
const files = reactive({
    file: undefined
});

const kind = computed(() => isDetached ? '--detach-sign' : '--sign');

const formData = computed(() => {
    const form = new FormData();
    if (files.file) form.append('file', files.file);
    form.append('pin', pin.value);
    form.append('user', cert.value);
    form.append('kind', kind.value);
    form.append('ascii', isAscii.value);

    return form;
});

const { exec: fetchPrivateCerts, response: certList, fetching: isCertLoading } = useFetch('/certs/private')
const { exec: sendFiles,
    response: filesResponse,
    error: filesError,
    fetching: isFileLoading,
    status: filesStatus } = useFetch('/signature', {
        method: 'POST',
        body: formData
    })



watch(isCertLoading, (n, o) => {
    if (n) return;
});

const selectedCertInfo = computed(() => {
    return certList.value.filter(el => el.id == cert.value);
})


function onUploadFile(e) {
    files[e.target.name] = e.target.files[0];
}

async function sendForm(e) {
    e.preventDefault();

    if (!files.file) {
        M.toast({ html: '<b>Pick a file first!</b>', classes: 'rounded' });
        return;
    }
    if (!cert.value) {
        M.toast({ html: '<b>Pick a certificate first!</b>', classes: 'rounded' });
        return;
    }
    if (!pin.value) {
        M.toast({ html: '<b>Input pincode!</b>', classes: 'rounded' });
        return;
    }

    try {
        await sendFiles();
    }
    catch (e) {
        if (e instanceof SyntaxError) {
            M.toast({ html: 'Something went wrong' }); return;
        }
        M.toast({ html: e });
    }
}

watch(isFileLoading, (newVal, oldVal) => {
    if (newVal) return; // only on finished query

    if (filesError.value) {
        M.toast({ html: 'Something went wrong...' });
        console.log(filesError.value)
        return;
    }

    if (filesStatus.value >= 400) {
        M.toast({
            html: `
            <b>Error ${filesStatus.value}: </b> <em>${JSON.stringify(unref(filesResponse).detail)}</em>
            ` });
        return;
    }

    M.toast({ html: 'Task created...' });
    setTimeout(() => router.push({ path: `/sign/check/${unref(filesResponse).id}` }), 1000);

}, { deep: true })


onMounted(async () => {
    M.AutoInit();

    await fetchPrivateCerts();
})
</script>

<template>
    <h2>Sign a file</h2>

    <form id="form" @submit.prevent="sendForm">

        <div class="file-field input-field">
            <div class="btn teal darken-4">
                <span>File</span>
                <input type="file" name="file" @change="onUploadFile">
            </div>
            <div class="file-path-wrapper">
                <input class="file-path validate" type="text">
            </div>
        </div>


        <CertSelector v-model:value="cert" :certList="certList" />
        <ul class="collapsible" v-show="cert">
            <CertItem v-for="_cert in selectedCertInfo" :data="_cert" />
        </ul>

        <div class="input-field col s12">
            <input id="pin" type="password" class="validate" v-model="pin">
            <label for="password">PIN</label>
        </div>

        <p>
            <label>
                <input type="checkbox" checked v-model="isDetached" />
                <span>Detached</span>
            </label>
        </p>

        <p>
            <label>
                <input type="checkbox" checked v-model="isAscii" />
                <span>ASCII</span>
            </label>
        </p>

        <button type="submit" class="waves-effect waves-light btn-large teal darken-4"><i
                class="material-icons right">send</i>send</button>
    </form>

    <div class="progress teal darken-4" v-show="isCertLoading">
        <div class="indeterminate"></div>
    </div>

</template>

<style scoped>
blockquote {
    border-left: 5px solid #004d40;
}
</style>
