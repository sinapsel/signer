<template>
    <h2>Send to check</h2>
    <blockquote>
        <p>Pick only file if attached signature. Pick both file and digital signature if detached.</p>
    </blockquote>
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
        <div class="file-field input-field">
            <div class="btn teal darken-4">
                <span>Signature</span>
                <input type="file" name="signature" @change="onUploadFile">
            </div>
            <div class="file-path-wrapper">
                <input class="file-path validate" type="text">
            </div>
        </div>
        <button type="submit" class="waves-effect waves-light btn-large teal darken-4"><i
                class="material-icons right">send</i>send</button>
    </form>

    <div class="progress teal darken-4" v-show="isFileLoading">
        <div class="indeterminate"></div>
    </div>

</template>

<style scoped>
blockquote {
    border-left: 5px solid #004d40;
}
</style>

<script setup>
import { reactive, toRef, ref, unref, computed, watch, isRef } from 'vue';
import useFetch from '@h/use-fetch';
import {useRouter} from 'vue-router';

const router = useRouter();

const files = reactive({
    signature: undefined,
    file: undefined
});

const formFiles = computed(() => {
    const form = new FormData();
    if (files.file) form.append('file', files.file);
    if (files.signature) form.append('signature', files.signature);

    return form;
});

const urlToVerify = computed(() => {
    if (files.signature && files.file) return '/verification/detached';
    if (files.file) return '/verification/attached';
    return '';
})

const filesResponser = computed(() => {
    return filesResponse.value;
})


function onUploadFile(e) {
    files[e.target.name] = e.target.files[0];
}

const { exec: sendFiles,
        status: filesStatus,
        response: filesResponse,
        error: filesError,
        fetching: isFileLoading } = useFetch(urlToVerify, {method: 'POST', body: formFiles});
        

watch(isFileLoading, (newVal, oldVal) => {
    if (newVal) return; // only on finished query

    if (filesError.value) {
        M.toast({html: 'Something went wrong...'});
        console.log(filesError.value)
        return;
    }
    
    if (filesStatus.value >= 400) {
        M.toast({ html: `
            <b>Error ${filesStatus.value}: </b> <em>${JSON.stringify(unref(filesResponse).detail)}</em>
            ` });
        return;
    }

    M.toast({ html: 'Task created...' });
    setTimeout( () => router.push({ path: `/verify/check/${unref(filesResponse).id}`}), 1000);

}, { deep: true })

async function sendForm(e) {
    e.preventDefault();

    if (!files.file) {
        M.toast({ html: '<b>Pick a file first!</b>', classes: 'rounded' });
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
</script>