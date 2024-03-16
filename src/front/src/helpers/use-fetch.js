import { toRefs, reactive, unref } from "vue";

const BASE = '/api';

const baseFetch = function (url, options) {
    const state = reactive({
        status: 0,
        response: [],
        error: null,
        fetching: false,
    });
    
    const fetchData = async () => {
        try {
            state.fetching = true;
            const res = await fetch(BASE + url, {mode: 'cors', credentials: 'include', ...options});
            state.status = res.status;
            const json = await res.json();
            state.response = json;
        } catch (errors) {
            state.error = errors;
        } finally {
            state.fetching = false;
        }
    };
    return { ...toRefs(state), fetchData };
}

class OptionBuilder {
    constructor() {
        this._options = {}; 
    }
    addOption(key, value = null) {
        const tmp = {};
        tmp[key] = unref(value);
        Object.assign(this._options, value === null ? null : tmp);
        return this;
    }
    build() {
        return this._options;
    }
}

const useFetch = (url, {method = 'GET', body = null, headers = null} = {}) => {
    const resp = reactive({ status: 0, response: [], error: null, fetching: false });
    const exec = async () => {
        console.log(new OptionBuilder()
        .addOption('method', method)
        .addOption('body', body)
        .addOption('headers', headers)
        .build())
        const { status, response, error, fetchData, fetching } = baseFetch(
            unref(url),
            new OptionBuilder()
            .addOption('method', method)
            .addOption('body', body)
            .addOption('headers', headers)
            .build()
        );
        fetchData();
        resp.status = status; resp.response = response; resp.error = error; resp.fetching = fetching;
    };
    return { exec, ...toRefs(resp) };
};

export { baseFetch };
export { BASE }

export default useFetch;

